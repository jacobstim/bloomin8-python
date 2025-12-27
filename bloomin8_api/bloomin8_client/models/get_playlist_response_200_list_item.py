from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="GetPlaylistResponse200ListItem")


@_attrs_define
class GetPlaylistResponse200ListItem:
    """
    Attributes:
        name (str | Unset):  Example: /gallerys/default/f1.jpg.
        duration (int | Unset):  Example: 40.
        time (str | Unset):
    """

    name: str | Unset = UNSET
    duration: int | Unset = UNSET
    time: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        duration = self.duration

        time = self.time

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if duration is not UNSET:
            field_dict["duration"] = duration
        if time is not UNSET:
            field_dict["time"] = time

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name", UNSET)

        duration = d.pop("duration", UNSET)

        time = d.pop("time", UNSET)

        get_playlist_response_200_list_item = cls(
            name=name,
            duration=duration,
            time=time,
        )

        get_playlist_response_200_list_item.additional_properties = d
        return get_playlist_response_200_list_item

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
