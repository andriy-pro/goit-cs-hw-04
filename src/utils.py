import os
from time import time

from config import COLORS, RESET, logger


def get_files(directory, extension=".txt"):
    """
    Отримує список файлів із директорії з заданим розширенням.
    """
    try:
        return [
            os.path.join(directory, file)
            for file in os.listdir(directory)
            if file.endswith(extension)
        ]
    except FileNotFoundError:
        logger.error(f"Директорія не знайдена: {directory}")
        return []
    except Exception as e:
        logger.error(f"Помилка читання директорії {directory}: {str(e)}")
        return []


def measure_time(func):
    """
    Декоратор для вимірювання часу виконання функції.
    """

    def wrapper(*args, **kwargs):
        start = time()
        result = func(*args, **kwargs)
        elapsed = time() - start
        logger.info(f"Час виконання '{func.__name__}': {elapsed:.2f} c")
        print(
            f"{COLORS['warning']}Час виконання '{func.__name__}': {elapsed:.2f} с{RESET}"
        )
        return result

    return wrapper


def build_shift_table(pattern):
    """
    Створює таблицю зсувів для алгоритму Боєра-Мура.
    """
    table = {}
    length = len(pattern)
    for index, char in enumerate(pattern[:-1]):
        table[char] = length - index - 1
    table.setdefault(pattern[-1], length)
    return table


def bm_search(text, keywords):
    """
    Застосовує алгоритм Боєра-Мура для пошуку ключових слів у тексті.
    Повертає словник результатів {слово: True} для знайдених слів.
    """
    results = {}
    text_lower = text.lower()

    for word in keywords:
        word_lower = word.lower()
        shift_table = build_shift_table(word_lower)
        i = 0
        word_found = False

        while i <= len(text_lower) - len(word_lower):
            j = len(word_lower) - 1
            while j >= 0 and text_lower[i + j] == word_lower[j]:
                j -= 1
            if j < 0:
                results[word] = True
                word_found = True
                break  # Move to the next keyword after finding a match
            else:
                shift = shift_table.get(
                    text_lower[i + len(word_lower) - 1], len(word_lower)
                )
                i += (
                    shift if shift > 0 else 1
                )  # Ensure at least one character is skipped

        if not word_found:
            logger.info(f"Ключове слово '{word}' не знайдено у тексті.")

    return results


def print_results(title, results):
    print(f"{COLORS['header']}{title}{RESET}")
    for keyword, found_files in results.items():
        filenames = [os.path.basename(file) for file in found_files]
        print(
            f"{COLORS['info']}Ключове слово '{keyword}' знайдено в {COLORS['white']}{len(found_files)}{COLORS['info']} файлах: {COLORS['filename']}{filenames}{RESET}"
        )
