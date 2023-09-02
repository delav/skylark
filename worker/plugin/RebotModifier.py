"""=================================================
@Author ：Delav
@Date   ：2020/11/13 16:25
@Desc   ：
=================================================="""
from robot.api import SuiteVisitor


class RobotModifier(SuiteVisitor):

    def __init__(self, name_map):
        self.name_map = name_map

    def start_keyword(self, keyword):
        """Called when a keyword starts.

        By default, calls :meth:`start_body_item` which, by default, does nothing.

        Can return explicit ``False`` to stop visiting.
        """
        return self.start_body_item(keyword)

    def end_keyword(self, keyword):
        """Called when a keyword ends.

        By default, calls :meth:`end_body_item` which, by default, does nothing.
        """
        key = keyword.kwname.replace(' ', '_').lower()
        if key in self.name_map:
            keyword.libname = None
            keyword.kwname = self.name_map[key]

    def start_message(self, msg):
        """Called when a message starts.

        By default, calls :meth:`start_body_item` which, by default, does nothing.

        Can return explicit ``False`` to stop visiting.
        """
        return self.start_body_item(msg)

    def end_message(self, msg):
        """Called when a message ends.

        By default, calls :meth:`end_body_item` which, by default, does nothing.
        """
        self.end_body_item(msg)