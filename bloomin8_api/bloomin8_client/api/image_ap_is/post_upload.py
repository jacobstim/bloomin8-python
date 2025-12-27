from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.post_upload_body import PostUploadBody
from ...models.post_upload_show_now import PostUploadShowNow
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    body: PostUploadBody,
    filename: str,
    gallery: str | Unset = UNSET,
    show_now: PostUploadShowNow | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    params: dict[str, Any] = {}

    params["filename"] = filename

    params["gallery"] = gallery

    json_show_now: int | Unset = UNSET
    if not isinstance(show_now, Unset):
        json_show_now = show_now.value

    params["show_now"] = json_show_now

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/upload",
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
    body: PostUploadBody,
    filename: str,
    gallery: str | Unset = UNSET,
    show_now: PostUploadShowNow | Unset = UNSET,
) -> Response[Any]:
    """Upload Image

     Uploads a single JPEG image to a specified gallery. The image can be displayed immediately upon
    upload.

    Args:
        filename (str):
        gallery (str | Unset):
        show_now (PostUploadShowNow | Unset):
        body (PostUploadBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        body=body,
        filename=filename,
        gallery=gallery,
        show_now=show_now,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: PostUploadBody,
    filename: str,
    gallery: str | Unset = UNSET,
    show_now: PostUploadShowNow | Unset = UNSET,
) -> Response[Any]:
    """Upload Image

     Uploads a single JPEG image to a specified gallery. The image can be displayed immediately upon
    upload.

    Args:
        filename (str):
        gallery (str | Unset):
        show_now (PostUploadShowNow | Unset):
        body (PostUploadBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        body=body,
        filename=filename,
        gallery=gallery,
        show_now=show_now,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
