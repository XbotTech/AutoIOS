import os
import time
from string import Template
from typing import List

import yaml
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy as By
from appium.webdriver.common.touch_action import TouchAction
from appium.webdriver.webdriver import WebDriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from appium.webdriver.webelement import WebElement
from common.handle_black import handle_black
from common.log import Logger
from appium.options.common import AppiumOptions

logger = Logger().get_logger()


class BasePage:

    def __init__(self, driver: WebDriver = None):

        if not driver:  # 如果没有传递driver
            option = AppiumOptions()
            option.set_capability("platformName", "android")
            option.set_capability("deviceName", "RFCY505MTLP")
            option.set_capability("appPackage", "com.blink.blinkfocos")
            option.set_capability("appActivity", ".SplashActivity")

            self.driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', options=option)
            self.driver.implicitly_wait(10)

        else:
            self.driver = driver

    # 元素定位交互方法封装
    # 查找单个元素
    @handle_black
    def find(self, by, locator) -> WebElement:
        by = by.lower()
        if by == "resource-id":  # resource-id
            by_locator = (By.ID, locator)
        elif by == "content-desc":
            by_locator = (By.ACCESSIBILITY_ID, locator)
        elif by == "class":
            by_locator = (By.CLASS_NAME, locator)
        elif by == "xpath":
            by_locator = (By.XPATH, locator)
        elif by == "uam":
            by_locator = (By.ANDROID_UIAUTOMATOR, locator)
        else:
            raise AttributeError(f"元素定位方式未找到，你传入的是{by}")
        # ele = self.driver.find_elements(*by_locator)
        ele = WebDriverWait(self.driver, 10, poll_frequency=0.05).until(ec.visibility_of_element_located(by_locator),
                                                                        message="元素定位异常")
        return ele

    # 查找多个元素
    @handle_black
    def finds(self, by, locator) -> List[WebElement]:
        by = by.lower()
        if by == "resource-id":  # resource-id
            by_locator = (By.ID, locator)
        elif by == "content-desc":
            by_locator = (By.ACCESSIBILITY_ID, locator)
        elif by == "class":
            by_locator = (By.CLASS_NAME, locator)
        elif by == "xpath":
            by_locator = (By.XPATH, locator)
        else:
            raise AttributeError(f"元素定位方式未找到，你传入的是{by}")
        # ele = self.driver.find_element(*by_locator)
        ele_s = WebDriverWait(self.driver, 10).until(
            ec.visibility_of_all_elements_located(by_locator),
            message="元素定位异常")
        return ele_s

    # 获取安卓系统toast专用方法
    def get_toast_text(self, index):
        """通用方法获取Toast消息"""
        try:
            # 等待Toast出现并获取文本
            toast = WebDriverWait(self.driver, index, poll_frequency=0.05).until(
                ec.presence_of_element_located((By.XPATH, "//android.widget.Toast")),
                message="Toast未出现")
            toast_text = (toast.get_attribute("text")).strip()
            return toast_text
        except TimeoutException:
            return None

            # 尝试所有可能的属性获取方式
            # attributes_to_try = ['text', 'name', 'content-desc', 'label', 'value', 'hint']

            # for attr in attributes_to_try:
            #     try:
            #         value = toast.get_attribute(attr)
            #         print(f"toast.get_attribute('{attr}'): '{value}'")
            #         if value and value.strip():  # 如果获取到非空文本
            #             print(value.strip())
            #             return value.strip()
            #     except Exception as e:
            #         print(f"获取属性 '{attr}' 时出错: {e}")

    # 查找单个元素，进行点击
    @handle_black
    def find_and_click(self, by, locator):
        self.find(by, locator).click()

    # 查找多个元素，对其中一个进行点击
    @handle_black
    def finds_and_click(self, by, locator, index):
        self.finds(by, locator)[index].click()

    # 有这个元素就点击，没有就跳过
    @handle_black
    def find_one_element_exist_click(self, by, locator):
        ele = self.find(by, locator)
        if ele.is_displayed():
            ele.click()
            logger.info(f"点击元素{locator}成功")
        else:
            logger.info(f"元素{locator}不存在,跳过.....")
            ...

    # 通过元素的一个属性去获取该元素的text，如果有这个元素就点击，没有就跳过
    def get_current_auth_mode(self, by, locator, text):
        element = self.find(by, locator)
        current_text = element.text
        if text in current_text:
            element.click()
            logger.info(f"点击元素{locator}成功")
        else:
            logger.info(f"元素{locator}不存在,跳过.....")
            pass

    # 查找单个元素，输入文本
    @handle_black
    def find_and_send(self, by, locator, text):
        self.find(by, locator).send_keys(text)

    # 查找多个元素，对其中一个进行输入
    @handle_black
    def finds_and_send(self, by, locator, index, text):
        self.finds(by, locator)[index].send_keys(text)

    # 查找单个元素，清空文本内容
    @handle_black
    def find_and_clear(self, by, locator):
        self.find(by, locator).clear()

    # 查找多个元素，清空其中一个
    @handle_black
    def finds_and_clear(self, by, locator, index):
        self.finds(by, locator)[index].clear()

    # 获取元素文本
    # @handle_black
    # def find_and_get_text(self, by, locator):
    #     return self.find(by, locator).text

    # # 获取元素属性
    # @handle_black
    # def find_and_get_attribute(self, by, locator, attr_name):
    #     return self.find(by, locator).get_attribute(attr_name)
    #
    # # 判断元素是否显示
    # @handle_black
    # def find_and_is_displayed(self, by, locator):
    #     return self.find(by, locator).is_displayed()
    #
    # # 查找某个文本有没有显示
    # @handle_black
    # def find_and_is_displayed(self,  locator):
    #     return self.find(locator).is_displayed()

    # 上下左右滑动
    def swipe_lrdu(self, direction, scale, t=300):  # 0.8
        size = self.driver.get_window_size()
        width = size["width"]  # 810
        height = size["height"]  # 1000

        x, y = width * 0.5, height * 0.5

        if direction == "up":  # 1300*0.8
            x1 = x
            x2 = x
            y1 = y + height * scale * 0.5
            y2 = y - height * scale * 0.5

        elif direction == "down":
            x1 = x
            x2 = x
            y1 = y - height * scale * 0.5
            y2 = y + height * scale * 0.5

        elif direction == "left":
            y1 = y
            y2 = y
            x1 = x + width * scale * 0.5
            x2 = x - width * scale * 0.5

        elif direction == "right":
            y1 = y
            y2 = y
            x2 = x + width * scale * 0.5
            x1 = x - width * scale * 0.5
        else:
            raise AttributeError(f"滑动方向错误，你滑动的方向是{direction}")

        self.driver.swipe(x1, y1, x2, y2, t)

    # 隐私协议专用滑动
    def scroll_privacy_agreement(self, times):
        # 获取当前屏幕尺寸
        window_size = self.driver.get_window_size()
        screen_width = window_size['width']
        screen_height = window_size['height']

        # 计算比例
        start_x_ratio = 0.47
        start_y_ratio = 0.67
        end_y_ratio = 0.33
        times = int(times)
        # 使用比例滑动（适配任意设备）
        for _ in range(times):
            new_start_x = screen_width * start_x_ratio
            new_start_y = screen_height * start_y_ratio
            new_end_y = screen_height * end_y_ratio

            # action = TouchAction(self.driver)
            # action.press(x=new_start_x, y=new_start_y).wait(500).move_to(x=new_start_x, y=new_end_y).release().perform()
            # time.sleep(0.5)

            # 使用W3C标准的触摸操作
            actions = ActionChains(self.driver)
            actions.w3c_actions = ActionBuilder(self.driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))

            # 移动到起始位置并按下
            actions.w3c_actions.pointer_action.move_to_location(new_start_x, new_start_y)
            actions.w3c_actions.pointer_action.pointer_down()

            actions.w3c_actions.pointer_action.pause(0.5)

            # 移动到结束位置
            actions.w3c_actions.pointer_action.move_to_location(new_start_x, new_end_y)

            # 释放
            actions.w3c_actions.pointer_action.pointer_up()

            # 执行所有动作
            actions.perform()

            time.sleep(1)

    def run_steps(self, yaml_path, page_function, **kwargs):
        with open(yaml_path, mode="r", encoding="utf-8") as f:
            res = yaml.safe_load(f)
        steps = res[page_function]

        # logger.info(f"传入的自定义参数是{kwargs}")

        for k, v in kwargs.items():  # {"tel":'"13012312300"'}
            if isinstance(v, str):
                kwargs[k] = f"'{v}'"

        for step in steps:
            step = yaml.dump(step)

            step = Template(step).substitute(kwargs)
            step = yaml.safe_load(step)

            sleep_time = step.get("sleep")
            if sleep_time:
                time.sleep(sleep_time)
                print(f'睡眠了{sleep_time}秒')
            action = step["action"]
            index = step["index"]
            locator = step["locator"]
            text = step["text"]
            try:
                if action == "find_and_click":
                    self.find_and_click(*locator)
                    logger.info(f"调用了 find_and_click 方法, 定位方式是 {locator}")
                elif action == "find":
                    ele = self.find(*locator)
                    logger.info(f"调用了 find 方法, 定位方式是 {locator}")
                    return ele
                elif action == "finds":
                    ele = self.finds(*locator)
                    logger.info(f"调用了 finds 方法, 定位方式是 {locator}")
                    return ele

                elif action == "finds_and_click":
                    self.finds_and_click(*locator, index)
                    logger.info(f"调用了 finds_and_click 方法, 定位方式是 {locator},下标 {index}")
                elif action == "find_and_send":
                    self.find_and_send(*locator, text)
                    logger.info(f"调用了 find_and_send 方法, 定位方式是 {locator},输入的文本 {text}")
                elif action == "find_one_element_exist_click":
                    self.find_one_element_exist_click(*locator)
                    logger.info(f"调用了 find_one_element_exist_click 方法, 定位方式是 {locator}")
                elif action == "get_current_auth_mode":
                    self.get_current_auth_mode(*locator, text)
                    logger.info(f"调用了 find_one_element_exist_click 方法, 定位方式是 {locator},要获取的文本 {text}")
                elif action == "finds_and_send":
                    self.finds_and_send(*locator, index, text)
                    logger.info(f"调用了 finds_and_send 方法, 定位方式是 {locator},下标 {index},输入的文本 {text}")
                elif action == "find_and_clear":
                    self.find_and_clear(*locator)
                    logger.info(f"调用了 find_and_clear 方法, 定位方式是 {locator}")
                elif action == "finds_and_clear":
                    self.finds_and_clear(*locator, index)
                    logger.info(f"调用了 finds_and_clear 方法, 定位方式是 {locator},下标 {index}")
                elif action == "swipe_lrdu":
                    self.swipe_lrdu(*index)
                    logger.info(f"调用了 swipe_lrdu 方法, 方向 {index[0]}  幅度{index[1]}")
                elif action == "scroll_privacy_agreement":
                    self.scroll_privacy_agreement(index)
                    logger.info(f"调用了 scroll_privacy_agreement 方法, 滑动了隐私协议")
                elif action == "get_toast_text":
                    result = self.get_toast_text(index)
                    logger.info(f"调用了 get_toast_text 方法 ,获取到的文本是{result}")
                    return result

                else:
                    raise AttributeError(f"你的元素定位交互方法 {action} 没有找到，再检查一下哦！")
            except Exception as e:
                logger.error(
                    f"元素定位交互异常，执行的操作是{action},传入的参数 定位方式{locator}::下标{index}::文本{text}::等待时间{sleep_time}")
                logger.error(f"报错信息是  {e}")
                raise e

    @staticmethod
    def get_yaml_path(yaml_file_name):
        path = os.path.abspath(__file__)  # 获取base_page.py的绝对路径
        py_page_path = os.path.dirname(path)  # 获取base_page.py所在的文件夹 py_page
        project_path = os.path.dirname(py_page_path)  # py_page所在的文件夹
        yaml_path = os.path.join(project_path, "py_yaml", yaml_file_name)
        return yaml_path


if __name__ == '__main__':
    ...
    # basepage = BasePage()
    # p = BasePage.get_yaml_path("main_page.yaml")
    # basepage.run_steps(p, "agree",tel="13012312300.")
    # time.sleep(10)
    #
    # basepage.find_and_click(By.XPATH, "//*[@text='同意']")
    # time.sleep(10)
    #
    # basepage.driver.quit()

    # basepage.swipe_lrdu("up",0.8)
    # time.sleep(3)
    # basepage.swipe_lrdu("down",0.6)
    # time.sleep(1)
    #
    # basepage.swipe_lrdu("left",0.8)
    # time.sleep(1)
    #
    # # basepage.swipe_lrdu("aaaa",0.8)
    # time.sleep(3)
