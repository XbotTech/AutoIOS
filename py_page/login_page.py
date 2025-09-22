from py_page.base_page import BasePage


class LoginPage(BasePage):
    yaml_path = BasePage.get_yaml_path("login_page.yaml")

    # 手机号号密码登录
    def num_pwd_login(self, phone, pwd):
        self.run_steps(self.yaml_path, "num_pwd_login", phone=phone, pwd=pwd)
        return self

    def xbg_agree(self):
        self.run_steps(self.yaml_path, "xbg_agree")
        from py_page.my_page import MyPage
        return MyPage(self.driver)

    def switch_password_login(self):
        self.run_steps(self.yaml_path, "switch_password_login")
        return self

    def is_button_enabled(self):
        ele = self.run_steps(self.yaml_path, "is_button_enabled")
        text = ele.get_attribute("enabled")
        return text
