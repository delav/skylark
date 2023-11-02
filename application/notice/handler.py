import json
import requests
from loguru import logger


class ReportNotifier(object):
    
    format_ding_url = 'https://oapi.dingtalk.com/robot/send?access_token={}'
    format_wecom_url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={}'
    format_lark_url = 'https://open.feishu.cn/open-apis/bot/v2/hook/{}'
    
    def __init__(self, report_url, result):
        self.report_url = report_url
        self.result = result
    
    def send_email(self, to_emails):
        pass
    
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
        # json_data = json.dumps(message)
        # r = requests.post(url, data=json_data, headers=headers)
        # logger.info(f'notice send finish|{r.status_code}|{r.text}')

    def _generate_email_content(self):
        return self.result

    def _generate_ding_body(self, keywords):
        report_url = self.result['report_url']
        body = {
            'msgtype': 'markdown',
            'markdown': {
                'title': keywords,
                'text': ""
            },
            'isAtAll': True
        }
        pgs = round(self.result['success_number']/self.result['total_number'], 3)
        self.result['progress'] = round(float(pgs*1000))/10
        self.result['times'] = str(self.result['end_time'] - self.result['start_time']).split('.')[0]
        part1 = '## 接口自动化测试报告【{}】\n'.format(self.result['project_name'])
        part2 = '<font color=#000000 size=3 face="黑体">总用例个数：{}</font>\n\n'.format(self.result['total_number'])
        part3 = '<font color=#228B22 size=3 face="黑体">通过用例数：{}</font>\n\n'.format(self.result['success_number'])
        part4 = '<font color=#fb0525 size=3 face="黑体">失败用例数：{}</font>\n\n'.format(self.result['failed_number'])
        part5 = '<font color=#0033CC size=3 face="黑体">测试通过率：{}%</font>\n\n'.format(self.result['progress'])
        part6 = '<font color=#9400D3 size=3 face="黑体">耗用的时间：{}</font>\n\n'.format(self.result['times'])
        part7 = '&nbsp;\n\n[点击查看报告]({})\n'.format(report_url)
        content = part1 + part2 + part3 + part4 + part5 + part6 + part7
        body['markdown']["text"] = content
        return body

    def _generate_wecom_body(self):
        report_url = self.result['report_url']
        body = {
            'msgtype': 'markdown',
            'markdown': {
                'content': ''
            },
        }
        pgs = round(self.result['success_number']/self.result['total_number'], 3)
        self.result['progress'] = round(float(pgs*1000))/10
        self.result['times'] = str(self.result['end_time'] - self.result['start_time']).split('.')[0]
        part1 = '### <font size=21>接口自动化测试报告【{}】</font>\n'.format(self.result['project_name'])
        part2 = '#### <font color=#000000 size=16 face="黑体">总用例个数：{}</font>\n\n'.format(self.result['total_number'])
        part3 = '#### <font color=#228B22 size=16 face="黑体">通过用例数：{}</font>\n\n'.format(self.result['success_number'])
        part4 = '#### <font color=#fb0525 size=16 face="黑体">失败用例数：{}</font>\n\n'.format(self.result['failed_number'])
        part5 = '#### <font color=#0033CC size=16 face="黑体">测试通过率：{}%</font>\n\n'.format(self.result['progress'])
        part6 = '#### <font color=#9400D3 size=16 face="黑体">耗用的时间：{}</font>\n\n'.format(self.result['times'])
        part7 = '\n\n<font size=13>[点击查看报告]({})</font>\n'.format(report_url)
        content = part1 + part2 + part3 + part4 + part5 + part6 + part7
        body['markdown']["content"] = content
        return body

    def _generate_lark_body(self, keywords):
        report_url = self.result['report_url']
        if keywords is not None and keywords != '':
            title = '{}-接口自动化测试报告【{}】'.format(keywords, self.result['project_name'])
        else:
            title = '接口自动化测试报告【{}】'.format(self.result["project_name"])
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
        self.result['progress'] = round(self.result['success_number']/self.result['total_number'], 2)*100
        self.result['times'] = str(self.result['end_time'] - self.result['start_time']).split('.')[0]
        part1 = [{'tag': 'text', 'text': '总用例个数：{}'.format(self.result['total_number'])}]
        part2 = [{'tag': 'text', 'text': '通过用例数：{}'.format(self.result['success_number'])}]
        part3 = [{'tag': 'text', 'text': '失败用例数：{}'.format(self.result['failed_number'])}]
        part4 = [{'tag': 'text', 'text': '测试通过率：{}'.format(self.result['progress'])}]
        part5 = [{'tag': 'text', 'text': '耗用的时间：{}'.format(self.result['times'])}]
        part6 = [{'tag': 'a', 'text': '\n点击查看报告', 'href': report_url}]
        content_list.extend([part1, part2, part3, part4, part5, part6])
        body['content']['post']['zh_cn']['content'] = content_list
        return body


    