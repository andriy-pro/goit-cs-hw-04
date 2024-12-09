from config import INPUT_DIR, KEYWORDS, NUM_PROCESSES, NUM_THREADS, logger
from multiprocessing_search import search_with_processes
from threaded_search import search_with_threads
from utils import get_files, measure_time, print_results


@measure_time
def run_threaded(files, keywords, num_threads):
    results = search_with_threads(files, keywords, num_threads)
    return results


@measure_time
def run_multiprocessing(files, keywords, num_processes):
    results = search_with_processes(files, keywords, num_processes)
    return results


def main():
    files = get_files(INPUT_DIR)
    if not files:
        logger.info("Файли для обробки не знайдено.")
        return

    # Запуск багатопотокової версії
    logger.info("Початок багатопотокового пошуку")
    threaded_results = run_threaded(files, KEYWORDS, NUM_THREADS)
    print_results("Результати багатопотокового пошуку:", threaded_results)

    # Запуск багатопроцесорної версії
    logger.info("Початок багатопроцесорного пошуку")
    mp_results = run_multiprocessing(files, KEYWORDS, NUM_PROCESSES)
    print_results("Результати багатопроцесорного пошуку:", mp_results)


if __name__ == "__main__":
    main()
