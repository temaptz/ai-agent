# 📖 Руководство по использованию

## 🚀 Быстрый старт

### 1. Первый запуск
```bash
# Настройка окружения
python setup_ollama.py

# Запуск агента
python main.py
```

### 2. Тестирование
```bash
# Проверка работоспособности
python test_agent.py

# Демонстрация возможностей
python demo.py
```

## 💡 Основные сценарии использования

### Интерактивный режим
```bash
python main.py
```
Введите вопрос и получите всесторонний анализ.

### Обработка конкретного вопроса
```bash
python main.py "Как работает блокчейн?"
```

### Пакетная обработка
```python
from agent.universal_agent import UniversalAgent

agent = UniversalAgent()
questions = [
    "Что такое машинное обучение?",
    "Как создать успешный стартап?",
    "Почему важна кибербезопасность?"
]

for question in questions:
    results = agent.process_question(question)
    print(f"Вопрос: {question}")
    print(f"Ответ: {results['final_insights']['summary']}")
```

## 🔧 Настройка агента

### Изменение модели
```python
# В config.py
ollama_model = "gemma2:9b"  # Или другая модель
```

### Настройка поиска
```python
# В config.py
duckduckgo_max_results = 15  # Больше результатов
request_timeout = 60  # Больше времени ожидания
```

### Ограничение итераций
```python
# В config.py
max_iterations = 3  # Меньше итераций для быстрой работы
max_aspects_per_question = 5  # Меньше аспектов
```

## 📊 Анализ результатов

### Структура результатов
```python
results = {
    "original_question": "Ваш вопрос",
    "analysis_results": {
        "motivation": "Анализ мотивации",
        "aspects": ["аспект1", "аспект2"],
        "research_questions": ["вопрос1", "вопрос2"]
    },
    "processed_aspects": ["обработанный_аспект1"],
    "research_data": [
        {
            "aspect": "аспект",
            "research_data": [...],
            "analysis": {...}
        }
    ],
    "final_insights": {
        "summary": "Краткий ответ",
        "key_conclusions": ["вывод1", "вывод2"],
        "insights": ["инсайт1", "инсайт2"],
        "recommendations": ["рекомендация1"],
        "confidence": "высокий/средний/низкий"
    }
}
```

### Извлечение информации
```python
# Краткий ответ
summary = results["final_insights"]["summary"]

# Ключевые выводы
conclusions = results["final_insights"]["key_conclusions"]

# Уровень уверенности
confidence = results["final_insights"]["confidence"]

# Количество аспектов
aspects_count = len(results["processed_aspects"])
```

## 🛠 Расширение функциональности

### Добавление нового инструмента
```python
# В agent/universal_agent.py
def _create_custom_tool(self):
    def custom_function(param: str) -> str:
        # Ваша логика
        return result
    
    return {
        "name": "custom_tool",
        "description": "Описание инструмента",
        "function": custom_function
    }
```

### Добавление нового промпта
```python
def _create_custom_prompt(self) -> ChatPromptTemplate:
    template = """
    Ваш промпт здесь...
    """
    return ChatPromptTemplate.from_template(template)
```

### Кастомизация анализа
```python
# Переопределите метод analyze_question
def analyze_question(self, state: AgentState) -> AgentState:
    # Ваша логика анализа
    return state
```

## 📈 Оптимизация производительности

### Для быстрой работы
```python
# В config.py
max_iterations = 2
max_aspects_per_question = 3
duckduckgo_max_results = 5
```

### Для глубокого анализа
```python
# В config.py
max_iterations = 10
max_aspects_per_question = 15
duckduckgo_max_results = 20
```

### Кэширование результатов
```python
from utils.helpers import save_results_to_file, load_results_from_file

# Сохранение
filename = save_results_to_file(results)

# Загрузка
results = load_results_from_file(filename)
```

## 🔍 Отладка

### Включение подробных логов
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Тестирование отдельных компонентов
```python
from tools.search_tools import web_search_tool, url_content_tool

# Тест поиска
results = web_search_tool.search("тест")

# Тест загрузки URL
content = url_content_tool.load_url("https://example.com")
```

### Проверка состояния агента
```python
agent = UniversalAgent()
print(f"Модель: {agent.llm.model}")
print(f"Инструменты: {len(agent.tools)}")
```

## 📝 Примеры использования

### Анализ технических вопросов
```python
technical_questions = [
    "Как работает машинное обучение?",
    "Что такое блокчейн?",
    "Как создать REST API?",
    "Почему важна кибербезопасность?"
]

for question in technical_questions:
    results = agent.process_question(question)
    print(f"Вопрос: {question}")
    print(f"Аспекты: {len(results['processed_aspects'])}")
    print(f"Уверенность: {results['final_insights']['confidence']}")
```

### Анализ бизнес-вопросов
```python
business_questions = [
    "Как создать успешный стартап?",
    "Почему важна цифровая трансформация?",
    "Как выбрать правильную бизнес-модель?",
    "Что такое agile-методология?"
]
```

### Анализ философских вопросов
```python
philosophical_questions = [
    "Почему люди боятся новых технологий?",
    "Как развить критическое мышление?",
    "Что такое этика в ИИ?",
    "Почему важно изучать историю?"
]
```

## 🚨 Обработка ошибок

### Типичные ошибки
```python
try:
    results = agent.process_question(question)
except Exception as e:
    print(f"Ошибка: {e}")
    # Обработка ошибки
```

### Проверка результатов
```python
if "error" in results:
    print(f"Ошибка анализа: {results['error']}")
else:
    print("Анализ успешен")
```

## 📊 Мониторинг

### Отслеживание производительности
```python
import time

start_time = time.time()
results = agent.process_question(question)
end_time = time.time()

print(f"Время обработки: {end_time - start_time:.2f} секунд")
```

### Анализ качества
```python
# Проверка полноты анализа
aspects_count = len(results["processed_aspects"])
sources_count = sum(len(aspect.get("research_data", [])) for aspect in results["research_data"])

print(f"Аспектов: {aspects_count}")
print(f"Источников: {sources_count}")
print(f"Уверенность: {results['final_insights']['confidence']}")
```

## 🎯 Лучшие практики

### Формулировка вопросов
- ✅ "Как работает машинное обучение?"
- ❌ "ML"

- ✅ "Почему Python стал популярным?"
- ❌ "Python"

### Ожидание результатов
- Простые вопросы: 30-60 секунд
- Сложные вопросы: 2-5 минут
- Очень сложные: 5-10 минут

### Интерпретация результатов
- Высокая уверенность: Результаты надежны
- Средняя уверенность: Требует дополнительной проверки
- Низкая уверенность: Недостаточно данных

---

**🎉 Агент готов к продуктивному использованию!**