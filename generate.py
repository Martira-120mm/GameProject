#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

# Расширения файлов, которые мы будем включать (можно дополнить)
TEXT_EXTENSIONS = {'.rs', '.toml', '.md', '.txt', '.ron', '.json', '.yml', '.yaml', '.html', '.css', '.js', '.py'}

# Папки, которые нужно игнорировать
IGNORE_DIRS = {'target', '.git', 'debug', 'release', 'node_modules'}


def is_text_file(filename):
    """Проверяет, является ли файл текстовым по расширению."""
    ext = os.path.splitext(filename)[1].lower()
    return ext in TEXT_EXTENSIONS


def collect_files(root_dir):
    """Собирает все текстовые файлы в проекте, пропуская игнорируемые папки."""
    files = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Удаляем из dirnames игнорируемые папки, чтобы os.walk в них не заходил
        dirnames[:] = [d for d in dirnames if d not in IGNORE_DIRS]

        for f in filenames:
            full_path = os.path.join(dirpath, f)
            if is_text_file(f):
                # Относительный путь от корня проекта
                rel_path = os.path.relpath(full_path, root_dir)
                files.append(rel_path)
    # Сортируем для удобства
    files.sort()
    return files


def write_structure(output_file, root_dir, files):
    """Записывает структуру в выходной файл."""
    with open(output_file, 'w', encoding='utf-8') as out:
        for rel_path in files:
            full_path = os.path.join(root_dir, rel_path)
            try:
                with open(full_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            except UnicodeDecodeError:
                # Пропускаем бинарные файлы, которые ошибочно попали
                print(f"Предупреждение: не удалось прочитать {rel_path} (пропущен)", file=sys.stderr)
                continue

            out.write(f"[file name]: {rel_path}\n")
            out.write("[file content begin]\n")
            out.write(content)
            if not content.endswith('\n'):
                out.write('\n')
            out.write("[file content end]\n\n")


def main():
    # Используем текущую папку как корень проекта
    root_dir = os.getcwd()
    output_file = "project_structure.txt"

    print(f"Сканируем проект в папке: {root_dir}")
    files = collect_files(root_dir)
    print(f"Найдено {len(files)} текстовых файлов.")

    write_structure(output_file, root_dir, files)
    print(f"Структура сохранена в файл: {output_file}")


if __name__ == "__main__":
    main()