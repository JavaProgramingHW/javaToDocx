def get_command(code):
    temp_code = code.split("\n")

    # 만약 맨 첫줄이 # 으로 시작하는 매개변수 코드라면
    parameter = None
    command_start_index = 0
    if temp_code[0][0] == "#":
        # 매개변수 코드
        parameter = temp_code[0][1:]
        command_start_index = 1

    if temp_code[command_start_index].replace(" ", "") == "/*":
        command_code = []
        for i in enumerate(temp_code):
            if i[1].replace(" ", "") == "*/":
                end_index = i[0]
                break
            elif i[1].replace(" ", "") == "/*":
                pass
            else:
                command_code.append(i[1])

    else:
        end_index = None
        command_code = None
    
    return parameter, end_index, command_code