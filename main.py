# 이미지 추가 :
# from docx.shared import Inches
# document.add_picture('path', width=Inches(1.25))

import os
import re
import logging
from docx import Document
from docx.shared import RGBColor, Pt

from utils.get_file_list import get_file_list
from utils.get_command import get_command
from utils.get_java_response import get_java_response, get_java_pk_response
from utils.get_image import get_image

version = "1.0.1"

if not os.path.exists("image"):
    os.makedirs("image")

# enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO)
LOGGER = logging.getLogger(__name__)

path = input("대상 경로를 입력하세요 : ")
name = input("학번과 이름을 입력하세요(ex. 20220101 홍길동) : ")

file_list = get_file_list(path)
LOGGER.info(f"대상 파일 리스트 - {file_list}")

document = Document()

p = document.add_heading(level=0)
wp = p.add_run(name)
wp.font.color.rgb = RGBColor(0, 0, 0)

for file in file_list:
    LOGGER.info(f"{file} - 작성 중. . .")

    document.add_page_break() # 다음 페이지로

    # 문제 제목 뽑아내기
    temp = file.split("_")
    after_list = []
    for i in temp:
        after_list.append(re.sub(r'[^0-9]', '', i))
    cell_title = ".".join(after_list)

    # 문제 제목 넣기 - ex. 1.1
    p = document.add_heading(level=1)
    wp = p.add_run(cell_title)
    wp.font.size = Pt(20) # 글자 크기 조절
    wp.font.color.rgb = RGBColor(0, 0, 0) # 글자 색깔 검정색으로


    temp_path = path
    # 파일 확장자가 .java 가 아닐 경우 - 즉 패키지일 경우
    if not file.endswith(".java"):
        temp_path = f"{path}/{file}"

        temp_file_list = get_file_list(temp_path)

        temp_file_list_processing = []
        file_java_exist = False
        for i in temp_file_list:
            # 만약 폴더명과 동일한 이름의 java 파일이 아닐 경우 추가 - 이를 리스트의 맨 위에 올리기 위함
            if i != f"{file}.java":
                temp_file_list_processing.append(i)
            else:
                file_java_exist = True

        # 리스트의 맨 앞에 추가
        if file_java_exist:
            temp_file_list_processing.insert(0, f"{file}.java")

        # 테이블 작성
        table = document.add_table(rows=1, cols=1)
        table.style = "Table Grid"

        # 테이블 내용 넣기
        for i in enumerate(temp_file_list_processing):
            code_date = open(f"{temp_path}/{i[1]}", "r", encoding = 'UTF-8')
            code = code_date.read()
            code_date.close()

            if i[1] == f"{file}.java":
                end_index, command = get_command(code)
                result = ""
                result = get_java_pk_response(path, file, command)

                hdr_cells = table.rows[0].cells
                hdr_cells[0].text = f"//{i[1]}\n\n{code}"
            else:
                row_cells = table.add_row().cells
                row_cells[0].text = f"//{i[1]}\n\n{code}"

        row_cells = table.add_row().cells

        # 이미지 경로 가져오기
        image_path = get_image(result, file)

        paragraph = row_cells[0].paragraphs[0]
        run = paragraph.add_run()
        run.add_picture(image_path)

        if os.path.exists(image_path):
            os.remove(image_path)

    else:
        # 코드 가져오기
        code_date = open(f"{temp_path}/{file}", "r", encoding = 'UTF-8')
        code = code_date.read()
        code_date.close()

        end_index, command = get_command(code)
        result = ""
        result = get_java_response(temp_path, file, command)

        if end_index is not None:
            temp_code = code.split("\n")
            code = "\n".join(temp_code[end_index+1:])

        # 테이블 작성
        table = document.add_table(rows=1, cols=1)
        table.style = "Table Grid"

        hdr_cells = table.rows[0].cells
        hdr_cells[0].text = code
        
        row_cells = table.add_row().cells

        # 이미지 경로 가져오기
        image_path = get_image(result, file)

        paragraph = row_cells[0].paragraphs[0]
        run = paragraph.add_run()
        run.add_picture(image_path)

        if os.path.exists(image_path):
            os.remove(image_path)

    LOGGER.info(f"{file} - 작성 완료!")

# 저장
document.save('result.docx')