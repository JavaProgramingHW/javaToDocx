import os
import base64
import shutil

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait

from .get_file_list import get_file_list

from umlib.Java2UML import Java2UML

def get_uml_image(filename, img_file_name):
    temp_img_file_name = img_file_name.replace("\\", "/").split('/')[-1]
    os.system(f"java -jar uml/UMLParserClass.jar {filename} {temp_img_file_name}")
    if not os.path.exists(f"{filename}/{temp_img_file_name}"):
        return None
    else:
        shutil.copy(f"{filename}/{temp_img_file_name}", img_file_name)
        os.remove(f"{filename}/{temp_img_file_name}")
    return img_file_name

def get_code_for_uml(path):
    code_list = get_file_list(path)
    code = ""
    for file in code_list:
        with open(f"{path}/{file}", "r") as f:
            code = code + "\n" + f.read()
    
    return code

def get_uml_image_from_viz(filename, code):
    url = "http://viz-js.com/"

    # DRIVER_SETTING
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")
    cap = DesiredCapabilities().CHROME
    cap["marionette"] = True
    options.add_experimental_option("excludeSwitches", ["enable-logging"])

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)

    # 코드 입력
    code = code.replace('\n', '')
    driver.execute_script(f"ace.edit('editor').setValue('{code}');")

    # 이미지 설정
    select = Select(driver.find_element(By.XPATH, '//*[@id="format"]/select'))
    select.select_by_visible_text('png-image-element')

    # 이미지 저장
    WebDriverWait(driver,timeout=10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="output"]/img')))
    img = driver.find_element(By.XPATH, '//*[@id="output"]/img').get_attribute('src')
    imgdata = base64.b64decode(img.replace('data:image/png;base64,', ''))
    with open(filename, 'wb') as f:
        f.write(imgdata)
    
    # 웹 닫기
    driver.quit()
    
    return filename

def download_uml_class_diagram_img(from_file, to_img):
    # 이미지 1차 다운로드
    imgfile_name = get_uml_image(from_file, to_img)

    # 이미지 생성에 실패했을 경우
    if imgfile_name is None:
        # 코드 합치기
        code = get_code_for_uml(from_file)
        try:
            # 코드 변환
            uml_result = str(Java2UML().JavaCode2UML(code))
            # UML 이미지 생성
            imgfile_name = get_uml_image_from_viz(to_img, uml_result)
        except:
            pass