

class VariableFile(object):
    """
    python variable file, as common variable
    """

    def __init__(self, text):
        self.text_content = text

    def get_text(self):
        if not self.text_content or self.text_content.strip() == '':
            return ''
        return self.text_content

