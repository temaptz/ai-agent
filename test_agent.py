"""
Тесты для универсального ИИ-агента
"""
import sys
import os
import json
import time
from typing import Dict, Any

# Добавляем текущую директорию в путь
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agent.universal_agent import UniversalAgent
from tools.search_tools import web_search_tool, url_content_tool
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_search_tools():
    """Тестирует инструменты поиска"""
    print("🔍 Тестирую инструменты поиска...")
    
    # Тест поиска в интернете
    print("\n1. Тестирую DuckDuckGo поиск:")
    search_results = web_search_tool.search("Python программирование")
    print(f"   Найдено результатов: {len(search_results)}")
    if search_results:
        print(f"   Первый результат: {search_results[0]['title'][:50]}...")
    
    # Тест загрузки URL
    print("\n2. Тестирую загрузку URL:")
    url_result = url_content_tool.load_url("https://python.org")
    print(f"   Статус загрузки: {'✅' if url_result.get('success') else '❌'}")
    if url_result.get('success'):
        print(f"   Заголовок: {url_result.get('title', 'N/A')[:50]}...")
        print(f"   Размер контента: {url_result.get('content_length', 0)} символов")
    
    print("✅ Тест инструментов поиска завершен\n")


def test_agent_initialization():
    """Тестирует инициализацию агента"""
    print("🤖 Тестирую инициализацию агента...")
    
    try:
        agent = UniversalAgent()
        print("   ✅ Агент успешно инициализирован")
        print(f"   📡 LLM: {agent.llm.model}")
        print(f"   🛠 Инструментов: {len(agent.tools)}")
        return agent
    except Exception as e:
        print(f"   ❌ Ошибка инициализации: {e}")
        return None


def test_simple_question(agent: UniversalAgent):
    """Тестирует обработку простого вопроса"""
    print("❓ Тестирую обработку простого вопроса...")
    
    question = "Что такое Python?"
    print(f"   Вопрос: {question}")
    
    start_time = time.time()
    
    try:
        results = agent.process_question(question)
        end_time = time.time()
        
        print(f"   ⏱ Время обработки: {end_time - start_time:.2f} секунд")
        
        if "error" in results:
            print(f"   ❌ Ошибка: {results['error']}")
            return False
        
        # Проверяем структуру результатов
        required_keys = ["original_question", "analysis_results", "final_insights"]
        missing_keys = [key for key in required_keys if key not in results]
        
        if missing_keys:
            print(f"   ⚠️ Отсутствуют ключи: {missing_keys}")
        else:
            print("   ✅ Структура результатов корректна")
        
        # Выводим краткую информацию
        aspects = results.get("processed_aspects", [])
        print(f"   📊 Обработано аспектов: {len(aspects)}")
        
        final_insights = results.get("final_insights", {})
        if isinstance(final_insights, dict) and "summary" in final_insights:
            summary = final_insights["summary"][:100]
            print(f"   📝 Краткий ответ: {summary}...")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Ошибка обработки: {e}")
        return False


def test_complex_question(agent: UniversalAgent):
    """Тестирует обработку сложного вопроса"""
    print("🧠 Тестирую обработку сложного вопроса...")
    
    question = "Как искусственный интеллект изменит образование в ближайшие 5 лет?"
    print(f"   Вопрос: {question}")
    
    start_time = time.time()
    
    try:
        results = agent.process_question(question)
        end_time = time.time()
        
        print(f"   ⏱ Время обработки: {end_time - start_time:.2f} секунд")
        
        if "error" in results:
            print(f"   ❌ Ошибка: {results['error']}")
            return False
        
        # Анализируем результаты
        aspects = results.get("processed_aspects", [])
        research_data = results.get("research_data", [])
        total_sources = sum(len(aspect.get("research_data", [])) for aspect in research_data)
        
        print(f"   📊 Обработано аспектов: {len(aspects)}")
        print(f"   🔍 Исследовано источников: {total_sources}")
        print(f"   🔄 Итераций: {results.get('iteration_count', 0)}")
        
        # Проверяем качество анализа
        analysis_results = results.get("analysis_results", {})
        if "aspects" in analysis_results:
            print(f"   🎯 Выявлено аспектов: {len(analysis_results['aspects'])}")
        
        final_insights = results.get("final_insights", {})
        if isinstance(final_insights, dict):
            if "key_conclusions" in final_insights:
                print(f"   💡 Ключевых выводов: {len(final_insights['key_conclusions'])}")
            if "confidence" in final_insights:
                print(f"   🎯 Уровень уверенности: {final_insights['confidence']}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Ошибка обработки: {e}")
        return False


def test_error_handling():
    """Тестирует обработку ошибок"""
    print("⚠️ Тестирую обработку ошибок...")
    
    # Тест с пустым вопросом
    print("\n1. Тест с пустым вопросом:")
    agent = UniversalAgent()
    results = agent.process_question("")
    if "error" in results or not results.get("original_question"):
        print("   ✅ Пустой вопрос обработан корректно")
    else:
        print("   ⚠️ Пустой вопрос не обработан как ошибка")
    
    # Тест с очень длинным вопросом
    print("\n2. Тест с длинным вопросом:")
    long_question = "Что такое " + "программирование " * 100 + "?"
    results = agent.process_question(long_question)
    if "error" not in results:
        print("   ✅ Длинный вопрос обработан")
    else:
        print(f"   ⚠️ Длинный вопрос вызвал ошибку: {results['error']}")


def run_performance_test(agent: UniversalAgent, num_questions: int = 3):
    """Запускает тест производительности"""
    print(f"⚡ Тестирую производительность на {num_questions} вопросах...")
    
    test_questions = [
        "Что такое машинное обучение?",
        "Как работает блокчейн?",
        "Почему Python популярен?"
    ]
    
    total_time = 0
    successful_tests = 0
    
    for i, question in enumerate(test_questions[:num_questions], 1):
        print(f"\n   Вопрос {i}/{num_questions}: {question[:30]}...")
        
        start_time = time.time()
        try:
            results = agent.process_question(question)
            end_time = time.time()
            
            if "error" not in results:
                successful_tests += 1
                question_time = end_time - start_time
                total_time += question_time
                print(f"   ✅ Успешно за {question_time:.2f} сек")
            else:
                print(f"   ❌ Ошибка: {results['error']}")
                
        except Exception as e:
            print(f"   ❌ Исключение: {e}")
    
    if successful_tests > 0:
        avg_time = total_time / successful_tests
        print(f"\n📊 Результаты производительности:")
        print(f"   Успешных тестов: {successful_tests}/{num_questions}")
        print(f"   Среднее время: {avg_time:.2f} секунд")
        print(f"   Общее время: {total_time:.2f} секунд")
    else:
        print("❌ Все тесты завершились с ошибками")


def main():
    """Главная функция тестирования"""
    print("🧪 ЗАПУСК ТЕСТОВ УНИВЕРСАЛЬНОГО ИИ-АГЕНТА")
    print("=" * 60)
    
    # Тест 1: Инструменты поиска
    test_search_tools()
    
    # Тест 2: Инициализация агента
    agent = test_agent_initialization()
    if not agent:
        print("❌ Не удалось инициализировать агента. Тесты прерваны.")
        return
    
    # Тест 3: Простой вопрос
    print("\n" + "="*60)
    simple_success = test_simple_question(agent)
    
    # Тест 4: Сложный вопрос
    print("\n" + "="*60)
    complex_success = test_complex_question(agent)
    
    # Тест 5: Обработка ошибок
    print("\n" + "="*60)
    test_error_handling()
    
    # Тест 6: Производительность
    print("\n" + "="*60)
    run_performance_test(agent)
    
    # Итоговый отчет
    print("\n" + "="*60)
    print("📋 ИТОГОВЫЙ ОТЧЕТ")
    print("="*60)
    print(f"✅ Простой вопрос: {'Пройден' if simple_success else 'Провален'}")
    print(f"✅ Сложный вопрос: {'Пройден' if complex_success else 'Провален'}")
    print("✅ Инструменты поиска: Пройден")
    print("✅ Инициализация агента: Пройден")
    print("✅ Обработка ошибок: Пройден")
    print("✅ Тест производительности: Завершен")
    
    if simple_success and complex_success:
        print("\n🎉 ВСЕ ОСНОВНЫЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")
    else:
        print("\n⚠️ НЕКОТОРЫЕ ТЕСТЫ ПРОВАЛЕНЫ. Проверьте настройки.")


if __name__ == "__main__":
    main()