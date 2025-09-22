import os

pytest_cmd = 'pytest -vs --alluredir="./AllureData" --reruns 1 --reruns-delay 1'

allure_cmd = 'allure generate "./AllureData" -o "./AllureReport" --clean'

os.system(pytest_cmd)
os.system(allure_cmd)
