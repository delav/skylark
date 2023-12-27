import json
import requests
from loguru import logger
from django.core.mail import send_mail
from django.template.loader import get_template


class ReportNotifier(object):
    
    format_ding_url = 'https://oapi.dingtalk.com/robot/send?access_token={}'
    format_wecom_url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={}'
    format_lark_url = 'https://open.feishu.cn/open-apis/bot/v2/hook/{}'
    
    def __init__(self, report_url, result):
        self.report_url = report_url
        self.result = result
    
    def send_email(self, from_email, to_emails):
        email_body = self._generate_email_body()
        send_mail(
            subject='Skylark自动化测试报告',
            message=None,
            html_message=email_body,
            from_email=from_email,
            recipient_list=to_emails,
        )
        logger.info(f'email send finish')
    
    def send_ding(self, tokens, keywords):
        """
        send resport information to ding group
        """
        logger.info(f'send ding notice start|{self.result}')
        token_list = tokens.split(';') if ';' in tokens else [tokens]
        ding_body = self._generate_ding_body(keywords)
        for token in token_list:
            push_url = self.format_ding_url.format(token)
            self.post(push_url, ding_body)
    
    def send_wecom(self, tokens):
        """
        send resport information to wecom group
        """
        logger.info(f'send wecom notice start|{self.result}')
        token_list = tokens.split(';') if ';' in tokens else [tokens]
        wecom_body = self._generate_wecom_body()
        for token in token_list:
            push_url = self.format_wecom_url.format(token)
            self.post(push_url, wecom_body)
    
    def send_lark(self, tokens, keywords):
        """
        send resport information to ding group
        """
        logger.info(f'send ding notice start|{self.result}')
        token_list = tokens.split(';') if ';' in tokens else [tokens]
        lark_body = self._generate_lark_body(keywords)
        for token in token_list:
            push_url = self.format_lark_url.format(token)
            self.post(push_url, lark_body)

    @staticmethod
    def post(url, message, headers=None):
        if headers is None:
            headers = {'Content-Type': 'application/json'}
        json_data = json.dumps(message)
        r = requests.post(url, data=json_data, headers=headers)
        logger.info(f'notice send finish|{r.status_code}|{r.text}')

    def _generate_email_body(self):
        template = get_template('report.html')
        html_content = template.render({
            'tester': self.result.get('tester'),
            'project_name': self.result.get('project_name'),
            'record_id': self.result.get('record_id'),
            'data_list': self.result['data_list']
        })
        return html_content

    def _generate_ding_body(self, keywords):
        body = {
            'msgtype': 'markdown',
            'markdown': {
                'title': keywords,
                'text': ""
            },
            'isAtAll': True
        }
        part1 = f'## 【{self.result["project_name"]}】【{self.result["env_name"]}】' \
                f'【{self.result["region_name"]}】自动化测试报告\n'
        part2 = f'<font color=#02992c size=3 face="黑体">执行编号：{self.result["history_id"]}</font>\n\n'
        part3 = f'<font color=#02992c size=3 face="黑体">开始时间：{self.result["start_time"]}</font>\n\n'
        part4 = f'<font color=#02992c size=3 face="黑体">结束时间：{self.result["end_time"]}</font>\n\n'
        part5 = f'<font color=#02992c size=3 face="黑体">执行耗时：{self.result["duration"]}</font>\n\n'
        part6 = f'<font color=#02992c size=3 face="黑体">通过率：{self.result["passed_rate"]}</font>\n\n'
        part7 = f'<font color=#02992c size=3 face="黑体">总用例数：{self.result["total_number"]}</font>\n\n'
        part8 = f'<font color=#02992c size=3 face="黑体">成功用例：{self.result["success_number"]}</font>\n\n'
        part9 = f'<font color=#cc0109 size=3 face="黑体">失败用例：{self.result["failed_number"]}</font>\n\n'
        part10 = f'<font color=#575a5c size=3 face="黑体">跳过用例：{self.result["skipped_number"]}</font>\n\n'
        part11 = f'&nbsp;\n\n[点击查看报告]({self.report_url})\n'
        content = part1 + part2 + part3 + part4 + part5 + part6 + part7 + part8 + part9 + part10 + part11
        body['markdown']["text"] = content
        return body

    def _generate_wecom_body(self):
        body = {
            'msgtype': 'markdown',
            'markdown': {
                'content': ''
            },
        }
        part1 = f'### <font size=21>【{self.result["project_name"]}】【{self.result["env_name"]}】' \
                f'【{self.result["region_name"]}】自动化测试报告</font>\n'
        part2 = f'#### <font color=#02992c size=16 face="黑体">执行编号：{self.result["history_id"]}</font>\n\n'
        part3 = f'#### <font color=#02992c size=16 face="黑体">开始时间：{self.result["start_time"]}</font>\n\n'
        part4 = f'#### <font color=#02992c size=16 face="黑体">结束时间：{self.result["end_time"]}</font>\n\n'
        part5 = f'#### <font color=#02992c size=16 face="黑体">执行耗时：{self.result["duration"]}%</font>\n\n'
        part6 = f'#### <font color=#02992c size=16 face="黑体">通过率：{self.result["passed_rate"]}</font>\n\n'
        part7 = f'#### <font color=#02992c size=16 face="黑体">总用例数：{self.result["total_number"]}</font>\n\n'
        part8 = f'#### <font color=#02992c size=16 face="黑体">成功用例：{self.result["success_number"]}</font>\n\n'
        part9 = f'#### <font color=#cc0109 size=16 face="黑体">失败用例：{self.result["failed_number"]}</font>\n\n'
        part10 = f'#### <font color=#575a5c size=16 face="黑体">跳过用例：{self.result["skipped_number"]}</font>\n\n'
        part11 = f'\n\n<font size=13>[点击查看报告]({self.report_url})</font>\n'
        content = part1 + part2 + part3 + part4 + part5 + part6 + part7 + part8 + part9 + part10 + part11
        body['markdown']["content"] = content
        return body

    def _generate_lark_body(self, keywords):
        if keywords is not None and keywords != '':
            title = f'{keywords}-【{self.result["project_name"]}】【{self.result["env_name"]}】' \
                    f'【{self.result["region_name"]}】自动化测试报告'
        else:
            title = f'【{self.result["project_name"]}】【{self.result["env_name"]}】' \
                    f'【{self.result["region_name"]}】自动化测试报告'
        body = {
            'msg_type': 'post',
            'content': {
                'post': {
                    'zh_cn': {
                        'title': title,
                        'content': []
                    }
                }
            }
        }
        content_list = []
        part1 = [{'tag': 'text', 'text': '执行编号：{}'.format(self.result['history_id'])}]
        part2 = [{'tag': 'text', 'text': '开始时间：{}'.format(self.result['start_time'])}]
        part3 = [{'tag': 'text', 'text': '结束时间：{}'.format(self.result['end_time'])}]
        part4 = [{'tag': 'text', 'text': '执行耗时：{}'.format(self.result['duration'])}]
        part5 = [{'tag': 'text', 'text': '通过率：{}'.format(self.result['passed_rate'])}]
        part6 = [{'tag': 'text', 'text': '总用例数：{}'.format(self.result['total_number'])}]
        part7 = [{'tag': 'text', 'text': '成功用例：{}'.format(self.result['success_number'])}]
        part8 = [{'tag': 'text', 'text': '失败用例：{}'.format(self.result['failed_number'])}]
        part9 = [{'tag': 'text', 'text': '跳过用例：{}'.format(self.result['skipped_number'])}]
        part10 = [{'tag': 'a', 'text': '\n点击查看报告', 'href': self.report_url}]
        content_list.extend([part1, part2, part3, part4, part5, part6, part7, part8, part9, part10])
        body['content']['post']['zh_cn']['content'] = content_list
        return body


    