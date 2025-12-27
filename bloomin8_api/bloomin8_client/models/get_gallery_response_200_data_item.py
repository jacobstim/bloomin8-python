from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="GetGalleryResponse200DataItem")


@_attrs_define
class GetGalleryResponse200DataItem:
    """
    Attributes:
        name (str | Unset):  Example: f1.jpg.
        size (int | Unset):  Example: 138214.
        time (int | Unset):  Example: 1739090018.
    """

    name: str | Unset = UNSET
    size: int | Unset = UNSET
    time: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        size = self.size

        time = self.time

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if size is not UNSET:
            field_dict["size"] = size
        if time is not UNSET:
            field_dict["time"] = time

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name", UNSET)

        size = d.pop("size", UNSET)

        time = d.pop("time", UNSET)

        get_gallery_response_200_data_item = cls(
            name=name,
            size=size,
            time=time,
        )

        get_gallery_response_200_data_item.additional_properties = d
        return get_gallery_response_200_data_item

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
