import json
import requests
from loguru import logger


def push_ding_msg(token, keywords, result):
    logger.info("钉钉群token:{},关键词:{}".format(token, keywords))
    logger.info("结果通知数据: {}".format(result))
    if ";" in token:
        token_list = token.split(";")
        urls = token_list
    else:
        urls = [token]
    for t in urls:
        url = 'https://oapi.dingtalk.com/robot/send?access_token={}'.format(t)
        report_url = 'http://192.168.1.50:9090/output/reports/'\
                     + result["project_name"] + '/' + result["run_id"] + '/log.html'
        headers = {'Content-Type': 'application/json'}

        data = {
            "msgtype": "markdown",
            "markdown": {
                "title": keywords,
                "text": ""
            },
            "isAtAll": True
        }
        pgs = round(result["success_number"]/result["total_number"], 3)
        result["progress"] = round(float(pgs*1000))/10
        result["times"] = str(result["end_time"] - result["start_time"]).split('.')[0]
        part1 = "## 接口自动化测试报告【{}】\n".format(result["project_name"])
        part2 = '<font color=#000000 size=3 face="黑体">总用例个数：{}</font>\n\n'.format(result["total_number"])
        part3 = '<font color=#228B22 size=3 face="黑体">通过用例数：{}</font>\n\n'.format(result["success_number"])
        part4 = '<font color=#fb0525 size=3 face="黑体">失败用例数：{}</font>\n\n'.format(result["failed_number"])
        part5 = '<font color=#0033CC size=3 face="黑体">测试通过率：{}%</font>\n\n'.format(result["progress"])
        part6 = '<font color=#9400D3 size=3 face="黑体">耗用的时间：{}</font>\n\n'.format(result["times"])
        part7 = '&nbsp;\n\n[点击查看报告]({})\n'.format(report_url)
        content = part1 + part2 + part3 + part4 + part5 + part6 + part7
        data["markdown"]["text"] = content
        json_data = json.dumps(data)
        r = requests.post(url, data=json_data, headers=headers)
        json.loads(r.text)


def push_wecom_msg(token, result):
    logger.info("结果通知数据: {}".format(result))
    if ";" in token:
        token_list = token.split(";")
        urls = token_list
    else:
        urls = [token]
    for t in urls:
        url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={}'.format(t)
        report_url = 'http://192.168.1.50:9090/output/reports/'\
                     + result["project_name"] + '/' + result["run_id"] + '/log.html'
        headers = {'Content-Type': 'application/json'}

        data = {
            "msgtype": "markdown",
            "markdown": {
                "content": ""
            },
        }
        pgs = round(result["success_number"]/result["total_number"], 3)
        result["progress"] = round(float(pgs*1000))/10
        result["times"] = str(result["end_time"] - result["start_time"]).split('.')[0]
        part1 = "### <font size=21>接口自动化测试报告【{}】</font>\n".format(result["project_name"])
        part2 = '#### <font color=#000000 size=16 face="黑体">总用例个数：{}</font>\n\n'.format(result["total_number"])
        part3 = '#### <font color=#228B22 size=16 face="黑体">通过用例数：{}</font>\n\n'.format(result["success_number"])
        part4 = '#### <font color=#fb0525 size=16 face="黑体">失败用例数：{}</font>\n\n'.format(result["failed_number"])
        part5 = '#### <font color=#0033CC size=16 face="黑体">测试通过率：{}%</font>\n\n'.format(result["progress"])
        part6 = '#### <font color=#9400D3 size=16 face="黑体">耗用的时间：{}</font>\n\n'.format(result["times"])
        part7 = '\n\n<font size=13>[点击查看报告]({})</font>\n'.format(report_url)
        content = part1 + part2 + part3 + part4 + part5 + part6 + part7
        data["markdown"]["content"] = content
        json_data = json.dumps(data)
        r = requests.post(url, data=json_data, headers=headers)
        json.loads(r.text)


def push_lark_msg(token, keywords, result):
    print("结果通知数据: {}".format(result))
    if ";" in token:
        token_list = token.split(";")
        urls = token_list
    else:
        urls = [token]
    for t in urls:
        url = 'https://open.feishu.cn/open-apis/bot/v2/hook/{}'.format(t)
        report_url = 'http://192.168.1.50:9090/output/reports/'\
                     + result["project_name"] + '/' + result["run_id"] + '/log.html'
        headers = {'Content-Type': 'application/json'}

        if keywords is not None and keywords != "":
            title = "{}-接口自动化测试报告【{}】".format(keywords, result["project_name"])
        else:
            title = "接口自动化测试报告【{}】".format(result["project_name"])
        data = {
            "msg_type": "post",
            "content": {
                "post": {
                    "zh_cn": {
                        "title": title,
                        "content": []
                    }
                }
            }
        }
        content_list = []
        result["progress"] = round(result["success_number"]/result["total_number"], 2)*100
        result["times"] = str(result["end_time"] - result["start_time"]).split('.')[0]
        part1 = [{"tag": "text", "text": "总用例个数：{}".format(result["total_number"])}]
        part2 = [{"tag": "text", "text": "通过用例数：{}".format(result["success_number"])}]
        part3 = [{"tag": "text", "text": "失败用例数：{}".format(result["failed_number"])}]
        part4 = [{"tag": "text", "text": "测试通过率：{}".format(result["progress"])}]
        part5 = [{"tag": "text", "text": "耗用的时间：{}".format(result["times"])}]
        part6 = [{"tag": "a", "text": "\n点击查看报告", "href": report_url}]
        content_list.extend([part1, part2, part3, part4, part5, part6])
        data["content"]["post"]["zh_cn"]["content"] = content_list
        json_data = json.dumps(data)
        r = requests.post(url, data=json_data, headers=headers, verify=False)
        json.loads(r.text)
