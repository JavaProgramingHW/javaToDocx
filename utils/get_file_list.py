import os
import natsort

def get_file_list(path):
    """ 파일명은 Hw(챕터)_(문제번호) 로 통일한다. ex. Hw1_1 """
    file_list = []

    for file in os.listdir(path):
        if (file.endswith(".java") or os.path.isdir(f"{path}/{file}") or file.endswith(".json")) and file[0] != ".":
            file_list.append(file)

    file_list = natsort.natsorted(file_list)

    return file_list