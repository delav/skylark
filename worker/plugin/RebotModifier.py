"""=================================================
@Author ：Delav
@Date   ：2020/11/13 16:25
@Desc   ：
=================================================="""
from robot.model import SuiteVisitor


class RobotModifier(SuiteVisitor):

    def __init__(self, name_map):
        self.name_map = name_map

    def visit_test(self, test):
        """Implements traversing through the test and its keywords.

        Can be overridden to allow modifying the passed in ``test`` without
        calling :func:`start_test` or :func:`end_test` nor visiting keywords.
        """
        if self.start_test(test) is not False:
            test.keywords.visit(self)
            self.end_test(test)

    def visit_keyword(self, kw):
        """Implements traversing through the keyword and its child keywords.

        Can be overridden to allow modifying the passed in ``kw`` without
        calling :func:`start_keyword` or :func:`end_keyword` nor visiting
        child keywords.
        """
        if self.start_keyword(kw) is not False:
            kw.keywords.visit(self)
            kw.messages.visit(self)
            self.end_keyword(kw)

    def start_keyword(self, keyword):
        """Called when keyword starts. Default implementation does nothing.

        Can return explicit ``False`` to stop visiting.
        """
        pass

    def end_keyword(self, keyword):
        """Called when keyword ends. Default implementation does nothing."""
        keyword.libname = None
        key = keyword.kwname
        if key in self.name_map:
            keyword.kwname = self.name_map[key]

    def visit_message(self, msg):
        """Implements visiting the message.

        Can be overridden to allow modifying the passed in ``msg`` without
        calling :func:`start_message` or :func:`end_message`.
        """
        if self.start_message(msg) is not False:
            self.end_message(msg)

    def start_message(self, msg):
        """Called when message starts. Default implementation does nothing.

        Can return explicit ``False`` to stop visiting.
        """
        pass

    def end_message(self, msg):
        """Called when message ends. Default implementation does nothing."""
        pass
