from collections.abc import Iterable
from os import path

from wg_wrapper.consts import WG_DEFAULT_INTERFACE, WG_PATH
from wg_wrapper.schemas import WGPeerConfig, WGServerConfig


class WGConfigStrBuilder:
    lines: list[str]

    def __init__(self):
        self.lines = []

    def add_section(self, title: str) -> "WGConfigStrBuilder":
        self.lines.append(f"[{title}]")
        return self

    def add_simple_variable(self, name: str, value: str) -> "WGConfigStrBuilder":
        self.lines.append(f"{name} = {value}")
        return self

    def add_variable(self, name: str, value: list[str] | str) -> "WGConfigStrBuilder":
        if isinstance(value, list):
            for v in value:
                self.add_simple_variable(name, v)
        elif isinstance(value, str):
            self.add_simple_variable(name, value)
        return self

    def add_variables(
        self, variables: Iterable[tuple[str, list[str] | str]]
    ) -> "WGConfigStrBuilder":
        for [variable, value] in variables:
            self.add_variable(variable, value)
        return self

    def build(self) -> str:
        return "\n".join(self.lines)


class WGInterfaceConfigStrBuilder(WGConfigStrBuilder):

    def __init__(self):
        super().__init__()

    def add_interface(self, server: WGServerConfig) -> "WGInterfaceConfigStrBuilder":
        self.add_section("Interface")
        self.add_variables(
            [
                ("PrivateKey", server.keys.private_key),
                ("Address", server.address),
                ("ListenPort", str(server.listen_port)),
                ("PreUp", server.pre_up),
                ("PostUp", server.post_up),
                ("PreDown", server.pre_down),
                ("PostDown", server.post_down),
            ]
        )
        return self

    def add_peer(self, peer: WGPeerConfig) -> "WGInterfaceConfigStrBuilder":
        self.add_section("Peer")
        self.add_variables(
            [("PublicKey", peer.keys.public_key), ("AllowedIPs", peer.allowed_ips)]
        )
        return self

    def add_peers(self, peers: list[WGPeerConfig]) -> "WGInterfaceConfigStrBuilder":
        for peer in peers:
            self.add_peer(peer)
        return self


class WGTunelConfigStrBuilder(WGConfigStrBuilder):

    def __init__(self):
        super().__init__()

    def add_interface(
        self,
        peer: WGPeerConfig,
    ) -> "WGTunelConfigStrBuilder":
        self.add_section("Interface")
        self.add_variables(
            [
                ("PrivateKey", peer.keys.private_key),
                ("Address", peer.allowed_ips),
                ("DNS", "8.8.8.8"),
            ]
        )
        return self

    def add_peer(self, server: WGServerConfig) -> "WGTunelConfigStrBuilder":
        self.add_section("Peer")
        self.add_variables(
            [
                ("PublicKey", server.keys.public_key),
                ("AllowedIPs", "0.0.0.0/0"),
                ("Endpoint", f"{server.ip_address}:{server.listen_port}"),
                ("PersistentKeepalive", "20"),
            ]
        )
        return self


class WGInterfaceConfigWritter:
    interface_file: str

    def __init__(self, interface_file: str = WG_DEFAULT_INTERFACE):
        self.interface_file = interface_file

    def write(self, interface: WGServerConfig, peers: list[WGPeerConfig]) -> None:
        content = (
            WGInterfaceConfigStrBuilder().add_interface(interface).add_peers(peers)
        ).build()
        with open(path.join(WG_PATH, self.interface_file), "w") as file:
            file.write(content)


def wg0_config_exists() -> bool:
    return path.isfile(path.join(WG_PATH, WG_DEFAULT_INTERFACE))
