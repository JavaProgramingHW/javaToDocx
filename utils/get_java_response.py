import sys
import time
import pexpect

def get_java_pk_response(path, file_name, command):
    result = ""
    child = pexpect.spawn(f'javac {file_name}/{file_name}.java', cwd=path)
    javac = child.read()
    child = pexpect.spawn(f'java {file_name}/{file_name}', cwd=path, encoding='utf-8')

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

    return result

def get_java_response(path, file_name, command):
    result = ""
    child = pexpect.spawn(f'java {file_name}', cwd=path, encoding='utf-8')

    child.logfile = sys.stdout

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

    print()

    return result