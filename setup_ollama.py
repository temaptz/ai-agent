"""
Скрипт для настройки Ollama и проверки доступности модели Gemma3
"""
import subprocess
import sys
import time
import requests
import json
from typing import List, Dict, Any


def check_ollama_installation() -> bool:
    """
    Проверяет, установлен ли Ollama
    
    Returns:
        True если Ollama установлен, False иначе
    """
    try:
        result = subprocess.run(['ollama', '--version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print(f"✅ Ollama установлен: {result.stdout.strip()}")
            return True
        else:
            print("❌ Ollama не найден в системе")
            return False
    except FileNotFoundError:
        print("❌ Ollama не установлен")
        return False
    except Exception as e:
        print(f"❌ Ошибка проверки Ollama: {e}")
        return False


def check_ollama_server() -> bool:
    """
    Проверяет, запущен ли сервер Ollama
    
    Returns:
        True если сервер доступен, False иначе
    """
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            print("✅ Сервер Ollama запущен и доступен")
            return True
        else:
            print(f"❌ Сервер Ollama недоступен (код: {response.status_code})")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Не удается подключиться к серверу Ollama")
        return False
    except Exception as e:
        print(f"❌ Ошибка проверки сервера: {e}")
        return False


def get_available_models() -> List[Dict[str, Any]]:
    """
    Получает список доступных моделей
    
    Returns:
        Список моделей с их информацией
    """
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=10)
        if response.status_code == 200:
            data = response.json()
            models = data.get("models", [])
            print(f"📋 Найдено моделей: {len(models)}")
            return models
        else:
            print("❌ Не удалось получить список моделей")
            return []
    except Exception as e:
        print(f"❌ Ошибка получения моделей: {e}")
        return []


def check_gemma_model(models: List[Dict[str, Any]]) -> bool:
    """
    Проверяет, доступна ли модель Gemma
    
    Args:
        models: Список доступных моделей
        
    Returns:
        True если Gemma доступна, False иначе
    """
    gemma_models = [model for model in models if 'gemma' in model.get('name', '').lower()]
    
    if gemma_models:
        print("✅ Модели Gemma найдены:")
        for model in gemma_models:
            name = model.get('name', 'Unknown')
            size = model.get('size', 0)
            size_gb = size / (1024**3) if size > 0 else 0
            print(f"   • {name} ({size_gb:.1f} GB)")
        return True
    else:
        print("❌ Модели Gemma не найдены")
        return False


def install_gemma_model() -> bool:
    """
    Устанавливает модель Gemma2:9b
    
    Returns:
        True если установка успешна, False иначе
    """
    print("📥 Устанавливаю модель gemma2:9b...")
    print("⚠️ Это может занять несколько минут...")
    
    try:
        # Запускаем команду установки
        process = subprocess.Popen(
            ['ollama', 'pull', 'gemma2:9b'],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        # Выводим прогресс в реальном времени
        for line in process.stdout:
            if line.strip():
                print(f"   {line.strip()}")
        
        process.wait()
        
        if process.returncode == 0:
            print("✅ Модель gemma2:9b успешно установлена")
            return True
        else:
            print("❌ Ошибка установки модели")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка при установке модели: {e}")
        return False


def test_model_response() -> bool:
    """
    Тестирует ответ модели на простой запрос
    
    Returns:
        True если модель отвечает корректно, False иначе
    """
    print("🧪 Тестирую ответ модели...")
    
    try:
        # Отправляем тестовый запрос
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "gemma2:9b",
                "prompt": "Привет! Как дела?",
                "stream": False
            },
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            model_response = data.get("response", "")
            if model_response.strip():
                print(f"✅ Модель отвечает: {model_response[:100]}...")
                return True
            else:
                print("❌ Модель не вернула ответ")
                return False
        else:
            print(f"❌ Ошибка API (код: {response.status_code})")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка тестирования модели: {e}")
        return False


def start_ollama_server() -> bool:
    """
    Пытается запустить сервер Ollama
    
    Returns:
        True если сервер запущен, False иначе
    """
    print("🚀 Пытаюсь запустить сервер Ollama...")
    
    try:
        # Запускаем сервер в фоновом режиме
        process = subprocess.Popen(
            ['ollama', 'serve'],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        
        # Ждем запуска сервера
        for i in range(30):  # Ждем до 30 секунд
            time.sleep(1)
            if check_ollama_server():
                print("✅ Сервер Ollama успешно запущен")
                return True
            print(f"   Ожидание запуска... ({i+1}/30)")
        
        print("❌ Не удалось запустить сервер Ollama")
        return False
        
    except Exception as e:
        print(f"❌ Ошибка запуска сервера: {e}")
        return False


def main():
    """Главная функция настройки"""
    print("🔧 НАСТРОЙКА OLLAMA ДЛЯ УНИВЕРСАЛЬНОГО ИИ-АГЕНТА")
    print("=" * 60)
    
    # Шаг 1: Проверяем установку Ollama
    print("\n1️⃣ Проверяю установку Ollama...")
    if not check_ollama_installation():
        print("\n❌ Ollama не установлен!")
        print("📥 Установите Ollama с https://ollama.ai/")
        print("   Linux: curl -fsSL https://ollama.ai/install.sh | sh")
        print("   macOS: brew install ollama")
        print("   Windows: скачайте с https://ollama.ai/download")
        return False
    
    # Шаг 2: Проверяем сервер
    print("\n2️⃣ Проверяю сервер Ollama...")
    if not check_ollama_server():
        print("\n🔄 Сервер не запущен, пытаюсь запустить...")
        if not start_ollama_server():
            print("\n❌ Не удалось запустить сервер!")
            print("💡 Попробуйте запустить вручную: ollama serve")
            return False
    
    # Шаг 3: Проверяем доступные модели
    print("\n3️⃣ Проверяю доступные модели...")
    models = get_available_models()
    
    # Шаг 4: Проверяем Gemma
    print("\n4️⃣ Проверяю модели Gemma...")
    if not check_gemma_model(models):
        print("\n📥 Модели Gemma не найдены, устанавливаю...")
        if not install_gemma_model():
            print("\n❌ Не удалось установить модель!")
            return False
    else:
        print("✅ Модели Gemma уже установлены")
    
    # Шаг 5: Тестируем модель
    print("\n5️⃣ Тестирую работу модели...")
    if not test_model_response():
        print("\n❌ Модель не отвечает корректно!")
        return False
    
    # Итоговый отчет
    print("\n" + "="*60)
    print("🎉 НАСТРОЙКА ЗАВЕРШЕНА УСПЕШНО!")
    print("="*60)
    print("✅ Ollama установлен и запущен")
    print("✅ Модель gemma2:9b доступна")
    print("✅ Модель отвечает на запросы")
    print("\n🚀 Теперь можно запускать агента:")
    print("   python main.py")
    print("   python test_agent.py")
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)