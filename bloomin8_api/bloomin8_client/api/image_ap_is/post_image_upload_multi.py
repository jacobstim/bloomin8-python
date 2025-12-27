from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.post_image_upload_multi_body import PostImageUploadMultiBody
from ...models.post_image_upload_multi_override import PostImageUploadMultiOverride
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    body: PostImageUploadMultiBody,
    gallery: str | Unset = UNSET,
    override: PostImageUploadMultiOverride | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    params: dict[str, Any] = {}

    params["gallery"] = gallery

    json_override: int | Unset = UNSET
    if not isinstance(override, Unset):
        json_override = override.value

    params["override"] = json_override

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/image/uploadMulti",
        "params": params,
    }

    _kwargs["files"] = body.to_multipart()

    _kwargs["headers"] = headers
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
    body: PostImageUploadMultiBody,
    gallery: str | Unset = UNSET,
    override: PostImageUploadMultiOverride | Unset = UNSET,
) -> Response[Any]:
    """Upload Multiple Images

     Uploads multiple images in a single request.

    Args:
        gallery (str | Unset):
        override (PostImageUploadMultiOverride | Unset):
        body (PostImageUploadMultiBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        body=body,
        gallery=gallery,
        override=override,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: PostImageUploadMultiBody,
    gallery: str | Unset = UNSET,
    override: PostImageUploadMultiOverride | Unset = UNSET,
) -> Response[Any]:
    """Upload Multiple Images

     Uploads multiple images in a single request.

    Args:
        gallery (str | Unset):
        override (PostImageUploadMultiOverride | Unset):
        body (PostImageUploadMultiBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        body=body,
        gallery=gallery,
        override=override,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
