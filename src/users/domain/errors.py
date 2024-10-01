from src.core.errors import DomainError, ResourceNotFound


class UserError(DomainError):
    @classmethod
    def invalid_id(cls) -> "UserError":
        return cls("Invalid node id passed")


class UserErrorNotFound(ResourceNotFound):
    pass


class ExportError(DomainError):
    pass
