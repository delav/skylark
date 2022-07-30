

class DataStructure(object):

    def __init__(self, env='test', project_id=None, project_name=None):
        self.env = env
        self.project_id = project_id
        self.project_name = project_name
        self.map = {}

    def get_text_by_path(self):
        pass

    def parser(self, reader):
        data = reader.read()
        self.map.update(data)
