import os
import base64

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait

from .get_file_list import get_file_list

def get_uml_image(filename):
    img_file_name = filename + ".png"
    os.system(f"java -jar uml/UMLParserClass.jar {filename} {img_file_name}")
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
    
    return filename