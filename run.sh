#!/bin/bash

# Скрипт для запуска универсального ИИ-агента
# Автор: Сеньор-программист с 20-летним стажем

echo "🚀 Универсальный ИИ-агент"
echo "=========================="

# Проверяем, что мы в правильной директории
if [ ! -f "main.py" ]; then
    echo "❌ Ошибка: Запустите скрипт из корневой директории проекта"
    exit 1
fi

# Проверяем Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Ошибка: Python3 не найден"
    exit 1
fi

# Проверяем виртуальное окружение
if [ ! -d "venv" ]; then
    echo "📦 Создаю виртуальное окружение..."
    python3 -m venv venv
fi

# Активируем виртуальное окружение
echo "🔧 Активирую виртуальное окружение..."
source venv/bin/activate

# Устанавливаем зависимости
echo "📥 Устанавливаю зависимости..."
pip install -r requirements.txt

# Проверяем Ollama
echo "🤖 Проверяю Ollama..."
if ! command -v ollama &> /dev/null; then
    echo "❌ Ollama не найден. Устанавливаю..."
    curl -fsSL https://ollama.ai/install.sh | sh
fi

# Запускаем Ollama в фоне
echo "🚀 Запускаю Ollama..."
ollama serve &
OLLAMA_PID=$!

# Ждем запуска Ollama
echo "⏳ Ожидаю запуска Ollama..."
sleep 5

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

# Запускаем агента
echo "🎯 Запускаю агента..."
echo "=========================="

# Обработка аргументов командной строки
if [ $# -eq 0 ]; then
    # Интерактивный режим
    python main.py
else
    # Обработка конкретного вопроса
    python main.py "$*"
fi

# Останавливаем Ollama
echo "🛑 Останавливаю Ollama..."
kill $OLLAMA_PID 2>/dev/null

echo "✅ Работа завершена"