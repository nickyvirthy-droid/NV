"""

OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo: Action Loader

Descrição: Registro das actions padrão.

Interface Viva: Nicky Virthy

Arquiteto: Alex Projeti

"""

from plugins.actions.system_info.action import (
    SystemInfoAction
)
from plugins.actions.datetime.action import (
    DatetimeAction
)
from plugins.actions.uptime.action import (
    UptimeAction
)
from plugins.actions.disk_usage.action import (
    DiskUsageAction
)
from plugins.actions.memory_usage.action import (
    MemoryUsageAction
)
from plugins.actions.cpu_info.action import (
    CpuInfoAction
)
from plugins.actions.ip_address.action import (
    IpAddressAction
)
from plugins.actions.list_actions.action import (
    ListActionsAction
)
from plugins.actions.process_list.action import (
    ProcessListAction
)
from plugins.actions.process_info.action import (
    ProcessInfoAction
)
from plugins.actions.docker_list.action import (
    DockerListAction
)
from plugins.actions.docker_status.action import (
    DockerStatusAction
)
from plugins.actions.docker_logs.action import (
    DockerLogsAction
)
from plugins.actions.docker_stats.action import (
    DockerStatsAction
)
from plugins.actions.service_list.action import (
    ServiceListAction
)
from plugins.actions.service_status.action import (
    ServiceStatusAction
)
from plugins.actions.service_logs.action import (
    ServiceLogsAction
)
from plugins.actions.filesystem_search.action import (
    FilesystemSearchAction
)
from plugins.actions.filesystem_read.action import (
    FilesystemReadAction
)
from plugins.actions.filesystem_list.action import (
    FilesystemListAction
)
from plugins.actions.filesystem_exists.action import (
    FilesystemExistsAction
)
from plugins.actions.filesystem_info.action import (
    FilesystemInfoAction
)
from plugins.actions.git_branch.action import (
    GitBranchAction
)
from plugins.actions.git_status.action import (
    GitStatusAction
)
from plugins.actions.git_commit.action import (
    GitCommitAction
)
from plugins.actions.git_add.action import (
    GitAddAction
)
from plugins.actions.git_log.action import (
    GitLogAction
)
from plugins.actions.git_diff.action import (
    GitDiffAction
)
from plugins.actions.git_checkout.action import (
    GitCheckoutAction
)
from plugins.actions.git_fetch.action import (
    GitFetchAction
)
from plugins.actions.git_pull.action import (
    GitPullAction
)
from plugins.actions.git_push.action import (
    GitPushAction
)
from plugins.actions.system_exec.action import (
    SystemExecAction
)
from plugins.actions.system_which.action import (
    SystemWhichAction
)
from plugins.actions.system_hostname.action import (
    SystemHostnameAction
)
from plugins.actions.system_env.action import (
    SystemEnvAction
)
from plugins.actions.system_ping.action import (
    SystemPingAction
)
from plugins.actions.system_user.action import (
    SystemUserAction
)
from plugins.actions.system_groups.action import (
    SystemGroupsAction
)
from plugins.actions.process_kill.action import (
    ProcessKillAction
)
from plugins.actions.filesystem_write.action import (
    FilesystemWriteAction
)
from plugins.actions.filesystem_delete.action import (
    FilesystemDeleteAction
)
from plugins.actions.filesystem_mkdir.action import (
    FilesystemMkdirAction
)
from plugins.actions.filesystem_move.action import (
    FilesystemMoveAction
)
from plugins.actions.filesystem_copy.action import (
    FilesystemCopyAction
)
from plugins.actions.filesystem_touch.action import (
    FilesystemTouchAction
)
from plugins.actions.filesystem_tree.action import (
    FilesystemTreeAction
)
from plugins.actions.filesystem_hash.action import (
    FilesystemHashAction
)
from plugins.actions.filesystem_archive.action import (
    FilesystemArchiveAction
)
from plugins.actions.filesystem_extract.action import (
    FilesystemExtractAction
)
from plugins.actions.action_info.action import (
    ActionInfoAction
)
from plugins.actions.action_schema.action import (
    ActionSchemaAction
)
from plugins.actions.action_validate.action import (
    ActionValidateAction
)
from plugins.actions.database_tables.action import (
    DatabaseTablesAction
)
from plugins.actions.database_schema.action import (
    DatabaseSchemaAction
)
from plugins.actions.database_query.action import (
    DatabaseQueryAction
)

def register_actions(manager):

    manager.registry.register(
        SystemInfoAction()
    )

    manager.registry.register(
        DatetimeAction()
    )

    manager.registry.register(
        UptimeAction()
    )

    manager.registry.register(
        DiskUsageAction()
    )

    manager.registry.register(
        MemoryUsageAction()
    )

    manager.registry.register(
        CpuInfoAction()
    )

    manager.registry.register(
        IpAddressAction()
    )

    manager.registry.register(
        ListActionsAction()
    )

    manager.registry.register(
        ProcessListAction()
    )

    manager.registry.register(
        ProcessInfoAction()
    )

    manager.registry.register(
        DockerListAction()
    )

    manager.registry.register(
        DockerStatusAction()
    )

    manager.registry.register(
        DockerLogsAction()
    )

    manager.registry.register(
        DockerStatsAction()
    )

    manager.registry.register(
        ServiceListAction()
    )

    manager.registry.register(
        ServiceStatusAction()
    )

    manager.registry.register(
        ServiceLogsAction()
    )

    manager.registry.register(
        FilesystemSearchAction()
    )

    manager.registry.register(
        FilesystemReadAction()
    )

    manager.registry.register(
        FilesystemListAction()
    )

    manager.registry.register(
        FilesystemExistsAction()
    )

    manager.registry.register(
        FilesystemInfoAction()
    )

    manager.registry.register(
        GitBranchAction()
    )

    manager.registry.register(
        GitStatusAction()
    )

    manager.registry.register(
        GitCommitAction()
    )

    manager.registry.register(
        GitAddAction()
    )

    manager.registry.register(
        GitLogAction()
    )

    manager.registry.register(
        GitDiffAction()
    )

    manager.registry.register(
        GitCheckoutAction()
    )

    manager.registry.register(
        GitFetchAction()
    )

    manager.registry.register(
        GitPullAction()
    )

    manager.registry.register(
        GitPushAction()
    )

    manager.registry.register(
        SystemExecAction()
    )

    manager.registry.register(
        SystemWhichAction()
    )

    manager.registry.register(
        SystemHostnameAction()
    )

    manager.registry.register(
        SystemEnvAction()
    )

    manager.registry.register(
        SystemPingAction()
    )

    manager.registry.register(
        SystemUserAction()
    )

    manager.registry.register(
        SystemGroupsAction()
    )

    manager.registry.register(
        ProcessKillAction()
    )

    manager.registry.register(
        FilesystemWriteAction()
    )

    manager.registry.register(
        FilesystemDeleteAction()
    )

    manager.registry.register(
        FilesystemMkdirAction()
    )

    manager.registry.register(
        FilesystemMoveAction()
    )

    manager.registry.register(
        FilesystemCopyAction()
    )

    manager.registry.register(
        FilesystemTouchAction()
    )

    manager.registry.register(
        FilesystemTreeAction()
    )

    manager.registry.register(
        FilesystemHashAction()
    )

    manager.registry.register(
        FilesystemArchiveAction()
    )

    manager.registry.register(
        FilesystemExtractAction()
    )

    manager.registry.register(
        ActionInfoAction()
    )

    manager.registry.register(
        ActionSchemaAction()
    )

    manager.registry.register(
        ActionValidateAction()
    )

    manager.registry.register(
        DatabaseTablesAction()
    )

    manager.registry.register(
        DatabaseSchemaAction()
    )

    manager.registry.register(
        DatabaseQueryAction()
    )
