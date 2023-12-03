from application.status import ModuleStatus, BuildStatus

module_status_map = {
    ModuleStatus.NORMAL: 'Normal',
    ModuleStatus.DISCARDED: 'Discarded',
    ModuleStatus.DISABLED: 'Disabled',
    ModuleStatus.DELETED: 'Deleted'
}

build_status_map = {
    BuildStatus.PENDING: 'Pending',
    BuildStatus.RUNNING: 'Running',
    BuildStatus.FINISH: 'Finish',
    BuildStatus.FAILED: 'Failed',
    BuildStatus.SUCCESS: 'Success',
}
