"""Utility functions for the Bloomin8 API."""

from typing import Callable, TypeVar
from functools import wraps

import httpx
import httpcore

from .bloomin8_client.errors import DeviceUnreachableError


T = TypeVar('T')


def handle_connection_errors(host: str) -> Callable:
    """
    Decorator to handle connection errors gracefully.
    
    Converts low-level httpx/httpcore exceptions into user-friendly DeviceUnreachableError.
    
    Args:
        host: The host address for error messages
        
    Returns:
        Decorated function that handles connection errors
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args, **kwargs) -> T:
            try:
                return func(*args, **kwargs)
            except httpcore.ConnectTimeout:
                raise DeviceUnreachableError(host, "Connection timed out")
            except httpcore.ConnectError as e:
                raise DeviceUnreachableError(host, f"Connection failed: {e}")
            except httpx.ConnectTimeout:
                raise DeviceUnreachableError(host, "Connection timed out")
            except httpx.ConnectError as e:
                raise DeviceUnreachableError(host, f"Connection failed: {e}")
            except httpx.TimeoutException:
                raise DeviceUnreachableError(host, "Request timed out")
            except httpx.NetworkError as e:
                raise DeviceUnreachableError(host, f"Network error: {e}")
            except OSError as e:
                # Catch socket-level errors (connection refused, etc.)
                if "refused" in str(e).lower() or "unreachable" in str(e).lower():
                    raise DeviceUnreachableError(host, str(e))
                raise  # Re-raise if it's a different OSError
        return wrapper
    return decorator
