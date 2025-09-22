from py_page.base_page import BasePage


class MainPage(BasePage):
    yaml_path = BasePage.get_yaml_path("main_page.yaml")

    def goto_my_page(self):
        self.run_steps(self.yaml_path, "goto_my_page")
        from py_page.my_page import MyPage
        return MyPage(self.driver)

    def agree(self):
        self.run_steps(self.yaml_path, "agree")
        return self
