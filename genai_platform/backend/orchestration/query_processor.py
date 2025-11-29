"""
GenAI Platform - Query Processor
Main orchestration engine for processing user queries
"""

from typing import Dict, Any, Optional
from loguru import logger
from dataclasses import dataclass

from backend.models.model_router import ModelRouter
from backend.models.base_model import ModelResponse
from backend.security.rbac import RBACManager
from backend.security.pii_detector import PIIDetector


@dataclass
class QueryContext:
    """Context for query processing."""
    user_id: str
    division_id: str
    department_id: str
    persona_id: str
    model_id: Optional[str] = None
    role_id: str = ""


@dataclass
class ProcessedResponse:
    """Processed query response."""
    text: str
    model_id: str
    provider: str
    tokens_used: int
    cost: float
    citations: list
    metadata: Dict[str, Any]
    redacted_pii: list


class QueryProcessor:
    """
    Main query processing orchestrator.
    Handles authorization, PII detection, model routing, and response processing.
    """
    
    def __init__(self):
        """Initialize query processor."""
        self.model_router = ModelRouter()
        self.rbac = RBACManager()
        self.pii_detector = PIIDetector()
        
        logger.info("QueryProcessor initialized")
    
    def process(
        self,
        query: str,
        context: QueryContext
    ) -> ProcessedResponse:
        """
        Process user query end-to-end.
        
        Args:
            query: User query text
            context: Query context (user, division, persona, etc.)
            
        Returns:
            ProcessedResponse with model output and metadata
        """
        logger.info(f"Processing query for user {context.user_id}")
        
        # Step 1: Authorization check
        if not self._authorize(context):
            logger.warning(f"Authorization failed for user {context.user_id}")
            return self._create_error_response(
                "Authorization failed. You don't have permission to access this division/department."
            )
        
        # Step 2: PII detection in query
        if self.pii_detector.has_pii(query, min_sensitivity='medium'):
            logger.info("PII detected in query")
            # For now, just log - in production, might redact or warn user
        
        # Step 3: Build context for model
        model_context = {
            'division_id': context.division_id,
            'department_id': context.department_id,
            'user_id': context.user_id
        }
        
        # Step 4: Route to model and get response
        try:
            model_response: ModelResponse = self.model_router.route(
                prompt=query,
                model_id=context.model_id,
                persona_id=context.persona_id,
                context=model_context
            )
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return self._create_error_response(f"Error generating response: {str(e)}")
        
        # Step 5: PII detection and redaction in response
        redacted_text, pii_detections = self.pii_detector.redact(model_response.text)
        
        if pii_detections:
            logger.warning(f"Redacted {len(pii_detections)} PII instances from response")
        
        # Step 6: Build processed response
        processed = ProcessedResponse(
            text=redacted_text,
            model_id=model_response.model_id,
            provider=model_response.provider,
            tokens_used=model_response.tokens_used,
            cost=model_response.cost,
            citations=[],  # TODO: Add RAG citations
            metadata=model_response.metadata,
            redacted_pii=pii_detections
        )
        
        logger.info(f"Query processed successfully (model={model_response.model_id}, tokens={model_response.tokens_used}, cost=${model_response.cost:.4f})")
        
        return processed
    
    def _authorize(self, context: QueryContext) -> bool:
        """
        Check if user is authorized for the query.
        
        Args:
            context: Query context
            
        Returns:
            True if authorized
        """
        # Check division access
        can_access = self.rbac.can_access_division(
            role_id=context.role_id,
            division_id=context.division_id,
            user_division=context.division_id  # In real impl, get from user record
        )
        
        if not can_access:
            return False
        
        # Check department access
        can_access = self.rbac.can_access_department(
            role_id=context.role_id,
            department_id=context.department_id,
            user_department=context.department_id,  # In real impl, get from user record
            user_division=context.division_id,
            target_division=context.division_id
        )
        
        return can_access
    
    def _create_error_response(self, error_message: str) -> ProcessedResponse:
        """Create error response."""
        return ProcessedResponse(
            text=f"❌ Error: {error_message}",
            model_id="error",
            provider="system",
            tokens_used=0,
            cost=0.0,
            citations=[],
            metadata={'error': True},
            redacted_pii=[]
        )
