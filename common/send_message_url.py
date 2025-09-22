import requests
import json
import time


class SendReportMessage:
    def __init__(self, webhook_url: str):
        """
        企业微信消息发送器（正式版）
        :param webhook_url: 企业微信机器人Webhook地址
        """
        self.webhook_url = webhook_url
        self.headers = {'Content-Type': 'application/json'}

    def send_wecom_rich_card(
            self,
            title: str,
            description: str,
            statistics: dict
    ) -> dict:
        """
        发送企业微信富文本卡片消息（正式发送）
        :param title: 主标题
        :param description: 副标题/描述
        :param statistics: 统计信息字典
        :return: 企业微信API响应
        """
        # 构建payload（严格遵循企业微信规范）
        payload = {
            "msgtype": "template_card",
            "template_card": {
                "card_type": "text_notice",
                "source": {
                    "icon_url": "https://example.com/logo.png",
                    "desc": "自动化测试报告"
                },
                "main_title": {
                    "title": title,
                    "desc": description
                },
                "emphasis_content": [
                    {
                        "title": "测试结果",
                        "desc": f"通过率: <font color='info'>{statistics['passed'] / statistics['total'] * 100:.1f}%</font>"
                    }
                ],
                "horizontal_content_list": [
                    {"key": "总用例数", "value": str(statistics['total']), "type": 1},
                    {"key": "通过用例", "value": f"<font color='info'>{statistics['passed']}</font>", "type": 1},
                    {"key": "失败用例", "value": str(statistics['failed']), "type": 1},
                    {"key": "异常用例", "value": str(statistics['error']), "type": 1},
                    {"key": "跳过用例", "value": str(statistics['skipped']), "type": 1}
                ]
            }
        }

        try:
            # 实际发送请求
            response = requests.post(
                url=self.webhook_url,
                data=json.dumps(payload),
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            # 返回标准错误格式
            return {
                "errcode": 500,
                "errmsg": f"HTTP请求失败: {str(e)}",
                "webhook_url": self.webhook_url
            }
        except Exception as e:
            # 捕获其他异常
            return {
                "errcode": 500,
                "errmsg": f"消息处理失败: {str(e)}",
                "payload": payload
            }


if __name__ == "__main__":
    # 配置企业微信Webhook URL（必须替换为实际URL）
    WEBHOOK_URL = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=a5cb1336-d6a5-4e0f-ba54-3104fe1b6f69"

    # 创建发送器
    sender = SendReportMessage(WEBHOOK_URL)

    # 测试数据
    test_stats = {
        "total": 200,
        "passed": 170,
        "failed": 20,
        "error": 5,
        "skipped": 5
    }

    # 发送消息
    result = sender.send_wecom_rich_card(
        title="📊 正式环境测试报告",
        description=f"测试完成时间: {time.strftime('%Y-%m-%d %H:%M:%S')}",
        statistics=test_stats
    )

    print("消息发送结果:")
    print(json.dumps(result, indent=2, ensure_ascii=False))
