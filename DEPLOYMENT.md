# 🚀 Руководство по развертыванию

## Системные требования

### Минимальные требования
- **OS**: Linux, macOS, Windows
- **Python**: 3.8 или выше
- **RAM**: 8 GB (рекомендуется 16 GB)
- **Дисковое пространство**: 10 GB свободного места
- **Интернет**: Стабильное соединение для поиска

### Рекомендуемые требования
- **RAM**: 32 GB
- **CPU**: 8+ ядер
- **GPU**: NVIDIA GPU с 8+ GB VRAM (опционально)
- **Дисковое пространство**: 50+ GB

## Установка

### 1. Клонирование репозитория
```bash
git clone <repository-url>
cd universal-ai-agent
```

### 2. Создание виртуального окружения
```bash
# Linux/macOS
python -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 4. Настройка Ollama
```bash
# Автоматическая настройка
python setup_ollama.py

# Или ручная настройка
ollama pull gemma2:9b
ollama serve
```

## Конфигурация

### Переменные окружения
Создайте файл `.env`:
```bash
cp .env.example .env
```

Отредактируйте `.env`:
```env
# Ollama настройки
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=gemma2:9b

# Настройки поиска
DUCKDUCKGO_MAX_RESULTS=10
REQUEST_TIMEOUT=30

# Настройки агента
MAX_ITERATIONS=5
MAX_ASPECTS_PER_QUESTION=10
```

### Настройка производительности
Отредактируйте `config.py` для оптимизации:

```python
# Для мощных систем
duckduckgo_max_results = 20
max_iterations = 10
max_aspects_per_question = 15

# Для слабых систем
duckduckgo_max_results = 5
max_iterations = 3
max_aspects_per_question = 5
```

## Запуск

### Локальный запуск
```bash
# Интерактивный режим
python main.py

# Обработка конкретного вопроса
python main.py "Ваш вопрос здесь"

# Демонстрация возможностей
python demo.py

# Тестирование
python test_agent.py
```

### Запуск как сервис (Linux)

#### Создание systemd сервиса
```bash
sudo nano /etc/systemd/system/ai-agent.service
```

Содержимое файла:
```ini
[Unit]
Description=Universal AI Agent
After=network.target

[Service]
Type=simple
User=your_username
WorkingDirectory=/path/to/universal-ai-agent
Environment=PATH=/path/to/universal-ai-agent/venv/bin
ExecStart=/path/to/universal-ai-agent/venv/bin/python main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

#### Активация сервиса
```bash
sudo systemctl daemon-reload
sudo systemctl enable ai-agent
sudo systemctl start ai-agent
sudo systemctl status ai-agent
```

### Docker развертывание

#### Создание Dockerfile
```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Установка Ollama
RUN curl -fsSL https://ollama.ai/install.sh | sh

# Копирование файлов проекта
COPY . .

# Установка Python зависимостей
RUN pip install -r requirements.txt

# Скачивание модели
RUN ollama pull gemma2:9b

# Запуск Ollama и агента
CMD ["sh", "-c", "ollama serve & python main.py"]
```

#### Сборка и запуск
```bash
docker build -t universal-ai-agent .
docker run -p 11434:11434 -p 8000:8000 universal-ai-agent
```

## Мониторинг

### Логирование
Агент ведет подробные логи:
```bash
# Просмотр логов
tail -f logs/agent.log

# Фильтрация по уровню
grep "ERROR" logs/agent.log
grep "INFO" logs/agent.log
```

### Метрики производительности
```python
# В коде агента доступны метрики:
- Время обработки вопросов
- Количество обработанных аспектов
- Количество исследованных источников
- Уровень уверенности в результатах
```

### Мониторинг ресурсов
```bash
# Мониторинг использования памяти
htop

# Мониторинг дискового пространства
df -h

# Мониторинг сетевой активности
netstat -tulpn
```

## Масштабирование

### Горизонтальное масштабирование
1. Запустите несколько экземпляров агента
2. Используйте балансировщик нагрузки
3. Настройте общую базу данных для кэширования

### Вертикальное масштабирование
1. Увеличьте количество ядер CPU
2. Добавьте больше RAM
3. Используйте GPU для ускорения LLM

### Кэширование
```python
# Добавьте кэширование в config.py
CACHE_ENABLED = True
CACHE_TTL = 3600  # 1 час
CACHE_SIZE = 1000  # Максимум записей
```

## Безопасность

### Изоляция
```bash
# Запуск в изолированном окружении
docker run --rm -it --network none universal-ai-agent
```

### Ограничения ресурсов
```bash
# Ограничение памяти
ulimit -v 8388608  # 8 GB

# Ограничение CPU
taskset -c 0-3 python main.py  # Использовать только 4 ядра
```

### Аутентификация
```python
# Добавьте в config.py
API_KEY = "your-secret-key"
REQUIRE_AUTH = True
```

## Резервное копирование

### Конфигурация
```bash
# Создание резервной копии
tar -czf backup-$(date +%Y%m%d).tar.gz \
    config.py \
    .env \
    logs/ \
    results/
```

### Восстановление
```bash
# Восстановление из резервной копии
tar -xzf backup-20240101.tar.gz
```

## Устранение неполадок

### Частые проблемы

#### Ollama не запускается
```bash
# Проверка статуса
systemctl status ollama

# Перезапуск
sudo systemctl restart ollama

# Проверка логов
journalctl -u ollama -f
```

#### Нехватка памяти
```bash
# Освобождение памяти
sudo sync
echo 3 | sudo tee /proc/sys/vm/drop_caches

# Увеличение swap
sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

#### Медленная работа
```bash
# Оптимизация настроек
# Уменьшите max_iterations в config.py
# Уменьшите duckduckgo_max_results
# Используйте более быструю модель
```

### Диагностика
```bash
# Полная диагностика системы
python test_agent.py

# Проверка подключений
curl http://localhost:11434/api/tags

# Тест производительности
python demo.py
```

## Обновление

### Обновление кода
```bash
git pull origin main
pip install -r requirements.txt
```

### Обновление модели
```bash
ollama pull gemma2:9b
```

### Обновление зависимостей
```bash
pip install --upgrade -r requirements.txt
```

---

**🎉 Агент успешно развернут и готов к работе!**