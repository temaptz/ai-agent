"""
Пакет инструментов для универсального ИИ-агента
"""

from .search_tools import web_search_tool, url_content_tool, WebSearchTool, URLContentTool

__all__ = [
    'web_search_tool',
    'url_content_tool', 
    'WebSearchTool',
    'URLContentTool'
]