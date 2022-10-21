import os

def get_uml_image(filename):
    img_file_name = filename + ".png"
    os.system(f"java -jar uml/UMLParserClass.jar {filename} {img_file_name}")
    return img_file_name