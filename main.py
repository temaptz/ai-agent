"""
Главный файл для запуска универсального ИИ-агента
"""
import os
import sys
import json
from typing import Optional
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

# Добавляем текущую директорию в путь
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agent.universal_agent import UniversalAgent
from config import settings
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def print_results(results: dict) -> None:
    """
    Красиво выводит результаты анализа
    
    Args:
        results: Результаты анализа от агента
    """
    print("\n" + "="*80)
    print("РЕЗУЛЬТАТЫ АНАЛИЗА")
    print("="*80)
    
    if "error" in results:
        print(f"❌ Ошибка: {results['error']}")
        return
    
    original_question = results.get("original_question", "")
    print(f"📝 ВОПРОС: {original_question}")
    print()
    
    # Анализ мотивации
    analysis_results = results.get("analysis_results", {})
    if analysis_results and "motivation" in analysis_results:
        print("🎯 МОТИВАЦИЯ И КОНТЕКСТ:")
        print(f"   {analysis_results['motivation']}")
        print()
    
    # Обработанные аспекты
    processed_aspects = results.get("processed_aspects", [])
    if processed_aspects:
        print("🔍 ОБРАБОТАННЫЕ АСПЕКТЫ:")
        for i, aspect in enumerate(processed_aspects, 1):
            print(f"   {i}. {aspect}")
        print()
    
    # Итоговые выводы
    final_insights = results.get("final_insights", {})
    if final_insights and isinstance(final_insights, dict):
        print("💡 ИТОГОВЫЕ ВЫВОДЫ:")
        
        if "summary" in final_insights:
            print(f"   📋 Краткий ответ: {final_insights['summary']}")
            print()
        
        if "key_conclusions" in final_insights:
            print("   🎯 Ключевые выводы:")
            for conclusion in final_insights["key_conclusions"]:
                print(f"      • {conclusion}")
            print()
        
        if "insights" in final_insights:
            print("   💭 Инсайты:")
            for insight in final_insights["insights"]:
                print(f"      • {insight}")
            print()
        
        if "recommendations" in final_insights:
            print("   📚 Рекомендации для дальнейшего изучения:")
            for rec in final_insights["recommendations"]:
                print(f"      • {rec}")
            print()
        
        if "confidence" in final_insights:
            confidence_emoji = {
                "высокий": "🟢",
                "средний": "🟡", 
                "низкий": "🔴"
            }.get(final_insights["confidence"], "❓")
            print(f"   {confidence_emoji} Уровень уверенности: {final_insights['confidence']}")
            print()
    
    # Статистика
    research_data = results.get("research_data", [])
    total_sources = sum(len(aspect.get("research_data", [])) for aspect in research_data)
    
    print("📊 СТАТИСТИКА:")
    print(f"   • Обработано аспектов: {len(processed_aspects)}")
    print(f"   • Исследовано источников: {total_sources}")
    print(f"   • Итераций: {results.get('iteration_count', 0)}")
    print()


def interactive_mode() -> None:
    """Интерактивный режим работы с агентом"""
    print("🤖 Универсальный ИИ-агент запущен!")
    print("Введите ваш вопрос для всестороннего анализа.")
    print("Для выхода введите 'quit' или 'exit'.")
    print("-" * 60)
    
    agent = UniversalAgent()
    
    while True:
        try:
            question = input("\n❓ Ваш вопрос: ").strip()
            
            if question.lower() in ['quit', 'exit', 'выход']:
                print("👋 До свидания!")
                break
            
            if not question:
                print("⚠️  Пожалуйста, введите вопрос.")
                continue
            
            print(f"\n🔄 Анализирую вопрос: '{question}'")
            print("Это может занять некоторое время...")
            
            results = agent.process_question(question)
            print_results(results)
            
        except KeyboardInterrupt:
            print("\n\n👋 До свидания!")
            break
        except Exception as e:
            logger.error(f"Ошибка в интерактивном режиме: {e}")
            print(f"❌ Произошла ошибка: {e}")


def process_single_question(question: str) -> None:
    """
    Обрабатывает один вопрос и выводит результаты
    
    Args:
        question: Вопрос для анализа
    """
    print(f"🔄 Анализирую вопрос: '{question}'")
    print("Это может занять некоторое время...")
    
    agent = UniversalAgent()
    results = agent.process_question(question)
    print_results(results)


def main():
    """Главная функция"""
    print("🚀 Инициализация универсального ИИ-агента...")
    
    # Проверяем настройки
    print(f"📡 Ollama URL: {settings.ollama_base_url}")
    print(f"🧠 Модель: {settings.ollama_model}")
    print(f"🔍 Максимум результатов поиска: {settings.duckduckgo_max_results}")
    print()
    
    # Проверяем аргументы командной строки
    if len(sys.argv) > 1:
        # Обрабатываем вопрос из командной строки
        question = " ".join(sys.argv[1:])
        process_single_question(question)
    else:
        # Запускаем интерактивный режим
        interactive_mode()


if __name__ == "__main__":
    main()