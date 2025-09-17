"""
Инструменты для поиска информации в интернете
"""
import requests
from typing import List, Dict, Any, Optional
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS
import logging
from config import settings

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WebSearchTool:
    """Инструмент для поиска в интернете с использованием DuckDuckGo"""
    
    def __init__(self, max_results: int = None):
        """
        Инициализация инструмента поиска
        
        Args:
            max_results: Максимальное количество результатов поиска
        """
        self.max_results = max_results or settings.duckduckgo_max_results
        self.ddgs = DDGS()
    
    def search(self, query: str, region: str = "ru-ru") -> List[Dict[str, Any]]:
        """
        Выполняет поиск в интернете по заданному запросу
        
        Args:
            query: Поисковый запрос
            region: Регион для поиска (по умолчанию ru-ru)
            
        Returns:
            Список результатов поиска с заголовками, ссылками и описаниями
        """
        try:
            logger.info(f"Выполняю поиск по запросу: {query}")
            
            results = self.ddgs.text(
                query, 
                region=region, 
                max_results=self.max_results
            )
            
            # Преобразуем результаты в удобный формат
            formatted_results = []
            for result in results:
                formatted_results.append({
                    "title": result.get("title", ""),
                    "url": result.get("href", ""),
                    "description": result.get("body", ""),
                    "source": "DuckDuckGo"
                })
            
            logger.info(f"Найдено {len(formatted_results)} результатов")
            return formatted_results
            
        except Exception as e:
            logger.error(f"Ошибка при поиске: {e}")
            return []
    
    def search_news(self, query: str, region: str = "ru-ru") -> List[Dict[str, Any]]:
        """
        Выполняет поиск новостей по заданному запросу
        
        Args:
            query: Поисковый запрос
            region: Регион для поиска
            
        Returns:
            Список новостных результатов
        """
        try:
            logger.info(f"Выполняю поиск новостей по запросу: {query}")
            
            results = self.ddgs.news(
                query,
                region=region,
                max_results=self.max_results
            )
            
            formatted_results = []
            for result in results:
                formatted_results.append({
                    "title": result.get("title", ""),
                    "url": result.get("url", ""),
                    "description": result.get("body", ""),
                    "date": result.get("date", ""),
                    "source": result.get("source", ""),
                    "type": "news"
                })
            
            logger.info(f"Найдено {len(formatted_results)} новостных результатов")
            return formatted_results
            
        except Exception as e:
            logger.error(f"Ошибка при поиске новостей: {e}")
            return []


class URLContentTool:
    """Инструмент для загрузки и анализа содержимого веб-страниц"""
    
    def __init__(self, timeout: int = None):
        """
        Инициализация инструмента загрузки URL
        
        Args:
            timeout: Таймаут для HTTP-запросов в секундах
        """
        self.timeout = timeout or settings.request_timeout
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def load_url(self, url: str) -> Dict[str, Any]:
        """
        Загружает содержимое веб-страницы по URL
        
        Args:
            url: URL для загрузки
            
        Returns:
            Словарь с содержимым страницы, заголовком и метаданными
        """
        try:
            logger.info(f"Загружаю содержимое URL: {url}")
            
            response = requests.get(
                url, 
                headers=self.headers, 
                timeout=self.timeout,
                allow_redirects=True
            )
            response.raise_for_status()
            
            # Парсим HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Извлекаем основную информацию
            title = soup.find('title')
            title_text = title.get_text().strip() if title else ""
            
            # Удаляем скрипты и стили
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Извлекаем основной текст
            text_content = soup.get_text()
            
            # Очищаем текст
            lines = (line.strip() for line in text_content.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            # Извлекаем мета-описание
            meta_description = soup.find('meta', attrs={'name': 'description'})
            description = meta_description.get('content', '') if meta_description else ""
            
            # Извлекаем ключевые слова
            meta_keywords = soup.find('meta', attrs={'name': 'keywords'})
            keywords = meta_keywords.get('content', '') if meta_keywords else ""
            
            result = {
                "url": url,
                "title": title_text,
                "description": description,
                "keywords": keywords,
                "content": text[:5000],  # Ограничиваем размер контента
                "status_code": response.status_code,
                "content_length": len(text),
                "success": True
            }
            
            logger.info(f"Успешно загружено содержимое URL: {url}")
            return result
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Ошибка HTTP при загрузке {url}: {e}")
            return {
                "url": url,
                "error": str(e),
                "success": False
            }
        except Exception as e:
            logger.error(f"Неожиданная ошибка при загрузке {url}: {e}")
            return {
                "url": url,
                "error": str(e),
                "success": False
            }
    
    def extract_links(self, url: str) -> List[Dict[str, str]]:
        """
        Извлекает все ссылки с веб-страницы
        
        Args:
            url: URL для анализа
            
        Returns:
            Список ссылок с их текстом и атрибутами
        """
        try:
            logger.info(f"Извлекаю ссылки с URL: {url}")
            
            response = requests.get(
                url, 
                headers=self.headers, 
                timeout=self.timeout
            )
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            links = []
            
            for link in soup.find_all('a', href=True):
                link_text = link.get_text().strip()
                link_url = link['href']
                
                # Преобразуем относительные ссылки в абсолютные
                if link_url.startswith('/'):
                    from urllib.parse import urljoin
                    link_url = urljoin(url, link_url)
                
                if link_text and link_url:
                    links.append({
                        "text": link_text,
                        "url": link_url
                    })
            
            logger.info(f"Найдено {len(links)} ссылок")
            return links
            
        except Exception as e:
            logger.error(f"Ошибка при извлечении ссылок с {url}: {e}")
            return []


# Создаем глобальные экземпляры инструментов
web_search_tool = WebSearchTool()
url_content_tool = URLContentTool()