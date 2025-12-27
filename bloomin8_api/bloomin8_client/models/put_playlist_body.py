from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.put_playlist_body_type import PutPlaylistBodyType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.put_playlist_body_list_item import PutPlaylistBodyListItem


T = TypeVar("T", bound="PutPlaylistBody")


@_attrs_define
class PutPlaylistBody:
    """
    Attributes:
        name (str):  Example: daily_show.
        type_ (PutPlaylistBodyType):  Example: duration.
        list_ (list[PutPlaylistBodyListItem]):
        time_offset (int | Unset): In seconds, for 'time' type.
    """

    name: str
    type_: PutPlaylistBodyType
    list_: list[PutPlaylistBodyListItem]
    time_offset: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        type_ = self.type_.value

        list_ = []
        for list_item_data in self.list_:
            list_item = list_item_data.to_dict()
            list_.append(list_item)

        time_offset = self.time_offset

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "type": type_,
                "list": list_,
            }
        )
        if time_offset is not UNSET:
            field_dict["time_offset"] = time_offset

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.put_playlist_body_list_item import PutPlaylistBodyListItem

        d = dict(src_dict)
        name = d.pop("name")

        type_ = PutPlaylistBodyType(d.pop("type"))

        list_ = []
        _list_ = d.pop("list")
        for list_item_data in _list_:
            list_item = PutPlaylistBodyListItem.from_dict(list_item_data)

            list_.append(list_item)

        time_offset = d.pop("time_offset", UNSET)

        put_playlist_body = cls(
            name=name,
            type_=type_,
            list_=list_,
            time_offset=time_offset,
        )

        put_playlist_body.additional_properties = d
        return put_playlist_body

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
