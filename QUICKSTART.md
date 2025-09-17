# 🚀 Быстрый старт

## Установка и настройка

### 1. Установите зависимости
```bash
pip install -r requirements.txt
```

### 2. Настройте Ollama
```bash
# Автоматическая настройка
python setup_ollama.py

# Или вручную:
ollama pull gemma2:9b
ollama serve
```

### 3. Запустите агента
```bash
# Интерактивный режим
python main.py

# Обработка конкретного вопроса
python main.py "Как работает машинное обучение?"
```

## 🧪 Тестирование

```bash
# Запустить все тесты
python test_agent.py

# Запустить примеры
python examples.py
```

## 📁 Структура проекта

```
universal-ai-agent/
├── agent/                 # Основной агент
│   ├── __init__.py
│   └── universal_agent.py
├── tools/                 # Инструменты поиска
│   ├── __init__.py
│   └── search_tools.py
├── utils/                 # Вспомогательные функции
│   ├── __init__.py
│   └── helpers.py
├── config.py             # Конфигурация
├── main.py               # Главный файл
├── examples.py           # Примеры использования
├── test_agent.py         # Тесты
├── setup_ollama.py       # Настройка Ollama
├── requirements.txt      # Зависимости
└── README.md            # Документация
```

## ⚡ Примеры использования

### Простой вопрос
```python
from agent.universal_agent import UniversalAgent

agent = UniversalAgent()
results = agent.process_question("Что такое Python?")
print(results)
```

### Сложный анализ
```python
question = "Как искусственный интеллект изменит образование?"
results = agent.process_question(question)

# Результаты содержат:
# - analysis_results: разбиение на аспекты
# - research_data: данные исследования
# - final_insights: итоговые выводы
```

## 🔧 Настройка

Отредактируйте `config.py` для изменения настроек:

```python
# Ollama настройки
ollama_base_url = "http://localhost:11434"
ollama_model = "gemma2:9b"

# Настройки поиска
duckduckgo_max_results = 10
request_timeout = 30

# Настройки агента
max_iterations = 5
max_aspects_per_question = 10
```

## 🆘 Решение проблем

### Ollama не запускается
```bash
ollama serve
```

### Модель не найдена
```bash
ollama pull gemma2:9b
```

### Ошибки поиска
- Проверьте интернет-соединение
- Увеличьте `request_timeout` в конфигурации

## 📊 Мониторинг

Агент выводит подробную информацию о процессе:
- 🔍 Этапы анализа
- 📊 Статистику обработки
- ⏱ Время выполнения
- 🎯 Уровень уверенности в результатах

---

**Готово! Агент готов к работе! 🎉**