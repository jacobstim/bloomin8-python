from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PostSettingsBody")


@_attrs_define
class PostSettingsBody:
    """
    Attributes:
        name (str | Unset):  Example: Living Room Canvas.
        sleep_duration (int | Unset):  Example: 86400.
        max_idle (int | Unset):  Example: 300.
        idx_wake_sens (int | Unset):  Example: 3.
    """

    name: str | Unset = UNSET
    sleep_duration: int | Unset = UNSET
    max_idle: int | Unset = UNSET
    idx_wake_sens: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        sleep_duration = self.sleep_duration

        max_idle = self.max_idle

        idx_wake_sens = self.idx_wake_sens

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if sleep_duration is not UNSET:
            field_dict["sleep_duration"] = sleep_duration
        if max_idle is not UNSET:
            field_dict["max_idle"] = max_idle
        if idx_wake_sens is not UNSET:
            field_dict["idx_wake_sens"] = idx_wake_sens

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name", UNSET)

        sleep_duration = d.pop("sleep_duration", UNSET)

        max_idle = d.pop("max_idle", UNSET)

        idx_wake_sens = d.pop("idx_wake_sens", UNSET)

        post_settings_body = cls(
            name=name,
            sleep_duration=sleep_duration,
            max_idle=max_idle,
            idx_wake_sens=idx_wake_sens,
        )

        post_settings_body.additional_properties = d
        return post_settings_body

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
