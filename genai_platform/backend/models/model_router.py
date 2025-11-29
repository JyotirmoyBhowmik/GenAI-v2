"""
GenAI Platform - Model Router
Routes queries to appropriate models based on context and configuration
"""

from typing import Dict, Any, Optional
from loguru import logger

from backend.models.base_model import BaseModelAdapter, DummyModelAdapter, ModelResponse


class ModelRouter:
    """
    Routes queries to appropriate AI models.
    Selects models based on persona, user preferences, and availability.
    """
    
    def __init__(self):
        """Initialize model router."""
        from backend.config_manager import get_config
        self.config = get_config()
        
        # Model registry (model_id -> adapter instance)
        self.model_adapters: Dict[str, BaseModelAdapter] = {}
        
        # Initialize adapters
        self._initialize_adapters()
        
        logger.info(f"ModelRouter initialized with {len(self.model_adapters)} adapters")
    
    def _initialize_adapters(self):
        """Initialize model adapters for all enabled models."""
        models = self.config.list_models(enabled_only=True)
        
        for model_config in models:
            model_id = model_config['id']
            
            try:
                adapter = self._create_adapter(model_config)
                if adapter.is_available():
                    self.model_adapters[model_id] = adapter
                    logger.debug(f"Loaded adapter for: {model_id}")
                else:
                    logger.warning(f"Model {model_id} is not available")
            except Exception as e:
                logger.error(f"Error loading adapter for {model_id}: {e}")
    
    def _create_adapter(self, model_config: Dict[str, Any]) -> BaseModelAdapter:
        """
        Create model adapter based on provider.
        
        Args:
            model_config: Model configuration
            
        Returns:
            Model adapter instance
        """
        provider = model_config['provider']
        model_type = model_config.get('type', 'cloud')
        
        # For now, use dummy adapters
        # TODO: Implement real adapters when API keys are configured
        
        # Try to import real adapter, fall back to dummy
        adapter = None
        
        if provider == 'openai':
            try:
                from backend.models.cloud.openai_adapter import OpenAIAdapter
                adapter = OpenAIAdapter(model_config)
            except:
                logger.debug(f"OpenAI adapter not available, using dummy for {model_config['id']}")
        
        elif provider == 'google':
            try:
                from backend.models.cloud.gemini_adapter import GeminiAdapter
                adapter = GeminiAdapter(model_config)
            except:
                logger.debug(f"Gemini adapter not available, using dummy for {model_config['id']}")
        
        elif provider == 'anthropic':
            try:
                from backend.models.cloud.claude_adapter import ClaudeAdapter
                adapter = ClaudeAdapter(model_config)
            except:
                logger.debug(f"Claude adapter not available, using dummy for {model_config['id']}")
        
        elif provider == 'ollama':
            try:
                from backend.models.local.ollama_adapter import OllamaAdapter
                adapter = OllamaAdapter(model_config)
            except:
                logger.debug(f"Ollama adapter not available, using dummy for {model_config['id']}")
        
        # Fall back to dummy adapter
        if adapter is None:
            adapter = DummyModelAdapter(model_config)
        
        return adapter
    
    def route(
        self,
        prompt: str,
        model_id: Optional[str] = None,
        persona_id: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> ModelResponse:
        """
        Route query to appropriate model and get response.
        
        Args:
            prompt: User prompt/query
            model_id: Specific model ID to use (optional)
            persona_id: Persona ID for context (optional)
            context: Additional context
            
        Returns:
            ModelResponse from selected model
        """
        # Select model
        selected_model_id = self._select_model(model_id, persona_id)
        
        if selected_model_id not in self.model_adapters:
            logger.error(f"Model {selected_model_id} not available")
            # Fall back to first available model
            if self.model_adapters:
                selected_model_id = list(self.model_adapters.keys())[0]
                logger.info(f"Falling back to {selected_model_id}")
            else:
                raise ValueError("No models available")
        
        adapter = self.model_adapters[selected_model_id]
        
        # Build full prompt with persona context
        full_prompt = self._build_prompt(prompt, persona_id, context)
        
        # Generate response
        logger.info(f"Routing to model: {selected_model_id}")
        response = adapter.generate(full_prompt)
        
        return response
    
    def _select_model(
        self,
        model_id: Optional[str],
        persona_id: Optional[str]
    ) -> str:
        """
        Select model based on provided ID or persona preferences.
        
        Args:
            model_id: Explicit model ID
            persona_id: Persona ID for preferences
            
        Returns:
            Selected model ID
        """
        # If model explicitly specified, use it
        if model_id:
            return model_id
        
        # Otherwise, use persona preferences
        if persona_id:
            persona = self.config.get_persona(persona_id)
            if persona:
                allowed_models = persona.get('allowed_models', [])
                # Select first available allowed model
                for allowed_model in allowed_models:
                    if allowed_model in self.model_adapters:
                        return allowed_model
        
        # Fall back to default model from config
        default_model = self.config.get('app', 'models', 'default_cloud_model', default='gpt-4')
        
        if default_model in self.model_adapters:
            return default_model
        
        # Last resort: first available model
        if self.model_adapters:
            return list(self.model_adapters.keys())[0]
        
        raise ValueError("No models available")
    
    def _build_prompt(
        self,
        user_prompt: str,
        persona_id: Optional[str],
        context: Optional[Dict[str, Any]]
    ) -> str:
        """
        Build full prompt with persona and context.
        
        Args:
            user_prompt: User's query
            persona_id: Persona ID
            context: Additional context
            
        Returns:
            Full prompt string
        """
        parts = []
        
        # Add persona system prompt
        if persona_id:
            persona = self.config.get_persona(persona_id)
            if persona:
                system_prompt = persona.get('system_prompt', '')
                if system_prompt:
                    parts.append(f"SYSTEM: {system_prompt}\n")
        
        # Add context if available
        if context:
            division_id = context.get('division_id')
            department_id = context.get('department_id')
            
            if division_id or department_id:
                parts.append(f"CONTEXT: Division={division_id}, Department={department_id}\n")
        
        # Add user prompt
        parts.append(f"USER: {user_prompt}")
        
        return '\n'.join(parts)
    
    def get_available_models(self) -> list:
        """Get list of available model IDs."""
        return list(self.model_adapters.keys())
