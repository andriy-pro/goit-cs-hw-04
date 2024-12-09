from faker import Faker

from config import INPUT_DIR, logger

fake = Faker("uk_UA")

# Список файлів для генерації
files = [f"{INPUT_DIR}/test_file_{i}.txt" for i in range(1, 11)]


def generate_text(file_path, num_sentences=10000):
    """
    Генерує випадковий текст українською мовою та записує його у файл.
    """
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            for _ in range(num_sentences):
                file.write(fake.sentence() + "\n")
        logger.info(f"Файл створено: {file_path}")
    except Exception as e:
        logger.error(f"Помилка створення файлу {file_path}: {str(e)}")


def main():
    for file in files:
        generate_text(file)


if __name__ == "__main__":
    main()
