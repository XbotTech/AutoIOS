import time

from appium.webdriver.common.appiumby import AppiumBy as By
from common.log import Logger
from functools import wraps
from typing import List, Tuple, Callable, Any


'''
basepage.find/finds 方法的装饰器，用于处理黑名单弹框，保证业务进行
'''
logging = Logger(__name__).get_logger()

'''
优化点：
1、支持动态配置黑名单、重试次数等参数
2、保留原始异常信息，提供详细日志
3、支持多次重试和自定义延迟
4、将黑名单处理逻辑提取为独立函数
'''

class BlackListConfig:
    """黑名单配置类"""
    DEFAULT_BLACK_LIST = [
        (By.XPATH, '//XCUIElementTypeButton[@name="Frame"]'),
        # 可以添加更多默认黑名单元素
    ]

    def __init__(self, black_list: List[Tuple] = None, retry_delay: float = 1.0, max_retries: int = 1):
        self.black_list = black_list or self.DEFAULT_BLACK_LIST
        self.retry_delay = retry_delay
        self.max_retries = max_retries

def _handle_black_elements(driver, black_list: List[Tuple], retry_delay: float) -> bool:
    """
    处理黑名单元素

    Args:
        driver: WebDriver实例
        black_list: 黑名单元素列表
        retry_delay: 重试延迟时间

    Returns:
        bool: 是否成功处理了黑名单元素
    """
    for black_locator in black_list:
        try:
            logging.info(f"检查黑名单元素: {black_locator}")
            elements = driver.find_elements(*black_locator)
            if elements and elements[0].is_displayed():
                logging.info(f"找到并点击黑名单元素: {black_locator}")
                elements[0].click()
                time.sleep(retry_delay)
                return True
        except Exception as e:
            logging.debug(f"处理黑名单元素 {black_locator} 时发生异常: {str(e)}")
            continue

    return False

def handle_black(fun):
    """简化版黑名单处理装饰器"""
    config = BlackListConfig()

    @wraps(fun)
    def run(*args, **kwargs):

        by_self = args[0] if args else None

        try:
            return fun(*args, **kwargs)
        except Exception as e:
            if by_self and hasattr(by_self, 'driver'):
                if _handle_black_elements(by_self.driver, config.black_list, config.retry_delay):
                    return fun(*args, **kwargs)
            raise e

    return run

# def handle_black(fun):
#     def run(*args, **kwargs):
#         # 核心修改：直接判断函数名
#         # if fun.__name__ == "get_toast_text":
#         #     # 直接执行并返回结果，不进行任何异常处理
#         #     return fun(*args, **kwargs)
#
#         # 原有黑名单逻辑（仅处理非Toast函数）
#         black_list = [(By.XPATH, '//XCUIElementTypeButton[@name="Frame"]')]
#         by_self = args[0]
#
#         try:
#             return fun(*args, **kwargs)
#         except Exception as e:
#             # 非Toast函数仍执行黑名单处理
#             for black in black_list:
#                 logging.info(f"处理黑名单元素: {black}")
#                 eles = by_self.driver.find_elements(*black)
#                 if eles:
#                     eles[0].click()
#                     time.sleep(1)
#                     return fun(*args, **kwargs)
#             raise e
#
#     return run




