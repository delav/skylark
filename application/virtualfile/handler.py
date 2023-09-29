from pathlib import Path
from django.conf import settings
from application.constant import ModuleStatus, FileSaveMode
from application.manager import get_project_by_id
from application.virtualfile.models import VirtualFile
from application.virtualfile.serializers import VirtualFileSerializers
from infra.utils.readfile import FILE_READER_MAP

PATH_SEPARATOR = '/'
INTERNAL_DOWNLOAD_API = '/api/internal/download_file'


def get_file_content(suite_id, **kwargs):
    queryset = VirtualFile.objects.filter(
        suite_id=suite_id,
        **kwargs
    )
    if not queryset.exists():
        return None
    instance = queryset.first()
    data = VirtualFileSerializers(instance).data
    if instance.save_mode == FileSaveMode.DB:
        return data
    elif instance.save_mode == FileSaveMode.FILE:
        data['file_text'] = ''
        child_path_list = instance.file_path.split(PATH_SEPARATOR)
        file_path = Path(settings.PROJECT_FILES, *child_path_list)
        file_name = instance.file_name
        file = Path(file_path, file_name)
        if not file.exists():
            return data
        reader = FILE_READER_MAP.get(instance.file_suffix.lower())
        if reader:
            data['file_text'] = reader(file)
        else:
            data['file_text'] = '***暂不支持该类型的文件展示！***'
    return data


def update_file(suite_id, **kwargs):
    queryset = VirtualFile.objects.filter(
        suite_id=suite_id,
    )
    if not queryset.exists() or queryset.count() != 1:
        return
    file_obj = queryset.first()
    queryset.update(**kwargs)
    if kwargs.get('file_name') and file_obj.save_mode == FileSaveMode.FILE:
        file_name = kwargs.get('file_name')
        child_path_list = file_obj.file_path.split(PATH_SEPARATOR)
        file_path = [settings.PROJECT_FILES, *child_path_list]
        file = Path(*file_path, file_obj.file_name)
        if file.exists():
            file.rename(file.with_name(file_name))
    if kwargs.get('status') == ModuleStatus.DELETED and file_obj.save_mode == FileSaveMode.FILE:
        child_path_list = file_obj.file_path.split(PATH_SEPARATOR)
        file_path = [settings.PROJECT_FILES, *child_path_list]
        file = Path(*file_path, file_obj.file_name)
        if file.exists():
            file.unlink()


def get_file_download_info(suite_id, **kwargs):
    queryset = VirtualFile.objects.filter(
        suite_id=suite_id,
        **kwargs
    )
    if not queryset.exists():
        return {}
    instance = queryset.first()
    data = VirtualFileSerializers(instance).data
    file_path = instance.file_path + PATH_SEPARATOR + instance.file_name
    data['file_info'] = {
        'url': settings.SERVER_DOMAIN + INTERNAL_DOWNLOAD_API,
        'params': {'path': file_path}
    }
    return data


def get_download_file_stream(path_str, file_name):
    path_list = path_str.split(PATH_SEPARATOR)
    file_path = [settings.PROJECT_FILES, *path_list]
    file = Path(*file_path, file_name)
    if not file.exists():
        return None
    return open(file, 'rb', encoding='utf-8')


def get_full_dir_path(child_dir_obj, result):

    def _get_dir_path(dir_obj, result_path):
        result_path.append(dir_obj.name)
        if dir_obj.parent_dir:
            return _get_dir_path(dir_obj.parent_dir, result_path)
        project = get_project_by_id(dir_obj.project_id)
        if not project:
            return []
        result.append(project.get('name'))
        return result_path[::-1]

    return _get_dir_path(child_dir_obj, result)
