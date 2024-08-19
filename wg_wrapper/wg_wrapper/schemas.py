from dataclasses import dataclass


@dataclass
class CommandResult:
    stdout: str
    stderr: str
    code: int | None


@dataclass
class WGKeys:
    private_key: str
    public_key: str


@dataclass
class WGPeerConfig:
    keys: WGKeys
    allowed_ips: str


@dataclass
class WGServerConfig:
    keys: WGKeys
    address: str
    listen_port: str | int
    pre_up: list[str]
    post_up: list[str]
    pre_down: list[str]
    post_down: list[str]
