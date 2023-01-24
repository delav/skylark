import time
import json
from loguru import logger
from django.utils.deprecation import MiddlewareMixin


class OpLogs(MiddlewareMixin):

    def __init__(self, *args):
        super(OpLogs, self).__init__(*args)

        self.start_time = None
        self.end_time = None
        self.trace_data = {}

    # def process_request(self, request):
    #     self.start_time = time.time()
    #     re_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    #     re_url = request.path
    #     re_method = request.method
    #     re_content = request.GET if re_method == 'GET' else request.POST
    #     if re_content:
    #         re_content = json.dumps(re_content)
    #     else:
    #         re_content = None
    #     self.trace_data.update({
    #             're_time': re_time,
    #             're_url': re_url,
    #             're_method': re_method,
    #             're_content': re_content,
    #             're_user': request.user
    #         })
    #
    # def process_response(self, request, response):
    #     rp_content = response.content.decode()
    #     self.trace_data['rp_content'] = rp_content
    #     self.end_time = time.time()
    #     access_time = self.end_time - self.start_time
    #     self.trace_data['access_time'] = round(access_time * 1000)
    #     logger.info(f'{self.trace_data["re_time"]}|'
    #                 f'{self.trace_data["re_method"]}|'
    #                 f'{self.trace_data["re_url"]}|'
    #                 # f'{self.trace_data["re_user"]}|'
    #                 f'{self.trace_data["access_time"]}ms|'
    #                 f'req: {self.trace_data["re_content"]}|'
    #                 f'rsp: {self.trace_data["rp_content"]}'
    #                 )
    #     return response

