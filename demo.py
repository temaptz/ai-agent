"""
Демонстрация возможностей универсального ИИ-агента
"""
import sys
import os
import time
from typing import Dict, Any

# Добавляем текущую директорию в путь
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agent.universal_agent import UniversalAgent
from utils.helpers import create_summary_report, estimate_processing_time
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def demo_simple_question():
    """Демонстрация обработки простого вопроса"""
    print("🎯 ДЕМОНСТРАЦИЯ 1: Простой вопрос")
    print("=" * 50)
    
    question = "Что такое машинное обучение?"
    print(f"❓ Вопрос: {question}")
    
    estimated_time = estimate_processing_time(question)
    print(f"⏱ Оценочное время: {estimated_time} секунд")
    
    agent = UniversalAgent()
    start_time = time.time()
    
    print("\n🔄 Обрабатываю вопрос...")
    results = agent.process_question(question)
    
    end_time = time.time()
    actual_time = end_time - start_time
    
    print(f"✅ Обработка завершена за {actual_time:.1f} секунд")
    print(f"📊 Точность оценки: {((estimated_time - actual_time) / estimated_time * 100):.1f}%")
    
    # Выводим краткий отчет
    summary = create_summary_report(results)
    print(f"\n📋 КРАТКИЙ ОТЧЕТ:\n{summary}")
    
    return results


def demo_complex_question():
    """Демонстрация обработки сложного вопроса"""
    print("\n\n🧠 ДЕМОНСТРАЦИЯ 2: Сложный вопрос")
    print("=" * 50)
    
    question = "Как искусственный интеллект изменит образование в ближайшие 5 лет?"
    print(f"❓ Вопрос: {question}")
    
    estimated_time = estimate_processing_time(question)
    print(f"⏱ Оценочное время: {estimated_time} секунд")
    
    agent = UniversalAgent()
    start_time = time.time()
    
    print("\n🔄 Обрабатываю вопрос...")
    results = agent.process_question(question)
    
    end_time = time.time()
    actual_time = end_time - start_time
    
    print(f"✅ Обработка завершена за {actual_time:.1f} секунд")
    
    # Анализируем результаты
    aspects = results.get("processed_aspects", [])
    research_data = results.get("research_data", [])
    total_sources = sum(len(aspect.get("research_data", [])) for aspect in research_data)
    
    print(f"\n📊 ДЕТАЛЬНАЯ СТАТИСТИКА:")
    print(f"   • Обработано аспектов: {len(aspects)}")
    print(f"   • Исследовано источников: {total_sources}")
    print(f"   • Итераций: {results.get('iteration_count', 0)}")
    
    # Выводим аспекты
    if aspects:
        print(f"\n🔍 ОБРАБОТАННЫЕ АСПЕКТЫ:")
        for i, aspect in enumerate(aspects, 1):
            print(f"   {i}. {aspect}")
    
    # Выводим краткий отчет
    summary = create_summary_report(results)
    print(f"\n📋 КРАТКИЙ ОТЧЕТ:\n{summary}")
    
    return results


def demo_technical_question():
    """Демонстрация обработки технического вопроса"""
    print("\n\n⚙️ ДЕМОНСТРАЦИЯ 3: Технический вопрос")
    print("=" * 50)
    
    question = "Как работает блокчейн и какие у него преимущества?"
    print(f"❓ Вопрос: {question}")
    
    agent = UniversalAgent()
    start_time = time.time()
    
    print("\n🔄 Обрабатываю вопрос...")
    results = agent.process_question(question)
    
    end_time = time.time()
    actual_time = end_time - start_time
    
    print(f"✅ Обработка завершена за {actual_time:.1f} секунд")
    
    # Анализируем технические аспекты
    analysis_results = results.get("analysis_results", {})
    if "aspects" in analysis_results:
        print(f"\n🔧 ТЕХНИЧЕСКИЕ АСПЕКТЫ:")
        for i, aspect in enumerate(analysis_results["aspects"], 1):
            print(f"   {i}. {aspect}")
    
    # Выводим краткий отчет
    summary = create_summary_report(results)
    print(f"\n📋 КРАТКИЙ ОТЧЕТ:\n{summary}")
    
    return results


def demo_philosophical_question():
    """Демонстрация обработки философского вопроса"""
    print("\n\n🤔 ДЕМОНСТРАЦИЯ 4: Философский вопрос")
    print("=" * 50)
    
    question = "Почему люди боятся новых технологий?"
    print(f"❓ Вопрос: {question}")
    
    agent = UniversalAgent()
    start_time = time.time()
    
    print("\n🔄 Обрабатываю вопрос...")
    results = agent.process_question(question)
    
    end_time = time.time()
    actual_time = end_time - start_time
    
    print(f"✅ Обработка завершена за {actual_time:.1f} секунд")
    
    # Анализируем философские аспекты
    final_insights = results.get("final_insights", {})
    if isinstance(final_insights, dict):
        if "insights" in final_insights:
            print(f"\n💭 ФИЛОСОФСКИЕ ИНСАЙТЫ:")
            for insight in final_insights["insights"]:
                print(f"   • {insight}")
    
    # Выводим краткий отчет
    summary = create_summary_report(results)
    print(f"\n📋 КРАТКИЙ ОТЧЕТ:\n{summary}")
    
    return results


def demo_performance_comparison():
    """Демонстрация сравнения производительности"""
    print("\n\n⚡ ДЕМОНСТРАЦИЯ 5: Сравнение производительности")
    print("=" * 50)
    
    questions = [
        "Что такое Python?",
        "Как работает машинное обучение?",
        "Почему важна кибербезопасность?",
        "Как создать успешный стартап?",
        "Что такое квантовые вычисления?"
    ]
    
    agent = UniversalAgent()
    results = []
    
    print("🔄 Обрабатываю 5 вопросов разной сложности...")
    
    total_start = time.time()
    
    for i, question in enumerate(questions, 1):
        print(f"\n   Вопрос {i}/5: {question[:30]}...")
        
        start_time = time.time()
        result = agent.process_question(question)
        end_time = time.time()
        
        processing_time = end_time - start_time
        aspects_count = len(result.get("processed_aspects", []))
        
        results.append({
            "question": question,
            "time": processing_time,
            "aspects": aspects_count,
            "success": "error" not in result
        })
        
        print(f"   ✅ Завершен за {processing_time:.1f}с, аспектов: {aspects_count}")
    
    total_time = time.time() - total_start
    
    # Статистика
    successful = sum(1 for r in results if r["success"])
    avg_time = sum(r["time"] for r in results) / len(results)
    total_aspects = sum(r["aspects"] for r in results)
    
    print(f"\n📊 ИТОГОВАЯ СТАТИСТИКА:")
    print(f"   • Успешных обработок: {successful}/{len(questions)}")
    print(f"   • Общее время: {total_time:.1f} секунд")
    print(f"   • Среднее время на вопрос: {avg_time:.1f} секунд")
    print(f"   • Всего обработано аспектов: {total_aspects}")
    print(f"   • Средняя скорость: {len(questions)/total_time*60:.1f} вопросов/мин")
    
    return results


def main():
    """Главная функция демонстрации"""
    print("🎭 ДЕМОНСТРАЦИЯ ВОЗМОЖНОСТЕЙ УНИВЕРСАЛЬНОГО ИИ-АГЕНТА")
    print("=" * 70)
    print("Этот скрипт демонстрирует различные возможности агента")
    print("на примерах вопросов разной сложности и тематики.")
    print("=" * 70)
    
    try:
        # Демонстрация 1: Простой вопрос
        demo_simple_question()
        
        # Демонстрация 2: Сложный вопрос
        demo_complex_question()
        
        # Демонстрация 3: Технический вопрос
        demo_technical_question()
        
        # Демонстрация 4: Философский вопрос
        demo_philosophical_question()
        
        # Демонстрация 5: Сравнение производительности
        demo_performance_comparison()
        
        print("\n\n🎉 ВСЕ ДЕМОНСТРАЦИИ ЗАВЕРШЕНЫ!")
        print("=" * 70)
        print("Агент успешно продемонстрировал свои возможности:")
        print("✅ Анализ простых и сложных вопросов")
        print("✅ Работу с техническими и философскими темами")
        print("✅ Стабильную производительность")
        print("✅ Глубокий анализ и синтез информации")
        print("\n🚀 Агент готов к продуктивному использованию!")
        
    except KeyboardInterrupt:
        print("\n\n⏹️ Демонстрация прервана пользователем")
    except Exception as e:
        print(f"\n\n❌ Ошибка во время демонстрации: {e}")
        logger.error(f"Ошибка демонстрации: {e}")


if __name__ == "__main__":
    main()