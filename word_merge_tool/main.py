import os
from merge_logic import (
    extract_placeholders_from_docx,
    create_excel_template,
    load_excel_data,
    process_document,
    find_template_files,
    TEMPLATE_PREFIX, PARAM_PREFIX
)

# --- Конфигурация ---
MAIN_FOLDER = 'C:/Users/G.Tishchenko/Desktop/Запросы/'
OUTPUT_FOLDER_NAME = MAIN_FOLDER + 'output'

def main():
    print("=" * 50)
    print("--- Генератор документов Word ---")
    print("=" * 50, '\n')

    # Проверка существования папки
    if not os.path.exists(MAIN_FOLDER):
        print(f" ОШИБКА: Папка '{MAIN_FOLDER}' не найдена.")
        return

    # 1. Поиск шаблонов
    templates = find_template_files(MAIN_FOLDER)
    if not templates:
        print(f" ОШИБКА: Не найдено шаблонов вида {TEMPLATE_PREFIX}*.docx")
        print(f"   Создайте файл, например: {TEMPLATE_PREFIX}dogovor.docx")
        return

    # 2. Обработка каждого шаблона
    for tpl in templates:
        template_path = tpl['template']
        param_path = tpl['param_file']
        template_name = tpl['name']

        print("-" * 60)
        print(f"Обработка шаблона: {TEMPLATE_PREFIX}{template_name}.docx")
        print("-" * 60)

        # 3. Проверка наличия Excel файла
        if not os.path.exists(param_path):
            print(f"Файл '{param_path}' не найден.")
            print(f"   Сканирую шаблон для создания Excel-файла...")

            placeholders = extract_placeholders_from_docx(template_path)

            if not placeholders:
                print(f"ОШИБКА: В шаблоне не найдено плейсхолдеров вида {{param}}")
                print(f"   Добавьте в текст метки, например: {{request_number}}")
                print()
                continue

            print(f"   Найдено плейсхолдеров: {len(placeholders)}")
            for ph in placeholders:
                print(f"      • {{{ph}}}")

            create_excel_template(param_path, placeholders)
            print(f" Создан файл: {param_path}")
            print(f"\n Заполните '{PARAM_PREFIX}{template_name}.xlsx' данными и запустите скрипт снова.")
            print()
            continue

        print(f" Файл данных найден: {param_path}")
    #
    #
    #
    #
    #
    #

    # 4. Создание папки для вывода
        output_folder = os.path.join(MAIN_FOLDER, OUTPUT_FOLDER_NAME)
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # 5. Чтение данных из Excel
        try:
            print(f"\n Чтение данных...")
            data_rows = load_excel_data(param_path)

            if not data_rows:
                print(f" В файле нет строк с данными (только заголовки).")
                print(f"   Заполните {PARAM_PREFIX}{template_name}.xlsx и запустите скрипт снова.")
                print()
                continue

            print(f"   Найдено строк для обработки: {len(data_rows)}")

        except Exception as e:
            print(f" ОШИБКА при чтении Excel: {e}")
            print()
            continue

        # 6. Генерация файлов
        print(f"\n Генерация документов...")
        success_count = 0
        error_count = 0

        for i, row_data in enumerate(data_rows, 1):
            filename = row_data['filename']
            output_name = f"{filename}.docx"
            output_path = os.path.join(output_folder, output_name)

            try:
                process_document(template_path, output_path, row_data)
                print(f"   [{i}/{len(data_rows)}] ✓ {output_name}")
                success_count += 1
            except Exception as e:
                print(f"   [{i}/{len(data_rows)}] ❌ {output_name}: {e}")
                error_count += 1

        # 7. Итоговый отчет по шаблону
        print()
        print(f" Успешно создано: {success_count}")
        if error_count > 0:
            print(f"⚠ Ошибок: {error_count}")
        print(f" Результаты в папке: {OUTPUT_FOLDER_NAME}/")
        print()

    print("=" * 60)
    print("--- Завершено ---")
    print("=" * 60)

if __name__ == "__main__":
    main()
