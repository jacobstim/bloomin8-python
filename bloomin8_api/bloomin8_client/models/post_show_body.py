from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.post_show_body_dither import PostShowBodyDither
from ..models.post_show_body_play_type import PostShowBodyPlayType
from ..types import UNSET, Unset

T = TypeVar("T", bound="PostShowBody")


@_attrs_define
class PostShowBody:
    """
    Attributes:
        play_type (PostShowBodyPlayType): 0 for single image, 1 for gallery slideshow, 2 for playlist. Example: 1.
        gallery (str | Unset): Required when play_type is 1. Example: default.
        duration (int | Unset): Required when play_type is 1. Interval in seconds. Example: 120.
        playlist (str | Unset): Required when play_type is 2. Example: my_playlist.
        image (str | Unset): Optional. Path to an image to display immediately. Example: /gallerys/default/f1.jpg.
        dither (PostShowBodyDither | Unset): Optional. Dithering algorithm (e.g., 0 for Floyd-Steinberg, 1 for JJN).
            Example: 1.
    """

    play_type: PostShowBodyPlayType
    gallery: str | Unset = UNSET
    duration: int | Unset = UNSET
    playlist: str | Unset = UNSET
    image: str | Unset = UNSET
    dither: PostShowBodyDither | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        play_type = self.play_type.value

        gallery = self.gallery

        duration = self.duration

        playlist = self.playlist

        image = self.image

        dither: int | Unset = UNSET
        if not isinstance(self.dither, Unset):
            dither = self.dither.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "play_type": play_type,
            }
        )
        if gallery is not UNSET:
            field_dict["gallery"] = gallery
        if duration is not UNSET:
            field_dict["duration"] = duration
        if playlist is not UNSET:
            field_dict["playlist"] = playlist
        if image is not UNSET:
            field_dict["image"] = image
        if dither is not UNSET:
            field_dict["dither"] = dither

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        play_type = PostShowBodyPlayType(d.pop("play_type"))

        gallery = d.pop("gallery", UNSET)

        duration = d.pop("duration", UNSET)

        playlist = d.pop("playlist", UNSET)

        image = d.pop("image", UNSET)

        _dither = d.pop("dither", UNSET)
        dither: PostShowBodyDither | Unset
        if isinstance(_dither, Unset):
            dither = UNSET
        else:
            dither = PostShowBodyDither(_dither)

        post_show_body = cls(
            play_type=play_type,
            gallery=gallery,
            duration=duration,
            playlist=playlist,
            image=image,
            dither=dither,
        )

        post_show_body.additional_properties = d
        return post_show_body

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
