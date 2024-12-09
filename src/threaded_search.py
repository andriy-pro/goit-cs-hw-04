import threading
from collections import defaultdict

from config import logger
from utils import bm_search


def process_file(file_path, keywords, result_dict, lock):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
        found_keywords = bm_search(content, keywords)
        with lock:
            for keyword in found_keywords:
                result_dict[keyword].append(file_path)
        logger.info(f"Файл оброблено (thread): {file_path}")
    except FileNotFoundError:
        logger.error(f"Файл не знайдено: {file_path}")
    except Exception as e:
        logger.error(f"Помилка обробки {file_path}: {str(e)}")


def _process_files_chunk(files_chunk, keywords, result_dict, lock):
    for file_path in files_chunk:
        process_file(file_path, keywords, result_dict, lock)


def search_with_threads(files, keywords, num_threads):
    """
    Виконує багатопотоковий пошук ключових слів у файлах.
    """
    result_dict = defaultdict(list)
    lock = threading.Lock()
    threads = []
    if num_threads > len(files):
        num_threads = len(files) if len(files) > 0 else 1

    chunk_size = len(files) // num_threads if num_threads else 0
    if chunk_size == 0 and files:
        chunk_size = len(files)  # Якщо файлів менше ніж потоків, все в один chunk

    for i in range(num_threads):
        start_index = i * chunk_size
        end_index = len(files) if i == num_threads - 1 else (i + 1) * chunk_size
        thread_files = files[start_index:end_index]
        t = threading.Thread(
            target=_process_files_chunk,
            args=(thread_files, keywords, result_dict, lock),
        )
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    return dict(result_dict)
