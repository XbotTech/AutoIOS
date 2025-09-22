from py_page.base_page import BasePage


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
        return name, self.my_page_toast_text()

    def my_page_toast_text(self):
        toast_text = self.run_steps(self.yaml_path, "my_page_toast_text")
        return toast_text
