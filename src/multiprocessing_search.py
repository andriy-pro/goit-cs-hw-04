from collections import defaultdict
from multiprocessing import Process, Queue

from config import logger
from utils import bm_search


def process_file_mp(file_path, keywords, queue):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
        found_keywords = bm_search(content, keywords)
        # Результат - кортеж (keyword, file_path)
        for keyword in found_keywords:
            queue.put((keyword, file_path))
        logger.info(f"Файл оброблено (process): {file_path}")
    except FileNotFoundError:
        logger.error(f"Файл не знайдено: {file_path}")
    except Exception as e:
        logger.error(f"Помилка обробки {file_path}: {str(e)}")


def _process_files_chunk_mp(files_chunk, keywords, queue):
    for file_path in files_chunk:
        process_file_mp(file_path, keywords, queue)


def search_with_processes(files, keywords, num_processes):
    """
    Виконує багатопроцесорний пошук ключових слів у файлах.
    """
    result_dict = defaultdict(list)
    queue = Queue()
    processes = []

    if num_processes > len(files):
        num_processes = len(files) if len(files) > 0 else 1

    chunk_size = len(files) // num_processes if num_processes else 0
    if chunk_size == 0 and files:
        chunk_size = len(files)

    for i in range(num_processes):
        start_index = i * chunk_size
        end_index = len(files) if i == num_processes - 1 else (i + 1) * chunk_size
        proc_files = files[start_index:end_index]
        p = Process(target=_process_files_chunk_mp, args=(proc_files, keywords, queue))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    # Збирання результатів з черги
    while not queue.empty():
        keyword, file_path = queue.get()
        result_dict[keyword].append(file_path)

    return dict(result_dict)
