import ast
from pathlib import Path

KEYWORD = 'keyword'


class CodeScanner(object):

    @classmethod
    def scan_directory(cls, dir_path: Path):
        if not isinstance(dir_path, Path):
            dir_path = Path(dir_path)
        if not dir_path.exists():
            return []
        functions = []
        for f in dir_path.iterdir():
            if f.is_file() and f.suffix == '.py':
                functions.extend(cls.get_functions_info(f))
        return functions

    @classmethod
    def get_functions_info(cls, file_path: Path):
        with open(file_path, 'r', encoding='utf-8') as f:
            tree = ast.parse(f.read())

        module_name = file_path.name.split('.')[0]
        functions = []
        for node in tree.body:
            if isinstance(node, ast.FunctionDef):
                function_info = cls._handle_function_node(module_name, node)
                if function_info:
                    functions.append(function_info)
            elif isinstance(node, ast.ClassDef):
                class_name = node.name
                if class_name != module_name:
                    continue
                for func_node in node.body:
                    function_info = cls._handle_function_node(module_name, func_node)
                    if function_info:
                        functions.append(function_info)
        return functions

    @staticmethod
    def _handle_function_node(module_name, node):
        func_name = node.name
        if func_name.startswith('_'):
            return None
        func_args = []
        for i in range(len(node.args.args)):
            arg = node.args.args[i].arg
            if i == 0 and (arg == 'self' or arg == 'cls'):
                continue
            func_args.append(arg)
        func_vararg = True if node.args.vararg else False
        func_kwarg = True if node.args.kwarg else False
        func_doc = ast.get_docstring(node)
        func_returns = None
        for stmt in node.body:
            if isinstance(stmt, ast.Return):
                if not stmt.value:
                    break
                if isinstance(stmt.value, ast.Name):
                    func_returns = stmt.value.id
                else:
                    func_returns = 'Result'
                break
        is_keyword = False
        for decorator in node.decorator_list:
            if isinstance(decorator, ast.Name) and decorator.id == KEYWORD:
                is_keyword = True
                break
        return {
            'module': module_name,
            'name': func_name,
            'args': func_args,
            'vararg': func_vararg,
            'kwarg': func_kwarg,
            'doc': func_doc,
            'keyword': is_keyword,
            'returns': func_returns,
        }
