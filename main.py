# 이미지 추가 :
# from docx.shared import Inches
# document.add_picture('path', width=Inches(1.25))

import os
import re
import json
import shutil
import logging
import datetime
from docx import Document
from docx.shared import RGBColor, Pt

from utils.get_file_list import get_file_list
from utils.get_command import get_command
from utils.get_java_response import get_java_response, get_java_pk_response
from utils.get_image import get_image
from utils.misc import get_compile_command
from utils.uml import get_uml_image

version = "1.2.1"

userdata_path = "userdata.json"

# enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO)
LOGGER = logging.getLogger(__name__)

os.system("java --version")
print()
LOGGER.info(f"javaToDocx Version {version}")
LOGGER.info("Made by @ajb3296")
print()
path = input("대상 경로를 입력하세요 : ").strip()
homework_name = input("과제명을 입력하세요 : ").strip()


grade = None
studentID = None
name = None

if os.path.exists(userdata_path):
    file = open(userdata_path, "r", encoding = 'UTF-8')
    data = file.read()
    file.close()
    json_object = json.loads(data)
    if json_object["year"] == str(datetime.datetime.now().year):
        grade = json_object["grade"]
        studentID = json_object["studentID"]
        name = json_object["name"]

if name is None:
    grade = input("학년을 입력하세요(ex. 1) : ").strip()
    studentID = input("학번을 입력하세요(ex. 20220101) : ").strip()
    name = input("이름을 입력하세요(ex. 홍길동) : ").strip()

    file = open(userdata_path, "w", encoding = 'UTF-8')
    file.write(f"""{{
    "year": "{datetime.datetime.today().year}",
    "grade": "{grade}",
    "studentID": "{studentID}",
    "name": "{name}"
}}
""")
    file.close()

else:
    ...

file_list = get_file_list(path)
LOGGER.info(f"대상 파일 리스트 - {file_list}")

document = Document()

p = document.add_heading(level=0)
wp = p.add_run("자바프로그래밍")
wp.font.color.rgb = RGBColor(0, 0, 0)
p = document.add_heading(level=1)
wp = p.add_run(homework_name)
wp.font.color.rgb = RGBColor(0, 0, 0)

p = document.add_heading(level=3)
wp = p.add_run(f"금오공과대학교 컴퓨터소프트웨어공학과\n{grade}학년 {studentID} {name}")
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

        # 설계
        # temp_path 가 복사할 폴더
        try:
            shutil.rmtree(file)
        except FileNotFoundError:
            pass

        shutil.copytree(temp_path, file)
        imgfile_name = get_uml_image(file)
        img_path = f"{file}/{imgfile_name}"

        # 테이블에 UML class diagram 이미지 추가
        hdr_cells = table.rows[0].cells

        if os.path.exists(img_path):
            paragraph = hdr_cells[0].paragraphs[0]
            run = paragraph.add_run()
            run.add_picture(img_path)
        else:
            hdr_cells[0].text = f"설계 : UML class diagram - 이미지 생성 실패"

        # 임시폴더 제거
        try:
            shutil.rmtree(file)
        except FileNotFoundError:
            pass

        # 테이블 내용 넣기
        for i in enumerate(temp_file_list_processing):
            code_date = open(f"{temp_path}/{i[1]}", "r", encoding = 'UTF-8')
            code = code_date.read()
            code_date.close()

            if i[1] == f"{file}.java":
                end_index, command = get_command(code)
                result = ""
                result = get_java_pk_response(path, file, command)
                
                # 커맨드 적은 주석 제거
                if end_index is not None:
                    temp_code = code.split("\n")
                    code = "\n".join(temp_code[end_index+1:])

            # 코드
            row_cells = table.add_row().cells
            row_cells[0].text = f"//{i[1]}\n\n{code}"

        row_cells = table.add_row().cells

        # 터미널로 속이기
        print(result)
        compile_command = get_compile_command(temp_path, file, result)

        # 이미지 경로 가져오기
        image_path = get_image(compile_command)

        paragraph = row_cells[0].paragraphs[0]
        run = paragraph.add_run()
        run.add_picture(image_path)

        if os.path.exists(image_path):
            os.remove(image_path)
        
        row_cells = table.add_row().cells
        row_cells[0].text = f"난이도 : 중"

        row_cells = table.add_row().cells
        row_cells[0].text = f"완성도 : 정상 실행됨"

    else:
        # 코드 가져오기
        code_date = open(f"{temp_path}/{file}", "r", encoding = 'UTF-8')
        code = code_date.read()
        code_date.close()

        end_index, command = get_command(code)
        result = ""
        result = get_java_response(temp_path, file, command)

        # 커맨드 적은 주석 제거
        if end_index is not None:
            temp_code = code.split("\n")
            code = "\n".join(temp_code[end_index + 1:])

        # 테이블 작성
        table = document.add_table(rows=1, cols=1)
        table.style = "Table Grid"

        # 설계
        hdr_cells = table.rows[0].cells

        # 설계
        # temp_path 가 복사할 폴더
        file_for_uml = file.split(".")[0]
        try:
            shutil.rmtree(file_for_uml)
        except FileNotFoundError:
            pass
        os.mkdir(file_for_uml)
        
        shutil.copy(f"{temp_path}/{file}", file_for_uml)
        imgfile_name = get_uml_image(file_for_uml)
        img_path = f"{file_for_uml}/{imgfile_name}"

        # 테이블에 UML class diagram 이미지 추가
        hdr_cells = table.rows[0].cells

        if os.path.exists(img_path):
            paragraph = hdr_cells[0].paragraphs[0]
            run = paragraph.add_run()
            run.add_picture(img_path)
        else:
            hdr_cells[0].text = f"설계 : UML class diagram - 이미지 생성 실패"

        # 임시폴더 제거
        try:
            shutil.rmtree(file_for_uml)
        except FileNotFoundError:
            pass

        # 코드
        row_cells = table.add_row().cells
        row_cells[0].text = code
        
        row_cells = table.add_row().cells

        # 터미널로 속이기
        compile_command = get_compile_command(temp_path, file, result)

        # 이미지 경로 가져오기
        image_path = get_image(compile_command)

        paragraph = row_cells[0].paragraphs[0]
        run = paragraph.add_run()
        run.add_picture(image_path)

        if os.path.exists(image_path):
            os.remove(image_path)
        
        row_cells = table.add_row().cells
        row_cells[0].text = f"난이도 : 중"

        row_cells = table.add_row().cells
        row_cells[0].text = f"완성도 : 정상 실행됨"

    LOGGER.info(f"{file} - 작성 완료!")

# 저장
document.save('result.docx')