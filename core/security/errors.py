class NVError(Exception):
    pass


class ActionNotFoundError(
    NVError
):
    pass


class PermissionDeniedError(
    NVError
):
    pass


class ValidationFailedError(
    NVError
):
    pass
