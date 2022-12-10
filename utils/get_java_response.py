import os
import time
import shutil
import platform

from utils.get_image import get_image
from utils.misc import get_compile_command

if platform.system() == "Windows":
    import wexpect as pexpect
else:
    import pexpect

def get_java_pk_response(path, file_name, parameter, command, java_response_path):
    result = ""
    child = pexpect.spawn(f'javac {file_name}/{file_name}.java', cwd=path)
    javac = child.read()
    child = pexpect.spawn(f'java {file_name}/{file_name} {parameter if parameter is not None else ""}', cwd=path, encoding='utf-8')

    if command is not None:
        for msg in command:
            time.sleep(0.5)
            child.sendline(msg)
            if child.before is not None:
                result += child.before
                print(child.before)
            if child.after is not None:
                result += child.after
                print(child.after)
    result += child.read()
    print(result)
    print()

    compile_command = get_compile_command(path, file_name, parameter, result)
    image_path = get_image(compile_command)
    if image_path is not None and os.path.exists(image_path):
        shutil.copy(image_path, f"{java_response_path}/{file_name}.png")
        os.remove(image_path)

def get_java_response(path, file_name, parameter, command, java_response_path):
    result = ""
    child = pexpect.spawn(f'java {file_name} {parameter if parameter is not None else ""}', cwd=path, encoding='utf-8')

    if command is not None:
        for msg in command:
            time.sleep(0.5)
            child.sendline(msg)
            if child.before is not None:
                result += child.before
                print(child.before)
            if child.after is not None:
                result += child.after
                print(child.after)
    result += child.read()

    print(result)

    compile_command = get_compile_command(path, file_name, parameter, result)
    image_path = get_image(compile_command)
    if image_path is not None and os.path.exists(image_path):
        shutil.copy(image_path, f"{java_response_path}/{file_name}".replace(".java", ".png"))
        os.remove(image_path)

    return result