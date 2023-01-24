#  Copyright 2008-2015 Nokia Networks
#  Copyright 2016-     Robot Framework Foundation
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import os.path

from robot.errors import DataError
from robot.model import SuiteNamePatterns
from robot.output import LOGGER
from robot.utils import abspath, get_error_message, safe_str, get_source_split


class SuiteStructure:

    def __init__(self, source=None, init_file=None, children=None):
        self.source = source
        self.init_file = init_file
        self.children = children
        self.extension = self._get_extension(source, init_file)

    def _get_extension(self, source, init_file):
        if self.is_directory and not init_file:
            return None
        source = init_file or source
        path_split = get_source_split()
        paths = source.split(path_split)
        if '.' not in paths[-1]:
            return None
        return paths[-1].split('.')[-1].lower()

    @property
    def is_directory(self):
        return self.children is not None

    def visit(self, visitor):
        if self.children is None:
            visitor.visit_file(self)
        else:
            visitor.visit_directory(self)


class SuiteStructureBuilder:
    path_split = get_source_split()

    def __init__(self, included_extensions=('robot',), included_suites=None):
        self.included_extensions = included_extensions
        self.included_suites = included_suites

    def build(self, paths):
        paths = self._normalize_path(paths)
        root = SuiteStructure(source=self._top_level_name(paths))
        [self._build(root, path) for path in paths]
        # self.show_child([root])
        return root

    def _build(self, pointer, path_str):
        path_list = path_str.split(self.path_split)
        for j in range(1, len(path_list)):
            if not pointer.children:
                pointer.children = []
            ok, extension = self._is_init_file(path_list[j])
            if ok:
                pointer.init_file = path_str
                pointer.extension = extension
                continue
            source_name = self.path_split.join(path_list[:j + 1])
            child_suite = self._find_child(pointer, source_name)
            if not child_suite:
                child_suite = SuiteStructure(source=source_name)
                pointer.children.append(child_suite)
            pointer = child_suite
        return pointer

    def _normalize_path(self, paths):
        return paths

    def _top_level_name(self, paths):
        if not paths:
            raise DataError('One or more source paths required.')
        try:
            return paths[0].split(self.path_split, 1)[0]
        except DataError as err:
            raise DataError("Checking path '%s' failed: %s" % (paths[0], err.message))

    def _is_init_file(self, base):
        base = base.lower()
        index = base.find('__init__')
        if index == -1:
            return False, None
        extension = base[index:].split('.')[-1]
        return True, extension

    def _find_child(self, suite, suite_name):
        for child in suite.children:
            if suite_name == child.source:
                return child
        return None

    def show_child(self, root):
        for node in root:
            print(node.__dict__)
            if node.children:
                self.show_child(node.children)


class SuiteStructureVisitor:

    def visit_file(self, structure):
        pass

    def visit_directory(self, structure):
        self.start_directory(structure)
        for child in structure.children:
            child.visit(self)
        self.end_directory(structure)

    def start_directory(self, structure):
        pass

    def end_directory(self, structure):
        pass
