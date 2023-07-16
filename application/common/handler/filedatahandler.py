from pathlib import Path
from django.conf import settings
from application.constant import ModuleStatus, FileSaveMode
from application.virtualfile.models import VirtualFile
from application.virtualfile.serializers import VirtualFileSerializers
from infra.utils.readfile import FILE_READER_MAP

PATH_SEPARATOR = '/'


def get_file_content(suite_id, **kwargs):
    queryset = VirtualFile.objects.filter(
        suite_id=suite_id,
        **kwargs
    )
    if not queryset.exists():
        return {}
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
    if kwargs.get('name') and file_obj.save_mode == FileSaveMode.FILE:
        file_name = kwargs.get('name')
        child_path_list = file_obj.file_path.split(PATH_SEPARATOR)
        file_path = Path(settings.PROJECT_FILES, *child_path_list)
        file = Path(file_path, file_obj.file_name)
        if file.exists():
            file.rename(file.with_name(file_name))
    if kwargs.get('status') == ModuleStatus.DELETED and file_obj.save_mode == FileSaveMode.FILE:
        child_path_list = file_obj.file_path.split(PATH_SEPARATOR)
        file_path = Path(settings.PROJECT_FILES, *child_path_list)
        file = Path(file_path, file_obj.file_name)
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
    child_path_list = instance.file_path.split(PATH_SEPARATOR)
    file_path = Path(settings.PROJECT_FILES, *child_path_list)
    file_name = instance.file_name
    file = Path(file_path, file_name)
    data['file_info'] = {
        'host': '127.0.0.1:8000',
        'api': '/api/internal/download_file',
        'params': {'path': str(file)}
    }
    return data
