from infra.robot.variablefile import VariableFile
from application.common.handler.filedatahandler import get_file_content


class FileReader(object):

    def __init__(self, env_id, region_id, suite_id):
        self.env_id = env_id
        self.region_id = region_id
        self.suite_id = suite_id

    def read(self):
        return VariableFile(
            self._get_file_text()
        ).get_text()

    def _get_file_text(self):
        data = get_file_content(self.suite_id)
        env, region = data.get('env_id'), data.get('region_id')
        if not (env and region):
            return data.get('file_text', '')
        if env and region:
            if env == self.env_id and region == self.region_id:
                return data.get('file_text', '')
        if env and not region:
            if env == self.env_id:
                return data.get('file_text', '')
        if not env and region:
            if region == self.region_id:
                return data.get('file_text', '')
        return ''

