# 이미지 추가 :
# from docx.shared import Inches
# document.add_picture('path', width=Inches(1.25))

import re
import logging
from docx import Document
from docx.shared import RGBColor, Pt

from utils.get_file_list import get_file_list

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
    document.add_page_break() # 다음 페이지로

    # 코드 가져오기
    code_date = open(f"{path}/{file}", "r", encoding = 'UTF-8')
    code = code_date.read()
    code_date.close()

    # 문제 제목 뽑아내기
    temp = file.split("_")
    after_list = []
    for i in temp:
        after_list.append(re.sub(r'[^0-9]', '', i))

    cell_title = ".".join(after_list)

    LOGGER.info(f"{file} - 작성 중. . .")

    # 문제 제목 넣기 - ex. 1.1
    p = document.add_heading(level=1)
    wp = p.add_run(cell_title)
    wp.font.size = Pt(20) # 글자 크기 조절
    wp.font.color.rgb = RGBColor(0, 0, 0) # 글자 색깔 검정색으로

    # 테이블 작성
    table = document.add_table(rows=1, cols=1)
    table.style = "Table Grid"

    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = code
    row_cells = table.add_row().cells
    #row_cells[0].text = 결과 이미지 추가 업데이트 예정

    LOGGER.info(f"{file} - 작성 완료!")

# 저장
document.save('result.docx')