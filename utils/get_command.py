def get_command(code):
    temp_code = code.split("\n")
    if temp_code[0].replace(" ", "") == "/*":
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
    
    return end_index, command_code