import datetime


class UserEntity:
    def __init__(
        self,
        id: int,
        username: str,
        password: str,
        created_at: datetime.datetime,
        updated_at: datetime.datetime,
    ) -> None:
        self.id = id
        self.username = username
        self.password = password
        self.created_at = created_at
        self.updated_at = updated_at
