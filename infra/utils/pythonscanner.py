import ast
from pathlib import Path

KEYWORD = 'keyword'


def get_functions_info(file_path: Path):
    with open(file_path, 'r', encoding='utf-8') as f:
        tree = ast.parse(f.read())

    module_name = file_path.name.split('.')[0]
    functions = []
    for node in tree.body:
        if not isinstance(node, ast.FunctionDef):
            continue
        func_name = node.name
        func_args = [arg.arg for arg in node.args.args]
        func_vararg = True if node.args.vararg else False
        func_kwarg = True if node.args.kwarg else False
        func_doc = ast.get_docstring(node)
        func_returns = None
        for stmt in node.body:
            if isinstance(stmt, ast.Return):
                if stmt.value:
                    func_returns = stmt.value.id
                break
        is_keyword = False
        for decorator in node.decorator_list:
            if isinstance(decorator, ast.Name) and decorator.id == KEYWORD:
                is_keyword = True
                break

        functions.append({
            'module': module_name,
            'name': func_name,
            'args': func_args,
            'vararg': func_vararg,
            'kwarg': func_kwarg,
            'doc': func_doc,
            'keyword': is_keyword,
            'returns': func_returns,
        })

    return functions


def scan_directory(dir_path: Path):
    if not isinstance(dir_path, Path):
        dir_path = Path(dir_path)
    if not dir_path.exists():
        return []
    functions = []
    for f in dir_path.iterdir():
        if f.is_file() and f.suffix == '.py':
            functions.extend(get_functions_info(f))
    return functions

