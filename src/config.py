import logging
import os
from datetime import datetime

from colorama import Fore, Style

# Налаштування для MongoDB, PostgreSQL, та інші (не потрібно тут, залишено як приклад)
# Зараз використовується лише для логування та шляхи до файлів

# Шлях до вхідної директорії з файлами
INPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "input")

# Ключові слова для пошуку
KEYWORDS = [
    "немає",
    "значення",
    "зима",
    "сніг",
    "літо",
    "сонце",
    "москалі",
    "мають",
    "дохнуть",
    "донать",
    "на",
    "русоріз",
]

# Кількість потоків/процесів
NUM_THREADS = 4
NUM_PROCESSES = 4

# Налаштування логування
LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
LOG_FILE = os.path.join(LOG_DIR, f"search_app_{timestamp}.log")

LOG_LEVEL = logging.INFO
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"

logging.basicConfig(filename=LOG_FILE, level=LOG_LEVEL, format=LOG_FORMAT)
logger = logging.getLogger(__name__)

# Кольори для виводу
RESET = Style.RESET_ALL
COLORS = {
    "info": Fore.GREEN,
    "warning": Fore.YELLOW,
    "error": Fore.RED,
    "header": Fore.CYAN,
    "filename": Fore.LIGHTBLACK_EX,
    "white": Fore.WHITE,
}
