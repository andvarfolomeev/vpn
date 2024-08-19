from wg_wrapper.config import WGConfigStrBuilder, WGInterfaceConfigStrBuilder
from wg_wrapper.schemas import WGKeys, WGPeerConfig, WGServerConfig


def test_wg_config_builder_one_variable():
    assert (
        WGConfigStrBuilder().add_variable("PreUp", "some_smart_command").build()
        == f"PreUp = some_smart_command"
    )
    assert (
        WGConfigStrBuilder()
        .add_variable("PostUp", "some_smart_command for post up")
        .build()
        == "PostUp = some_smart_command for post up"
    )
    assert (
        WGConfigStrBuilder()
        .add_variable("PreDown", "some_smart_command for pre down")
        .build()
        == "PreDown = some_smart_command for pre down"
    )
    assert (
        WGConfigStrBuilder().add_variable("PreUp", ["some_smart_command"]).build()
        == f"PreUp = some_smart_command"
    )
    assert (
        WGConfigStrBuilder()
        .add_variable("PostUp", ["some_smart_command for post up"])
        .build()
        == "PostUp = some_smart_command for post up"
    )
    assert (
        WGConfigStrBuilder()
        .add_variable("PreDown", ["some_smart_command for pre down"])
        .build()
        == "PreDown = some_smart_command for pre down"
    )


def test_wg_config_builder_one_variable_as_list():
    assert (
        WGConfigStrBuilder()
        .add_variable("PreUp", ["some smart", "but stupid_command"])
        .build()
        == "PreUp = some smart\nPreUp = but stupid_command"
    )
    assert (
        WGConfigStrBuilder()
        .add_variable("PreUp", ["some smart", "but stupid_command", "and other"])
        .build()
        == "PreUp = some smart\nPreUp = but stupid_command\nPreUp = and other"
    )


def test_wg_config_builder_one_empty_variable():
    assert WGConfigStrBuilder().add_variable("PreUp", []).build() == ""


def test_wg_config_builder_two_variables():
    assert (
        WGConfigStrBuilder()
        .add_variable("PreUp", "hello")
        .add_variable("PostUp", "world")
        .build()
        == "PreUp = hello\nPostUp = world"
    )


def test_wg_interface_config_builder_without_peers():
    interface = WGServerConfig(
        keys=WGKeys(
            private_key="wEoVMj92P+E3fQXVf9IixWJqpCqcnP/4OfvrB1g3zmY=",
            public_key="wEoVMj92P+E3fQXVf9IixWJqpCqcnP/da123B1g3zmY=",
        ),
        address="163.196.224.189/24",
        listen_port="54332",
        pre_up=[],
        post_up=[],
        pre_down=[],
        post_down=[],
    )
    assert (
        WGInterfaceConfigStrBuilder().add_interface(interface).build()
        == """[Interface]
PrivateKey = wEoVMj92P+E3fQXVf9IixWJqpCqcnP/4OfvrB1g3zmY=
Address = 163.196.224.189/24
ListenPort = 54332"""
    )


def test_wg_interface_config_builder_with_peers():
    interface = WGServerConfig(
        keys=WGKeys(
            private_key="wEoVMj92P+E3fQXVf9IixWJqpCqcnP/4OfvrB1g3zmY=",
            public_key="wEoVMj92P+E3fQXVf9IixWJqpCqcnP/da123B1g3zmY=",
        ),
        address="163.196.224.189/24",
        listen_port="54332",
        pre_up=[],
        post_up=[],
        pre_down=[],
        post_down=[],
    )
    peers = [
        WGPeerConfig(
            WGKeys(private_key="some-public-key", public_key="some-private-key"),
            "0.0.0.0/0",
        ),
        WGPeerConfig(
            WGKeys(
                private_key="LEsliEny+aMcWcRbh8Qf414XsQHSBOAFk3TaEk/aSD0=",
                public_key="LEsliEny+aMc12dDqwdf414XsQHSBOAFk3TaEk/aSD0=",
            ),
            "1.2.3.4/5",
        ),
    ]
    assert (
        WGInterfaceConfigStrBuilder().add_interface(interface).add_peers(peers).build()
        == """[Interface]
PrivateKey = wEoVMj92P+E3fQXVf9IixWJqpCqcnP/4OfvrB1g3zmY=
Address = 163.196.224.189/24
ListenPort = 54332
[Peer]
PublicKey = some-public-key
AllowedIPs = 0.0.0.0/0
[Peer]
PublicKey = LEsliEny+aMcWcRbh8Qf414XsQHSBOAFk3TaEk/aSD0=
AllowedIPs = 1.2.3.4/5"""
    )
