import pytest

from common.send_message_url import SendReportMessage
from py_page.base_page import BasePage
import time
from common.log import Logger

logger = Logger().get_logger()


@pytest.fixture
def get_driver():
    driver = BasePage().driver
    yield driver
    driver.quit()


# def pytest_terminal_summary(terminalreporter):
#     # pytest_terminal_summary函数是pytest的一个插件钩子函数，用于在所有的测试运行完成后向终端报告总结信息
#     duration = time.time() - terminalreporter._sessionstarttime
#     duration = round(duration, 2)
#
#     test_result = dict(
#         total=terminalreporter._numcollected,
#         deselected=len(terminalreporter.stats.get('deselected', [])),
#         passed=len(terminalreporter.stats.get('passed', [])),
#         failed=len(terminalreporter.stats.get('failed', [])),
#         error=len(terminalreporter.stats.get('error', [])),
#         skipped=len(terminalreporter.stats.get('skipped', [])),
#         total_time=f"{duration}秒"
#     )
#
#     # 计算成功率
#     success_rate = 0
#     if test_result['total'] - test_result['deselected'] > 0:
#         success_rate = round(test_result['passed'] / (test_result['total'] - test_result['deselected']) * 100, 2)
#
#     # 设置状态图标和颜色
#     status_icon = "✅"
#     status_color = "#52c41a"  # 绿色
#     if test_result['failed'] > 0 or test_result['error'] > 0:
#         if success_rate < 80:
#             status_icon = "⚠️"
#             status_color = "#faad14"  # 橙色
#         if success_rate < 60:
#             status_icon = "❌"
#             status_color = "#f5222d"  # 红色
#
#     # 构建ActionCard格式的消息
#     current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
#
#     # 构建进度条（使用简单的字符，避免颜色渲染问题）
#     progress_bar_length = 20
#     passed_blocks = int(progress_bar_length * success_rate / 100)
#     progress_bar = f'<font color="#52c41a">{"█" * passed_blocks}</font>' + '░' * (progress_bar_length - passed_blocks)
#
#     template_card = {
#         "title": "安卓自动化测试报告",
#         "text": f"""# {status_icon} 安卓自动化测试报告
#     ## 🚀 测试结果概览
#
#     | 指标 | 数值 |
#     |:---:|:---:|
#     | 📊 总用例数 | <span style="color:#1890ff">{test_result['total']} 条</span> |
#     | ✅ 通过用例 | <span style="color:#52c41a">{test_result['passed']} 条</span> |
#     | ❌ 失败用例 | <span style="color:#f5222d">{test_result['failed']} 条</span> |
#     | ⚠️ 异常用例 | <span style="color:#f5222d">{test_result['error']} 条</span> |
#     | ⏭️ 跳过用例 | <span style="color:#1890ff">{test_result['skipped']} 条</span> |
#     | 🚫 反选用例 | <span style="color:#1890ff">{test_result['deselected']} 条</span> |
#
#     ## 📊 测试详情
#
#     **成功率**: <span style="color:{status_color}">{success_rate}%</span>
#     **进度**: {progress_bar} {success_rate}%
#     **运行耗时**: ⏱️ {test_result['total_time']}
#     **执行时间**: 🕒 {current_time}
#
#     > 本次测试由自动化测试系统生成
#     """,
#         "buttons": [
#             {
#                 "title": "查看完整报告",
#                 "action_url": "https://jxx.com"  # 替换为实际可访问的HTTPS链接
#             }
#         ],
#         "btn_orientation": "1"  # 按钮水平排列
#     }
#
#     # 发送到企业微信
#     SendReportMessage.send_dingtalk_message(template_card, msg_type="template_card")

# 老版本
# def pytest_terminal_summary(terminalreporter):
#     # pytest_terminal_summary函数是pytest的一个插件钩子函数，用于在所有的测试运行完成后向终端报告总结信息
#     # 即：收集自动化测试结果，然后统一发送到报告中
#     duration = time.time() - terminalreporter._sessionstarttime
#     duration = round(duration, 2)
#
#     test_result = dict(
#         total=terminalreporter._numcollected,
#         deselected=len(terminalreporter.stats.get('deselected', [])),
#         passed=len(terminalreporter.stats.get('passed', [])),
#         failed=len(terminalreporter.stats.get('failed', [])),
#         error=len(terminalreporter.stats.get('error', [])),
#         skipped=len(terminalreporter.stats.get('skipped', [])),
#         total_time=f"{duration}秒"
#     )
#
#     report_str = f'《安卓ui自动化测试报告》\n' \
#                  f'用例执行数: {test_result.get("total")} 条\n' \
#                  f'反选的用例: {test_result.get("deselected")} 条\n' \
#                  f'通过的用例: {test_result.get("passed")} 条\n' \
#                  f'失败的用例: {test_result.get("failed")} 条\n' \
#                  f'异常的用例: {test_result.get("error")} 条\n' \
#                  f'跳过的用例: {test_result.get("skipped")} 条\n' \
#                  f'运行总耗时: {test_result.get("total_time")}'
#
#     logger.info(report_str)
#
#     # 机器人发送自动化测试报告
#     SendReportMessage.send_dingtalk_message(report_str)

# def pytest_terminal_summary(terminalreporter):
#     # 计算测试结果
#     duration = time.time() - terminalreporter._sessionstarttime
#     duration = round(duration, 2)
#
#     test_result = dict(
#         total=terminalreporter._numcollected,
#         deselected=len(terminalreporter.stats.get('deselected', [])),
#         passed=len(terminalreporter.stats.get('passed', [])),
#         failed=len(terminalreporter.stats.get('failed', [])),
#         error=len(terminalreporter.stats.get('error', [])),
#         skipped=len(terminalreporter.stats.get('skipped', [])),
#         total_time=f"{duration}秒"
#     )
#
#     # 创建消息发送对象
#     report_sender = SendReportMessage('https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=13c296d9-ec40-4ecb-b7c7-d6720f9a4269')
#
#     # 正确调用方式：传递三个独立参数
#     report_sender.send_wecom_rich_card(
#         title="📊 安卓UI自动化测试报告",
#         description=f"测试完成时间: {time.strftime('%Y-%m-%d %H:%M:%S')}",
#         statistics=test_result
#     )


# 模拟测试数据
# def mock_terminalreporter():
#     # 创建模拟的terminalreporter对象
#     class MockTerminalReporter:
#         def __init__(self):
#             self._sessionstarttime = time.time() - 100  # 100秒前开始
#             self._numcollected = 200  # 总用例数
#             self.stats = {
#                 'passed': list(range(170)),  # 170个通过用例
#                 'failed': list(range(25)),  # 25个失败用例
#                 'error': list(range(5)),  # 5个异常用例
#                 'skipped': list(range(10)),  # 10个跳过用例
#                 'deselected': []  # 无反选用例
#             }
#
#     return MockTerminalReporter()


# 执行测试
# if __name__ == "__main__":
#     ...
# # 创建模拟的terminalreporter
# terminalreporter = mock_terminalreporter()
#
# # 执行测试报告生成
# pytest_terminal_summary(terminalreporter)
