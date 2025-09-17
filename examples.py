"""
Примеры использования универсального ИИ-агента
"""
import sys
import os

# Добавляем текущую директорию в путь
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agent.universal_agent import UniversalAgent
import json


def example_questions():
    """Возвращает список примеров вопросов для тестирования"""
    return [
        "Как искусственный интеллект изменит образование в ближайшие 5 лет?",
        "Почему некоторые люди боятся новых технологий?",
        "Как выбрать правильную карьеру в IT?",
        "Что такое квантовые вычисления и зачем они нужны?",
        "Как решить проблему изменения климата?",
        "Почему Python стал таким популярным языком программирования?",
        "Как создать успешный стартап?",
        "Что такое блокчейн и как он работает?",
        "Как развить критическое мышление?",
        "Почему важно изучать математику?"
    ]


def run_example(question: str, save_results: bool = True) -> dict:
    """
    Запускает анализ примера вопроса
    
    Args:
        question: Вопрос для анализа
        save_results: Сохранять ли результаты в файл
        
    Returns:
        Результаты анализа
    """
    print(f"\n{'='*80}")
    print(f"АНАЛИЗ ВОПРОСА: {question}")
    print('='*80)
    
    agent = UniversalAgent()
    results = agent.process_question(question)
    
    if save_results:
        # Сохраняем результаты в файл
        filename = f"results_{question.replace(' ', '_').replace('?', '').replace('!', '')[:50]}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"📁 Результаты сохранены в файл: {filename}")
    
    return results


def run_all_examples():
    """Запускает анализ всех примеров вопросов"""
    questions = example_questions()
    
    print("🚀 Запускаю анализ всех примеров вопросов...")
    print(f"📊 Всего вопросов: {len(questions)}")
    
    all_results = []
    
    for i, question in enumerate(questions, 1):
        print(f"\n📝 Вопрос {i}/{len(questions)}")
        try:
            results = run_example(question, save_results=True)
            all_results.append({
                "question": question,
                "results": results
            })
        except Exception as e:
            print(f"❌ Ошибка при обработке вопроса: {e}")
            all_results.append({
                "question": question,
                "error": str(e)
            })
    
    # Сохраняем сводные результаты
    with open("all_results_summary.json", 'w', encoding='utf-8') as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Анализ завершен! Результаты сохранены в файлы.")
    return all_results


def run_specific_example(question_index: int):
    """
    Запускает анализ конкретного примера по индексу
    
    Args:
        question_index: Индекс вопроса в списке примеров (начиная с 0)
    """
    questions = example_questions()
    
    if question_index < 0 or question_index >= len(questions):
        print(f"❌ Неверный индекс. Доступны индексы от 0 до {len(questions)-1}")
        return
    
    question = questions[question_index]
    run_example(question, save_results=True)


def interactive_example_selection():
    """Интерактивный выбор примера для анализа"""
    questions = example_questions()
    
    print("📋 Доступные примеры вопросов:")
    print("-" * 50)
    
    for i, question in enumerate(questions):
        print(f"{i+1:2d}. {question}")
    
    print("\nВыберите номер вопроса для анализа (или 0 для выхода):")
    
    while True:
        try:
            choice = input("Ваш выбор: ").strip()
            
            if choice == "0":
                print("👋 До свидания!")
                break
            
            question_index = int(choice) - 1
            
            if 0 <= question_index < len(questions):
                run_specific_example(question_index)
                break
            else:
                print(f"❌ Пожалуйста, введите число от 0 до {len(questions)}")
                
        except ValueError:
            print("❌ Пожалуйста, введите корректное число")
        except KeyboardInterrupt:
            print("\n👋 До свидания!")
            break


def main():
    """Главная функция для запуска примеров"""
    print("🤖 Примеры использования универсального ИИ-агента")
    print("=" * 60)
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "all":
            run_all_examples()
        elif command == "interactive":
            interactive_example_selection()
        elif command.isdigit():
            run_specific_example(int(command) - 1)
        else:
            print("❌ Неизвестная команда")
            print("Доступные команды:")
            print("  python examples.py all        - запустить все примеры")
            print("  python examples.py interactive - интерактивный выбор")
            print("  python examples.py <номер>    - запустить конкретный пример")
    else:
        interactive_example_selection()


if __name__ == "__main__":
    main()