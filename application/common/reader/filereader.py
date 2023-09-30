from infra.robot.variablefile import VariableFile
from application.virtualfile.handler import get_file_content, get_file_download_info


class VariableFileReader(object):

    def __init__(self, env_id, region_id, suite_id):
        self.env_id = env_id
        self.region_id = region_id
        self.suite_id = suite_id
        self.file_data = get_file_content(self.suite_id)

    def read(self):
        # read variable file content
        return VariableFile(
            self._get_file_text()
        ).get_text()

    def name(self):
        last_update = self.file_data.get('update_time')
        file_name = self.file_data.get('file_name')
        env, region = self.file_data.get('env_id'), self.file_data.get('region_id')
        env = env if env else 0
        region = region if region else 0
        return f'{env}_{region}_{last_update}_{file_name}'

    def _get_file_text(self):
        file_text = ''
        if not self.file_data:
            return file_text
        env, region = self.file_data.get('env_id'), self.file_data.get('region_id')
        if not (env and region):
            file_text = self.file_data.get('file_text', '')
        elif env and region:
            if env == self.env_id and region == self.region_id:
                file_text = self.file_data.get('file_text', '')
        elif env and not region:
            if env == self.env_id:
                file_text = self.file_data.get('file_text', '')
        elif not env and region:
            if region == self.region_id:
                file_text = self.file_data.get('file_text', '')
        return file_text


class ProjectFileReader(object):

    def __init__(self, suite_id):
        self.suite_id = suite_id
        self.file_data = get_file_download_info(self.suite_id)

    def read(self):
        # read project file download info
        if not self.file_data:
            return {}
        file_info = self.file_data.get('file_info', {})
        file_info['mtime'] = self.file_data['update_time']
        return file_info

    def name(self):
        return self.file_data.get('file_name', '')

