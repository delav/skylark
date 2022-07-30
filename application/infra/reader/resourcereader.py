from application.infra.reader.basereader import BaseReader
from application.infra.reader.builder import *


class ResourceReader(BaseReader):
    def __init__(self, project_id, project_name, module_id, module_type):
        self.project_id = project_id
        self.project_name = project_name
        self.module_id = module_id
        self.module_type = module_type

    def read(self):
        return MultiResource(self.project_id, self.project_name).resources_map()

