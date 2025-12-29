from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    image: str,
    gallery: str | Unset = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["image"] = image

    params["gallery"] = gallery

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/image/delete",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Any | None:
    if response.status_code == 200:
        return None

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Any]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    image: str,
    gallery: str | Unset = UNSET,
) -> Response[Any]:
    """Delete Image

     Deletes a specific image from a gallery.

    Args:
        image (str):
        gallery (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        image=image,
        gallery=gallery,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


# def sync(
#     *,
#     client: AuthenticatedClient | Client,
#     image: str,
#     gallery: str | Unset = UNSET,
# ) -> Any | None:
#     """Delete Image

#      Deletes a specific image from a gallery.

#     Args:
#         image (str):
#         gallery (str | Unset):

#     Raises:
#         errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
#         httpx.TimeoutException: If the request takes longer than Client.timeout.

#     Returns:
#         Any | None
#     """

#     return sync_detailed(
#         client=client,
#         image=image,
#         gallery=gallery,
#     ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    image: str,
    gallery: str | Unset = UNSET,
) -> Response[Any]:
    """Delete Image

     Deletes a specific image from a gallery.

    Args:
        image (str):
        gallery (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        image=image,
        gallery=gallery,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


# async def asyncio(
#     *,
#     client: AuthenticatedClient | Client,
#     image: str,
#     gallery: str | Unset = UNSET,
# ) -> Any | None:
#     """Delete Image

#      Deletes a specific image from a gallery.

#     Args:
#         image (str):
#         gallery (str | Unset):

#     Raises:
#         errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
#         httpx.TimeoutException: If the request takes longer than Client.timeout.

#     Returns:
#         Any | None
#     """

#     return (
#         await asyncio_detailed(
#             client=client,
#             image=image,
#             gallery=gallery,
#         )
#     ).parsed
