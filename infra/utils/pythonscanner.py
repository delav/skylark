import os
import ast

KEYWORD = 'keyword'  # 被@keyword装饰器装饰的函数的关键字


def get_functions_info(file_path):
    """
    获取一个python文件中的所有函数信息
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        tree = ast.parse(f.read())

    module_name = os.path.basename(file_path).split('.')[0]
    functions = []
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            func_name = node.name
            func_args = [arg.arg for arg in node.args.args]
            func_doc = ast.get_docstring(node)

            # 查找函数是否被@keyword装饰器装饰
            is_decorated = False
            for decorator in node.decorator_list:
                if isinstance(decorator, ast.Call) and decorator.func.id == KEYWORD:
                    is_decorated = True
                    break

            functions.append({
                'module': module_name,
                'name': func_name,
                'args': func_args,
                'doc': func_doc,
                'decorated': is_decorated
            })

    return functions


def scan_directory(directory_path):
    """
    扫描某个目录下的所有python文件并解析函数信息
    """
    functions = []
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                functions.extend(get_functions_info(file_path))

    return functions


if __name__ == '__main__':
    functions = scan_directory('/path/to/directory')
    for function in functions:
        print(function)
