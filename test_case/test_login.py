from common.screen_shot import getScreenShot
from py_page.main_page import MainPage
from common.log import Logger
from appium.webdriver.common.appiumby import AppiumBy
import allure

logger = Logger().get_logger()


@allure.feature("登录模块")  # 整个类都属于这个Feature
class TestLoginPage:
    @allure.story("手机密码登录")
    @allure.title("有效手机号和密码可以登录")
    def test_num_pwd_right(self, get_driver):
        try:
            name = (MainPage(
                get_driver).goto_my_page().goto_login_page().switch_password_login().num_pwd_login(
                "15371972593", "jxx321").xbg_agree().
                          get_user_name())

            # '//android.widget.TextView[@index="4"]'
            logger.info(f"获取用户名：{name}")

            assert name==  "jxx"
        except Exception as e:
            logger.error(f"执行登录用例失败，错误：{e}")
            getScreenShot(get_driver, __name__)
            raise e

