import getpass
import platform

def get_compile_command(path, file, result):
    path_for_print = ""
    path = path.replace("\\", "/")
    for i in enumerate(path.split("/")):
        if i[1].lower() == "desktop":
            path_for_print = "/".join(path.split("/")[i[0]+1:])
            break
    if path_for_print == "":
        path_for_print = path
    path_for_print = "~/" + path_for_print

    if not file.endswith(".java"):
        result_path = []
        file = path_for_print.split("/")[-1] + "/" + file
        for i in enumerate(path_for_print.split("/")):
            if i[0] == len(path_for_print.split("/")) - 1:
                break
            else:
                result_path.append(i[1])
        result_path = "/".join(result_path)

    else:
        result_path = path_for_print

    platform_node = platform.node().replace(".local", "")
    result = f"{getpass.getuser()}@{platform_node} {result_path} $ java {file}\n{result}"
    return result