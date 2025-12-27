from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="GetDeviceInfoResponse200")


@_attrs_define
class GetDeviceInfoResponse200:
    """
    Attributes:
        name (str | Unset):  Example: My Canvas.
        version (str | Unset):  Example: 1.0.0.
        board_model (str | Unset):  Example: sps_s3_v6_n16r8.
        screen_model (str | Unset):  Example: EL073TF1.
        battery (int | Unset):  Example: 85.
        fs_ready (bool | Unset):  Example: True.
        total_size (int | Unset):  Example: 15630401536.
        free_size (int | Unset):  Example: 15626108928.
        sleep_duration (int | Unset):  Example: 259200.
        max_idle (int | Unset):  Example: 120.
        network_type (int | Unset): 2 for Wi-Fi Example: 2.
        width (int | Unset):  Example: 480.
        height (int | Unset):  Example: 800.
        sta_ssid (str | Unset):  Example: My WiFi.
        sta_ip (str | Unset):  Example: 192.168.1.100.
        image (str | Unset):  Example: /gallerys/default/f1.jpg.
        next_time (int | Unset):  Example: 1739182800.
        gallery (str | Unset):  Example: default.
        playlist (str | Unset):
        play_type (int | Unset): 0 for single image, 1 for gallery slideshow, 2 for playlist. Example: 1.
    """

    name: str | Unset = UNSET
    version: str | Unset = UNSET
    board_model: str | Unset = UNSET
    screen_model: str | Unset = UNSET
    battery: int | Unset = UNSET
    fs_ready: bool | Unset = UNSET
    total_size: int | Unset = UNSET
    free_size: int | Unset = UNSET
    sleep_duration: int | Unset = UNSET
    max_idle: int | Unset = UNSET
    network_type: int | Unset = UNSET
    width: int | Unset = UNSET
    height: int | Unset = UNSET
    sta_ssid: str | Unset = UNSET
    sta_ip: str | Unset = UNSET
    image: str | Unset = UNSET
    next_time: int | Unset = UNSET
    gallery: str | Unset = UNSET
    playlist: str | Unset = UNSET
    play_type: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        version = self.version

        board_model = self.board_model

        screen_model = self.screen_model

        battery = self.battery

        fs_ready = self.fs_ready

        total_size = self.total_size

        free_size = self.free_size

        sleep_duration = self.sleep_duration

        max_idle = self.max_idle

        network_type = self.network_type

        width = self.width

        height = self.height

        sta_ssid = self.sta_ssid

        sta_ip = self.sta_ip

        image = self.image

        next_time = self.next_time

        gallery = self.gallery

        playlist = self.playlist

        play_type = self.play_type

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if version is not UNSET:
            field_dict["version"] = version
        if board_model is not UNSET:
            field_dict["board_model"] = board_model
        if screen_model is not UNSET:
            field_dict["screen_model"] = screen_model
        if battery is not UNSET:
            field_dict["battery"] = battery
        if fs_ready is not UNSET:
            field_dict["fs_ready"] = fs_ready
        if total_size is not UNSET:
            field_dict["total_size"] = total_size
        if free_size is not UNSET:
            field_dict["free_size"] = free_size
        if sleep_duration is not UNSET:
            field_dict["sleep_duration"] = sleep_duration
        if max_idle is not UNSET:
            field_dict["max_idle"] = max_idle
        if network_type is not UNSET:
            field_dict["network_type"] = network_type
        if width is not UNSET:
            field_dict["width"] = width
        if height is not UNSET:
            field_dict["height"] = height
        if sta_ssid is not UNSET:
            field_dict["sta_ssid"] = sta_ssid
        if sta_ip is not UNSET:
            field_dict["sta_ip"] = sta_ip
        if image is not UNSET:
            field_dict["image"] = image
        if next_time is not UNSET:
            field_dict["next_time"] = next_time
        if gallery is not UNSET:
            field_dict["gallery"] = gallery
        if playlist is not UNSET:
            field_dict["playlist"] = playlist
        if play_type is not UNSET:
            field_dict["play_type"] = play_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name", UNSET)

        version = d.pop("version", UNSET)

        board_model = d.pop("board_model", UNSET)

        screen_model = d.pop("screen_model", UNSET)

        battery = d.pop("battery", UNSET)

        fs_ready = d.pop("fs_ready", UNSET)

        total_size = d.pop("total_size", UNSET)

        free_size = d.pop("free_size", UNSET)

        sleep_duration = d.pop("sleep_duration", UNSET)

        max_idle = d.pop("max_idle", UNSET)

        network_type = d.pop("network_type", UNSET)

        width = d.pop("width", UNSET)

        height = d.pop("height", UNSET)

        sta_ssid = d.pop("sta_ssid", UNSET)

        sta_ip = d.pop("sta_ip", UNSET)

        image = d.pop("image", UNSET)

        next_time = d.pop("next_time", UNSET)

        gallery = d.pop("gallery", UNSET)

        playlist = d.pop("playlist", UNSET)

        play_type = d.pop("play_type", UNSET)

        get_device_info_response_200 = cls(
            name=name,
            version=version,
            board_model=board_model,
            screen_model=screen_model,
            battery=battery,
            fs_ready=fs_ready,
            total_size=total_size,
            free_size=free_size,
            sleep_duration=sleep_duration,
            max_idle=max_idle,
            network_type=network_type,
            width=width,
            height=height,
            sta_ssid=sta_ssid,
            sta_ip=sta_ip,
            image=image,
            next_time=next_time,
            gallery=gallery,
            playlist=playlist,
            play_type=play_type,
        )

        get_device_info_response_200.additional_properties = d
        return get_device_info_response_200

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
