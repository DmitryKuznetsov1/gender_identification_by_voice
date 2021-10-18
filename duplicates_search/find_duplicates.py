import sys, os
import hashlib
from typing import List


def get_same_size_files(files_paths: List) -> dict:
    same_size = {}
    for filepath in files_paths:
        size = os.path.getsize(filepath)
        if size in same_size:
            same_size[size].append(filepath)
        else:
            same_size[size] = [filepath]
    return same_size


def are_duplicates(filepath_1: str, filepath_2: str, step: int = 256, hash_method_name: str = "sha1") -> bool:
    """
    Проверяет, явлвяются ли дубликатами два файла.
    Предполагается, что они одинаковой длины (иначе вернет неправильный результат), что следует из логики сравнения.
    """
    hash_method = getattr(hashlib, hash_method_name)
    file_1_bytes = b''
    file_2_bytes = b''
    with open(filepath_1, 'rb') as f1, open(filepath_2, 'rb') as f2:
        while True:
            chunk_1 = f1.read(step)
            file_1_bytes += chunk_1
            if chunk_1 == b'':
                return file_1_bytes == file_2_bytes

            hash_1 = hash_method(chunk_1).digest()

            chunk_2 = f2.read(step)
            file_2_bytes += chunk_2
            hash_2 = hash_method(chunk_2).digest()
            if hash_1 != hash_2:
                return False


def get_uniques_and_its_duplicates(same_size_files: List) -> dict:
    """
    Пробегает по каждой группе (файлов одинаковых размеров) и
    """
    uniques_and_its_duplicates = {same_size_files[0]: []}

    for filepath in same_size_files[1:]:
        add_as_new_unique = True
        for unique in uniques_and_its_duplicates:
            if are_duplicates(unique, filepath):
                uniques_and_its_duplicates[unique].append(filepath)
                add_as_new_unique = False
        if add_as_new_unique:
            uniques_and_its_duplicates[filepath] = []
    return uniques_and_its_duplicates


def write_result(output, files_dict: dict):
    with open(output, 'w') as o:
        for unique, duplicates in files_dict.items():
            if duplicates:
                o.write(f"{unique}: {duplicates}\n")


def main(input_dir, output):
    files_in_dir = [f"{input_dir}/" + filename for filename in os.listdir(input_dir)]
    groups = get_same_size_files(files_in_dir)
    all_files = {}
    for size, same_size_files in groups.items():
        if len(same_size_files) == 1:
            # print(same_size_files[0], " has no duplicates")
            all_files.update({same_size_files[0]: []})
        else:
            uniques_and_its_duplicates = get_uniques_and_its_duplicates(same_size_files)
            all_files.update(uniques_and_its_duplicates)
    write_result(output, all_files)


if __name__ == "__main__":
    input_dir = sys.argv[1]
    output = sys.argv[2]
    main(input_dir, output)