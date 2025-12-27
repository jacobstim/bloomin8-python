from enum import Enum


class PutPlaylistBodyType(str, Enum):
    DURATION = "duration"
    TIME = "time"

    def __str__(self) -> str:
        return str(self.value)
