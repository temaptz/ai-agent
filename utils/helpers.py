"""
Вспомогательные функции для универсального ИИ-агента
"""
import json
import re
from typing import Dict, List, Any, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


def clean_text(text: str, max_length: int = 1000) -> str:
    """
    Очищает и обрезает текст до указанной длины
    
    Args:
        text: Исходный текст
        max_length: Максимальная длина текста
        
    Returns:
        Очищенный текст
    """
    if not text:
        return ""
    
    # Удаляем лишние пробелы и переносы строк
    text = re.sub(r'\s+', ' ', text.strip())
    
    # Обрезаем до максимальной длины
    if len(text) > max_length:
        text = text[:max_length] + "..."
    
    return text


def extract_keywords(text: str, min_length: int = 3) -> List[str]:
    """
    Извлекает ключевые слова из текста
    
    Args:
        text: Исходный текст
        min_length: Минимальная длина ключевого слова
        
    Returns:
        Список ключевых слов
    """
    if not text:
        return []
    
    # Удаляем знаки препинания и приводим к нижнему регистру
    words = re.findall(r'\b\w+\b', text.lower())
    
    # Фильтруем по длине и убираем стоп-слова
    stop_words = {
        'и', 'в', 'на', 'с', 'по', 'для', 'от', 'до', 'из', 'к', 'у', 'о', 'об',
        'что', 'как', 'где', 'когда', 'почему', 'зачем', 'который', 'которая',
        'которое', 'которые', 'это', 'эта', 'этот', 'эти', 'такой', 'такая',
        'такое', 'такие', 'его', 'её', 'их', 'мой', 'моя', 'моё', 'мои',
        'твой', 'твоя', 'твоё', 'твои', 'наш', 'наша', 'наше', 'наши',
        'ваш', 'ваша', 'ваше', 'ваши', 'он', 'она', 'оно', 'они', 'мы', 'вы',
        'я', 'ты', 'он', 'она', 'оно', 'мы', 'вы', 'они', 'себя', 'себе',
        'собой', 'собою', 'свой', 'своя', 'своё', 'свои', 'сам', 'сама',
        'само', 'сами', 'тот', 'та', 'то', 'те', 'этот', 'эта', 'это', 'эти'
    }
    
    keywords = [
        word for word in words 
        if len(word) >= min_length and word not in stop_words
    ]
    
    # Возвращаем уникальные ключевые слова
    return list(set(keywords))


def format_search_results(results: List[Dict[str, Any]]) -> str:
    """
    Форматирует результаты поиска для отображения
    
    Args:
        results: Список результатов поиска
        
    Returns:
        Отформатированная строка
    """
    if not results:
        return "Результаты поиска не найдены."
    
    formatted = []
    for i, result in enumerate(results[:5], 1):  # Показываем только первые 5
        title = result.get('title', 'Без заголовка')
        url = result.get('url', '')
        description = result.get('description', '')
        
        formatted.append(f"{i}. {title}")
        if url:
            formatted.append(f"   URL: {url}")
        if description:
            desc = clean_text(description, 200)
            formatted.append(f"   Описание: {desc}")
        formatted.append("")
    
    return "\n".join(formatted)


def validate_question(question: str) -> Dict[str, Any]:
    """
    Валидирует вопрос и возвращает информацию о нем
    
    Args:
        question: Вопрос для валидации
        
    Returns:
        Словарь с результатами валидации
    """
    result = {
        "is_valid": True,
        "length": len(question),
        "word_count": len(question.split()),
        "has_question_mark": question.strip().endswith('?'),
        "language": "unknown",
        "issues": []
    }
    
    if not question or not question.strip():
        result["is_valid"] = False
        result["issues"].append("Пустой вопрос")
        return result
    
    if len(question) < 10:
        result["issues"].append("Слишком короткий вопрос")
    
    if len(question) > 1000:
        result["issues"].append("Слишком длинный вопрос")
    
    if result["word_count"] < 3:
        result["issues"].append("Слишком мало слов")
    
    # Простое определение языка
    cyrillic_chars = len(re.findall(r'[а-яё]', question.lower()))
    latin_chars = len(re.findall(r'[a-z]', question.lower()))
    
    if cyrillic_chars > latin_chars:
        result["language"] = "russian"
    elif latin_chars > cyrillic_chars:
        result["language"] = "english"
    else:
        result["language"] = "mixed"
    
    return result


def create_summary_report(results: Dict[str, Any]) -> str:
    """
    Создает краткий отчет по результатам анализа
    
    Args:
        results: Результаты анализа от агента
        
    Returns:
        Краткий отчет в текстовом формате
    """
    if "error" in results:
        return f"❌ Ошибка анализа: {results['error']}"
    
    report_parts = []
    
    # Заголовок
    question = results.get("original_question", "Неизвестный вопрос")
    report_parts.append(f"📝 ВОПРОС: {question}")
    report_parts.append("")
    
    # Статистика
    processed_aspects = results.get("processed_aspects", [])
    research_data = results.get("research_data", [])
    total_sources = sum(len(aspect.get("research_data", [])) for aspect in research_data)
    iteration_count = results.get("iteration_count", 0)
    
    report_parts.append("📊 СТАТИСТИКА:")
    report_parts.append(f"   • Обработано аспектов: {len(processed_aspects)}")
    report_parts.append(f"   • Исследовано источников: {total_sources}")
    report_parts.append(f"   • Итераций: {iteration_count}")
    report_parts.append("")
    
    # Итоговые выводы
    final_insights = results.get("final_insights", {})
    if isinstance(final_insights, dict):
        if "summary" in final_insights:
            report_parts.append("💡 КРАТКИЙ ОТВЕТ:")
            report_parts.append(f"   {final_insights['summary']}")
            report_parts.append("")
        
        if "key_conclusions" in final_insights:
            report_parts.append("🎯 КЛЮЧЕВЫЕ ВЫВОДЫ:")
            for conclusion in final_insights["key_conclusions"]:
                report_parts.append(f"   • {conclusion}")
            report_parts.append("")
        
        if "confidence" in final_insights:
            confidence_emoji = {
                "высокий": "🟢",
                "средний": "🟡",
                "низкий": "🔴"
            }.get(final_insights["confidence"], "❓")
            report_parts.append(f"{confidence_emoji} Уровень уверенности: {final_insights['confidence']}")
    
    return "\n".join(report_parts)


def save_results_to_file(results: Dict[str, Any], filename: str = None) -> str:
    """
    Сохраняет результаты анализа в файл
    
    Args:
        results: Результаты анализа
        filename: Имя файла (если не указано, генерируется автоматически)
        
    Returns:
        Путь к сохраненному файлу
    """
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        question = results.get("original_question", "unknown")
        safe_question = re.sub(r'[^\w\s-]', '', question)[:30]
        filename = f"analysis_{timestamp}_{safe_question}.json"
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        logger.info(f"Результаты сохранены в файл: {filename}")
        return filename
        
    except Exception as e:
        logger.error(f"Ошибка сохранения файла {filename}: {e}")
        return ""


def load_results_from_file(filename: str) -> Optional[Dict[str, Any]]:
    """
    Загружает результаты анализа из файла
    
    Args:
        filename: Путь к файлу
        
    Returns:
        Результаты анализа или None при ошибке
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            results = json.load(f)
        
        logger.info(f"Результаты загружены из файла: {filename}")
        return results
        
    except Exception as e:
        logger.error(f"Ошибка загрузки файла {filename}: {e}")
        return None


def estimate_processing_time(question: str) -> int:
    """
    Оценивает примерное время обработки вопроса в секундах
    
    Args:
        question: Вопрос для анализа
        
    Returns:
        Оценочное время в секундах
    """
    word_count = len(question.split())
    char_count = len(question)
    
    # Базовая оценка: 30 секунд + 2 секунды на слово + 0.1 секунды на символ
    base_time = 30
    word_time = word_count * 2
    char_time = char_count * 0.1
    
    estimated_time = int(base_time + word_time + char_time)
    
    # Ограничиваем максимальное время
    return min(estimated_time, 300)  # Максимум 5 минут