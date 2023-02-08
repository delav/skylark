from application.infra.engine.structure import SuiteStructure


class DcsEngine(object):

    def __init__(self, **kwargs):
        self.data = None
        self.total_case = 0
        self.batch_no = 1
        self.options = kwargs

    def visit(self, structure):
        if self.options.get('distributed'):
            self.batch_no = 1

    def get_batch(self):
        return self.batch_no

    def get_cases(self):
        return self.total_case

    def get(self, batch_no):
        return self.data.get(batch_no)
