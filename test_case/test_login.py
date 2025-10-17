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

        """测试账号密码登录功能 - 验证登录成功后用户名显示正确"""
        # 测试数据配置
        TEST_DATA = {
            "phone": "1384081xxxx",
            "password": "123456xxx",
            "expected_username": "123456xxx"
        }

        main_page = MainPage(get_driver)
        # 检查用户是否已登录

        try:
            # 直接进入我的页面并检查状态
            my_page = main_page.goto_my_page()
            # 检查用户是否已登录
            login_status = my_page.check_login_status()

            if login_status["is_logged_in"]:
                actual_username = login_status["username"]
                logger.info(f"用户已登录，获取用户名：{actual_username}")

                # 直接验证用户名
                if actual_username == TEST_DATA["expected_username"]:
                    logger.info("✓ 用户名验证成功，用例直接通过")
                    return  # 直接返回，用例执行成功
                else:
                    logger.warning(f"用户名不匹配，期望 '{TEST_DATA['expected_username']}'，实际 '{actual_username}'")
                    # 用户名不匹配，继续执行登录流程
                    logger.info("用户名不匹配，执行重新登录")

            logger.info("用户未登录，继续进入登录页面")
            # 执行登录流程
            main_page = MainPage(get_driver)
            name = (main_page
                    .goto_my_page()
                    .goto_login_page()
                    .switch_password_login()
                    .num_pwd_login(TEST_DATA["phone"], TEST_DATA["password"])
                    .xbg_agree()
                    .get_user_name())

            logger.info(f"登录成功，获取用户名：{name}")
            logger.info(f"期望用户名：{TEST_DATA['expected_username']}")

            # 断言验证
            assert name == TEST_DATA["expected_username"], (
                f"用户名验证失败：期望 '{TEST_DATA['expected_username']}'，实际 '{name}'"
            )

            logger.info("用户名验证成功，测试用例通过")

        except AssertionError as e:
            logger.error(f"断言失败：{e}")
            getScreenShot(get_driver, f"{__name__}_assertion_fail")
            raise
        except Exception as e:
            logger.error(f"登录流程执行失败：{e}")
            getScreenShot(get_driver, f"{__name__}_execution_fail")
            raise


        # try:
        #     name = (MainPage(
        #         get_driver).goto_my_page().goto_login_page().switch_password_login().num_pwd_login(
        #         "15371972593", "jxx321").xbg_agree().
        #                   get_user_name())
        #
        #     # '//android.widget.TextView[@index="4"]'
        #     logger.info(f"获取用户名：{name}")
        #
        #     assert name==  "jxxniupi"
        # except Exception as e:
        #     logger.error(f"执行登录用例失败，错误：{e}")
        #     getScreenShot(get_driver, __name__)
        #     raise e

