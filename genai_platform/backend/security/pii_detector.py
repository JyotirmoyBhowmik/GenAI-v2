"""
GenAI Platform - PII Detector
Detects and redacts Personally Identifiable Information
"""

import re
from typing import List, Dict, Tuple, Optional
from loguru import logger


class PIIDetector:
    """
    PII (Personally Identifiable Information) detection and redaction.
    Uses regex patterns and rules-based detection.
    """
    
    def __init__(self):
        """Initialize PII detector."""
        from backend.config_manager import get_config
        self.config = get_config()
        
        # Load PII patterns from configuration
        self.patterns = self._load_patterns()
        
        logger.info(f"PIIDetector initialized with {len(self.patterns)} patterns")
    
    def _load_patterns(self) -> Dict[str, Dict]:
        """Load PII detection patterns from configuration."""
        pii_config = self.config.get('policies', 'pii_policies', 'pii_types', default=[])
        
        patterns = {}
        for pii_type in pii_config:
            name = pii_type.get('name')
            if name:
                patterns[name] = {
                    'pattern': pii_type.get('pattern', ''),
                    'sensitivity': pii_type.get('sensitivity', 'medium')
                }
        
        return patterns
    
    def detect(self, text: str) -> List[Dict[str, any]]:
        """
        Detect PII in text.
        
        Args:
            text: Text to scan for PII
            
        Returns:
            List of detected PII instances with type, value, position, sensitivity
        """
        detected = []
        
        for pii_type, pii_info in self.patterns.items():
            pattern = pii_info['pattern']
            sensitivity = pii_info['sensitivity']
            
            try:
                matches = re.finditer(pattern, text)
                for match in matches:
                    detected.append({
                        'type': pii_type,
                        'value': match.group(),
                        'start': match.start(),
                        'end': match.end(),
                        'sensitivity': sensitivity
                    })
            except re.error as e:
                logger.warning(f"Invalid regex pattern for {pii_type}: {e}")
        
        return detected
    
    def redact(self, text: str, redaction_char: str = "*") -> Tuple[str, List[Dict]]:
        """
        Redact PII from text.
        
        Args:
            text: Text to redact
            redaction_char: Character to use for redaction
            
        Returns:
            Tuple of (redacted_text, list_of_detections)
        """
        detections = self.detect(text)
        
        if not detections:
            return text, []
        
        # Sort detections by position (reverse order to preserve indices)
        detections.sort(key=lambda x: x['start'], reverse=True)
        
        redacted_text = text
        for detection in detections:
            pii_type = detection['type']
            start = detection['start']
            end = detection['end']
            value = detection['value']
            
            # Get redaction method from config
            redaction_method = self.config.get(
                'policies', 'pii_policies', 'redaction', 'redaction_methods', pii_type,
                default='mask_all'
            )
            
            # Apply redaction based on method
            redacted_value = self._apply_redaction(value, pii_type, redaction_method, redaction_char)
            
            # Replace in text
            redacted_text = redacted_text[:start] + redacted_value + redacted_text[end:]
        
        # Reverse back to original order
        detections.reverse()
        
        logger.debug(f"Redacted {len(detections)} PII instances")
        return redacted_text, detections
    
    def _apply_redaction(
        self,
        value: str,
        pii_type: str,
        method: str,
        redaction_char: str
    ) -> str:
        """
        Apply specific redaction method to a PII value.
        
        Args:
            value: PII value to redact
            pii_type: Type of PII
            method: Redaction method (mask_all, mask_partial, mask_middle)
            redaction_char: Character for masking
            
        Returns:
            Redacted value
        """
        if method == 'mask_all':
            return redaction_char * len(value)
        
        elif method == 'mask_partial':
            if pii_type == 'email':
                # Mask: user***@example.com
                if '@' in value:
                    local, domain = value.split('@', 1)
                    if len(local) > 2:
                        return local[:2] + redaction_char * 3 + '@' + domain
                return value
            else:
                # Show first 2 and last 2 characters
                if len(value) > 6:
                    return value[:2] + redaction_char * (len(value) - 4) + value[-2:]
                return redaction_char * len(value)
        
        elif METHOD == 'mask_middle':
            # Show first and last parts, mask middle
            if len(value) <= 4:
                return redaction_char * len(value)
            
            show_length = len(value) // 4
            if pii_type in ['phone', 'aadhaar']:
                # Keep structure for readability
                if ' ' in value or '-' in value:
                    parts = re.split(r'([\s-])', value)
                    masked_parts = []
                    for i, part in enumerate(parts):
                        if i % 2 == 0 and part:  # Actual number parts
                            if len(part) > 2:
                                masked_parts.append(redaction_char * len(part))
                            else:
                                masked_parts.append(part)
                        else:
                            masked_parts.append(part)
                    return ''.join(masked_parts)
            
            return value[:show_length] + redaction_char * (len(value) - 2 * show_length) + value[-show_length:]
        
        return redaction_char * len(value)
    
    def has_pii(self, text: str, min_sensitivity: str = 'medium') -> bool:
        """
        Check if text contains PII above minimum sensitivity.
        
        Args:
            text: Text to check
            min_sensitivity: Minimum sensitivity level (low, medium, high)
            
        Returns:
            True if PII detected above threshold
        """
        detections = self.detect(text)
        
        sensitivity_levels = {'low': 1, 'medium': 2, 'high': 3}
        min_level = sensitivity_levels.get(min_sensitivity, 2)
        
        for detection in detections:
            detection_level = sensitivity_levels.get(detection['sensitivity'], 2)
            if detection_level >= min_level:
                return True
        
        return False
