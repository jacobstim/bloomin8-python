from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_gallery_response_200_data_item import GetGalleryResponse200DataItem


T = TypeVar("T", bound="GetGalleryResponse200")


@_attrs_define
class GetGalleryResponse200:
    """
    Attributes:
        data (list[GetGalleryResponse200DataItem] | Unset):
        total (int | Unset):  Example: 1.
        offset (int | Unset):
        limit (int | Unset):  Example: 10.
    """

    data: list[GetGalleryResponse200DataItem] | Unset = UNSET
    total: int | Unset = UNSET
    offset: int | Unset = UNSET
    limit: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        data: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.data, Unset):
            data = []
            for data_item_data in self.data:
                data_item = data_item_data.to_dict()
                data.append(data_item)

        total = self.total

        offset = self.offset

        limit = self.limit

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if data is not UNSET:
            field_dict["data"] = data
        if total is not UNSET:
            field_dict["total"] = total
        if offset is not UNSET:
            field_dict["offset"] = offset
        if limit is not UNSET:
            field_dict["limit"] = limit

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.get_gallery_response_200_data_item import GetGalleryResponse200DataItem

        d = dict(src_dict)
        _data = d.pop("data", UNSET)
        data: list[GetGalleryResponse200DataItem] | Unset = UNSET
        if _data is not UNSET:
            data = []
            for data_item_data in _data:
                data_item = GetGalleryResponse200DataItem.from_dict(data_item_data)

                data.append(data_item)

        total = d.pop("total", UNSET)

        offset = d.pop("offset", UNSET)

        limit = d.pop("limit", UNSET)

        get_gallery_response_200 = cls(
            data=data,
            total=total,
            offset=offset,
            limit=limit,
        )

        get_gallery_response_200.additional_properties = d
        return get_gallery_response_200

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
