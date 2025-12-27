from enum import Enum


class GetPlaylistResponse200Type(str, Enum):
    DURATION = "duration"
    TIME = "time"

    def __str__(self) -> str:
        return str(self.value)
