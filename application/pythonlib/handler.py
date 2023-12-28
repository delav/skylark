from loguru import logger
from django.conf import settings
from infra.client.gitclient import GitClient


def update_library_repository():
    max_retry = 3
    library_path = settings.LIBRARY_PATH
    git_client = GitClient()
    try_count = 0
    update_flag = False
    if not library_path.exists():
        while try_count < max_retry:
            try:
                git_client.clone(settings.LIBRARY_GIT, library_path)
                logger.info('clone library success')
                update_flag = True
            except (Exception,) as e:
                logger.error(f'clone library failed: {e}')
                try_count += 1
                continue
            break
    else:
        while try_count < max_retry:
            try:
                git_client.pull(library_path)
                logger.info('pull library success')
                update_flag = True
            except (Exception,) as e:
                logger.error(f'pull library failed: {e}')
                try_count += 1
                continue
            break
    return update_flag
