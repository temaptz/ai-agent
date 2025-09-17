"""
Конфигурация для универсального ИИ-агента
"""
import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Настройки приложения"""
    
    # Ollama настройки
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = 'PetrosStav/gemma3-tools:12b' # "gemma3-abliterated:12b"
    
    # Настройки поиска
    duckduckgo_max_results: int = 10
    request_timeout: int = 30
    
    # Настройки агента
    max_iterations: int = 5
    max_aspects_per_question: int = 10
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Глобальный экземпляр настроек
settings = Settings()