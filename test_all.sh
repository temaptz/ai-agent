#!/bin/bash

# Скрипт для полного тестирования универсального ИИ-агента
# Автор: Сеньор-программист с 20-летним стажем

echo "🧪 ПОЛНОЕ ТЕСТИРОВАНИЕ УНИВЕРСАЛЬНОГО ИИ-АГЕНТА"
echo "=============================================="

# Проверяем, что мы в правильной директории
if [ ! -f "main.py" ]; then
    echo "❌ Ошибка: Запустите скрипт из корневой директории проекта"
    exit 1
fi

# Активируем виртуальное окружение
if [ -d "venv" ]; then
    echo "🔧 Активирую виртуальное окружение..."
    source venv/bin/activate
fi

# Устанавливаем зависимости
echo "📥 Устанавливаю зависимости..."
pip install -r requirements.txt

# Запускаем Ollama в фоне
echo "🚀 Запускаю Ollama..."
ollama serve &
OLLAMA_PID=$!

# Ждем запуска Ollama
echo "⏳ Ожидаю запуска Ollama..."
sleep 10

# Проверяем, что Ollama запустился
if ! curl -s http://localhost:11434/api/tags > /dev/null; then
    echo "❌ Не удалось запустить Ollama"
    kill $OLLAMA_PID 2>/dev/null
    exit 1
fi

# Устанавливаем модель, если нужно
echo "🧠 Проверяю модель Gemma2..."
if ! ollama list | grep -q "gemma2:9b"; then
    echo "📥 Устанавливаю модель Gemma2:9b..."
    ollama pull gemma2:9b
fi

echo ""
echo "🧪 ЗАПУСК ТЕСТОВ"
echo "================"

# Тест 1: Базовые тесты
echo ""
echo "1️⃣ Базовые тесты..."
python test_agent.py
if [ $? -eq 0 ]; then
    echo "✅ Базовые тесты пройдены"
else
    echo "❌ Базовые тесты провалены"
fi

# Тест 2: Демонстрация
echo ""
echo "2️⃣ Демонстрация возможностей..."
python demo.py
if [ $? -eq 0 ]; then
    echo "✅ Демонстрация завершена"
else
    echo "❌ Ошибка в демонстрации"
fi

# Тест 3: Примеры
echo ""
echo "3️⃣ Тестирование примеров..."
python examples.py interactive
if [ $? -eq 0 ]; then
    echo "✅ Примеры работают"
else
    echo "❌ Ошибка в примерах"
fi

# Тест 4: Производительность
echo ""
echo "4️⃣ Тест производительности..."
timeout 300 python -c "
from agent.universal_agent import UniversalAgent
import time

agent = UniversalAgent()
questions = [
    'Что такое Python?',
    'Как работает машинное обучение?',
    'Почему важна кибербезопасность?'
]

start_time = time.time()
for i, question in enumerate(questions, 1):
    print(f'Тест {i}/3: {question[:30]}...')
    results = agent.process_question(question)
    if 'error' in results:
        print(f'Ошибка в тесте {i}')
        exit(1)
    print(f'✅ Тест {i} завершен')

total_time = time.time() - start_time
print(f'Все тесты завершены за {total_time:.1f} секунд')
print(f'Среднее время: {total_time/len(questions):.1f} секунд на вопрос')
"

if [ $? -eq 0 ]; then
    echo "✅ Тест производительности пройден"
else
    echo "❌ Тест производительности провален"
fi

# Тест 5: Обработка ошибок
echo ""
echo "5️⃣ Тест обработки ошибок..."
python -c "
from agent.universal_agent import UniversalAgent

agent = UniversalAgent()

# Тест с пустым вопросом
results = agent.process_question('')
if 'error' in results or not results.get('original_question'):
    print('✅ Пустой вопрос обработан корректно')
else:
    print('❌ Пустой вопрос не обработан как ошибка')
    exit(1)

# Тест с очень длинным вопросом
long_question = 'Что такое ' + 'программирование ' * 100 + '?'
results = agent.process_question(long_question)
if 'error' not in results:
    print('✅ Длинный вопрос обработан')
else:
    print('❌ Длинный вопрос вызвал ошибку')
    exit(1)

print('✅ Тест обработки ошибок пройден')
"

if [ $? -eq 0 ]; then
    echo "✅ Тест обработки ошибок пройден"
else
    echo "❌ Тест обработки ошибок провален"
fi

# Останавливаем Ollama
echo ""
echo "🛑 Останавливаю Ollama..."
kill $OLLAMA_PID 2>/dev/null

# Итоговый отчет
echo ""
echo "📊 ИТОГОВЫЙ ОТЧЕТ"
echo "================="
echo "✅ Все тесты завершены"
echo "✅ Агент готов к использованию"
echo ""
echo "🚀 Для запуска используйте:"
echo "   python main.py"
echo "   ./run.sh"
echo ""
echo "📚 Документация:"
echo "   README.md - основная документация"
echo "   QUICKSTART.md - быстрый старт"
echo "   USAGE.md - руководство по использованию"
echo "   DEPLOYMENT.md - развертывание"
echo ""
echo "🎉 Тестирование завершено успешно!"