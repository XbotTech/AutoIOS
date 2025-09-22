import os
import allure
# import pyscreenshot as ImageGrab
# import time
from datetime import datetime

project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def getScreenShot(driver, name):
    print(name)
    currTime = datetime.utcnow().strftime("%m%d%H%M%S.%f")
    filename = project_path + '/screen_shot/' + name + "_" + currTime + '.png'
    driver.save_screenshot(filename)

    allure.attach.file(source=filename, name=f"{name}"+"_"+f"{currTime}", attachment_type=allure.attachment_type.PNG)