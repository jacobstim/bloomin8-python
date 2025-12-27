"""Contains shared errors types that can be raised from API functions"""


class UnexpectedStatus(Exception):
    """Raised by api functions when the response status an undocumented status and Client.raise_on_unexpected_status is True"""

    def __init__(self, status_code: int, content: bytes):
        self.status_code = status_code
        self.content = content

        super().__init__(
            f"Unexpected status code: {status_code}\n\nResponse content:\n{content.decode(errors='ignore')}"
        )


class DeviceUnreachableError(Exception):
    """Raised when the Bloomin8 device is unreachable (timeout, connection refused, etc.)"""

    def __init__(self, host: str, reason: str = "Connection failed"):
        self.host = host
        self.reason = reason
        super().__init__(f"Device unreachable at {host}: {reason}")


__all__ = ["UnexpectedStatus", "DeviceUnreachableError"]
