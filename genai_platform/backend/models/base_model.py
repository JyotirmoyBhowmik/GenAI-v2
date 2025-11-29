"""
GenAI Platform - Base Model Adapter
Abstract base class for all model adapters
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any, Iterator
from dataclasses import dataclass
from loguru import logger


@dataclass
class ModelResponse:
    """Standard response format from models."""
    text: str
    model_id: str
    provider: str
    tokens_used: int
    cost: float
    metadata: Dict[str, Any]


class BaseModelAdapter(ABC):
    """
    Abstract base class for all model adapters.
    Provides a unified interface for different AI models.
    """
    
    def __init__(self, model_config: Dict[str, Any]):
        """
        Initialize model adapter.
        
        Args:
            model_config: Model configuration from catalog
        """
        self.model_config = model_config
        self.model_id = model_config['id']
        self.model_name = model_config['model_name']
        self.provider = model_config['provider']
        self.max_tokens = model_config.get('max_tokens', 4096)
        self.pricing = model_config.get('pricing', {})
        
        logger.debug(f"Initialized {self.__class__.__name__} for {self.model_id}")
    
    @abstractmethod
    def generate(
        self,
        prompt: str,
        max_tokens: Optional[int] = None,
        temperature: float = 0.7,
        **kwargs
    ) -> ModelResponse:
        """
        Generate text from prompt.
        
        Args:
            prompt: Input prompt
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            **kwargs: Model-specific parameters
            
        Returns:
            ModelResponse object
        """
        pass
    
    @abstractmethod
    def stream_generate(
        self,
        prompt: str,
        max_tokens: Optional[int] = None,
        temperature: float = 0.7,
        **kwargs
    ) -> Iterator[str]:
        """
        Stream generated text.
        
        Args:
            prompt: Input prompt
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            **kwargs: Model-specific parameters
            
        Yields:
            Text chunks
        """
        pass
    
    def calculate_cost(self, input_tokens: int, output_tokens: int) -> float:
        """
        Calculate cost based on token usage.
        
        Args:
            input_tokens: Number of input tokens
            output_tokens: Number of output tokens
            
        Returns:
            Cost in USD
        """
        input_cost_per_1k = self.pricing.get('input_per_1k_tokens', 0.0)
        output_cost_per_1k = self.pricing.get('output_per_1k_tokens', 0.0)
        
        input_cost = (input_tokens / 1000) * input_cost_per_1k
        output_cost = (output_tokens / 1000) * output_cost_per_1k
        
        return input_cost + output_cost
    
    def is_available(self) -> bool:
        """
        Check if model is available/accessible.
        
        Returns:
            True if model can be used
        """
        # Default implementation - can be overridden
        return self.model_config.get('enabled', True)


class DummyModelAdapter(BaseModelAdapter):
    """
    Dummy model adapter for testing and placeholder.
    Returns canned responses without calling actual models.
    """
    
    def generate(
        self,
        prompt: str,
        max_tokens: Optional[int] = None,
        temperature: float = 0.7,
        **kwargs
    ) -> ModelResponse:
        """Generate dummy response."""
        
        response_text = f"""**Model**: {self.model_id} ({self.provider})

**Prompt Received**: {prompt[:100]}...

**Response**: This is a placeholder response from the model adapter. Full integration with {self.provider} will be completed in the next phase.

**Status**: Model adapter framework is operational. Connect your API keys in the .env file to enable live model responses.

**Next Steps**:
1. Add API keys to .env file
2. Model adapters will automatically connect
3. Full RAG pipeline integration coming soon
"""
        
        # Estimate tokens (very rough)
        input_tokens = len(prompt.split())
        output_tokens = len(response_text.split())
        
        cost = self.calculate_cost(input_tokens, output_tokens)
        
        return ModelResponse(
            text=response_text,
            model_id=self.model_id,
            provider=self.provider,
            tokens_used=input_tokens + output_tokens,
            cost=cost,
            metadata={
                'temperature': temperature,
                'max_tokens': max_tokens or self.max_tokens,
                'dummy': True
            }
        )
    
    def stream_generate(
        self,
        prompt: str,
        max_tokens: Optional[int] = None,
        temperature: float = 0.7,
        **kwargs
    ) -> Iterator[str]:
        """Stream dummy response."""
        response = self.generate(prompt, max_tokens, temperature, **kwargs)
        
        # Yield in chunks
        words = response.text.split()
        chunk_size = 5
        
        for i in range(0, len(words), chunk_size):
            chunk = ' '.join(words[i:i + chunk_size]) + ' '
            yield chunk
