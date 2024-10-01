from src.core.errors import DomainError, ResourceNotFound


class BotError(DomainError):
    @classmethod
    def invalid_id(cls) -> "BotError":
        return cls("Invalid node id passed")


class BotErrorNotFound(ResourceNotFound):
    pass
