# /Users/anjaebeom/Desktop/금오공대/1학년/2학기/자바프로그래밍/java/jp5/src

import getpass
import platform

def get_compile_command(path, file, result):
    for i in enumerate(path.split("/")):
        if i[1].lower() == "desktop":
            print_path = "/".join(path.split("/")[i[0]+1:])
            break
    print_path = "~/" + print_path

    if not file.endswith(".java"):
        result_path = []
        file = print_path.split("/")[-1] + "/" + file
        for i in enumerate(print_path.split("/")):
            if i[0] == len(print_path.split("/")) - 1:
                break
            else:
                result_path.append(i[1])
        result_path = "/".join(result_path)

    else:
        result_path = print_path

    platform_node = platform.node().replace(".local", "")
    result = f"{getpass.getuser()}@{platform_node}-ui-MacBookPro {result_path} $ java {file}\n{result}"
    return result