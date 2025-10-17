from datetime import time
from typing import Optional, Dict, Any

from py_page.base_page import BasePage, logger


class MyPage(BasePage):
    yaml_path = BasePage.get_yaml_path("my_page.yaml")

    # 点击登录，跳转到登录页面
    def goto_login_page(self):
        self.run_steps(self.yaml_path, "goto_login_page")
        from py_page.login_page import LoginPage
        return LoginPage(self.driver)

    # 获取登录用户名
    def get_user_name(self):
        ele = self.run_steps(self.yaml_path, "get_user_name")
        name = ele.text
        return name

    def my_page_toast_text(self):
        toast_text = self.run_steps(self.yaml_path, "my_page_toast_text")
        return toast_text

    """获取详细的登录状态"""
    def check_login_status(self) -> Dict[str, Any]:
        """用于判断账号是否为登录状态"""
        try:
            username = self.get_user_name()
            is_logged_in = self.is_user_logged_in(username)

            return {
                "is_logged_in": is_logged_in,
                "username": username,
            }
        except Exception as e:
            logger.error(f"获取登录状态失败: {e}")
            return {
                "is_logged_in": False,
                "username": None,
                "error": str(e)
            }

    def is_user_logged_in(self, username: Optional[str]) -> bool:
        """判断用户是否已登录"""
        if not username:
            return False

        # 未登录状态的典型文本
        not_logged_in_texts = [
            "未登录", "登录/注册", "点击登录", "立即登录",
            "请登录", "登录", "Sign in", "Login"
        ]

        # 如果包含未登录文本，返回False
        for text in not_logged_in_texts:
            if text in username:
                return False

        # 有效用户名的基本要求
        return len(username.strip()) >= 2 and not username.strip().isdigit()

