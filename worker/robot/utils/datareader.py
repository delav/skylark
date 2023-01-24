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

import threading
from .robottypes import is_bytes


class ThreadSafeSingleton(type):
    _instances = {}
    _singleton_lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with cls._singleton_lock:
                if cls not in cls._instances:
                    cls._instances[cls] = super(ThreadSafeSingleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class DataReader(metaclass=ThreadSafeSingleton):
    """
    Get file content by path from metadata,
    """

    def __init__(self, task_id=None, source_data=None):
        self.taskid = task_id
        self.sources = source_data

    def __enter__(self):
        return self

    def read(self, source):
        return self._decode(self.sources.get(source, ''))

    def _decode(self, content, remove_bom=True):
        if is_bytes(content):
            content = content.decode('UTF-8')
        if remove_bom and content.startswith('\ufeff'):
            content = content[1:]
        if '\r\n' in content:
            content = content.replace('\r\n', '\n')
        return content


def get_source_split():
    return '/'
