# wg-service

The service provides creating new tunnels in WireGuard

## Configuration

Place configuration to `.env`.

```bash
WG_SERVICE_POSTGRES_HOST='127.0.0.1'
WG_SERVICE_POSTGRES_DB='postgres'
WG_SERVICE_POSTGRES_EXTERNAL_PORT='5432'
WG_SERVICE_POSTGRES_USER='postgres'
WG_SERVICE_POSTGRES_PASSWORD='postgres'

WG_SERVICE_IP_ADDRESS="<ip_here>"
WG_SERVICE_WG0_ADDRESS='192.168.0.3'
WG_SERVICE_WG0_LISTEN_PORT='51871'
WG_SERVICE_WG0_PRE_UP=''
WG_SERVICE_WG0_POST_UP='iptables -A FORWARD -i %i -j ACCEPT; iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE'
WG_SERVICE_WG0_PRE_DOWN=''
WG_SERVICE_WG0_POST_DOWN='iptables -D FORWARD -i %i -j ACCEPT; iptables -t nat -D POSTROUTING -o eth0 -j MASQUERADE'

WG_SERVICE_WG_START_CLIENT_IP='10.0.0.2'
WG_SERVICE_WG_CLIENT_SUBNET='32'
```

## Use cases

### UC-1 Enabling WireGuard server interface

| Atribute       | Value                                                                                                                                                                                                  |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Actor          | System                                                                                                                                                                                                 |
| Description    | Enabling WireGuard server interface                                                                                                                                                                    |
| Pre-conditions | Environment variables must be settled in `.env` file                                                                                                                                                   |
| Result         | On start, the system must run interface of WireGuard server. If server configuration is not existed, the system must create it. Wireguard server must be enabled to establish connection with clients. |

### UC-2 Getting peer

| Atribute       | Value                                                                                                                                               |
| -------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| Actor          | App                                                                                                                                                 |
| Description    | Getting peer                                                                                                                                        |
| Pre-conditions | The user has logged in and requested VPN access                                                                                                     |
| Result         | Output includes public key, allowed IPs, endpoint, persistent leep alive and string configuration of tunnel. It must notify if peer is not created. |

### UC-3 Creating peer

| Atribute       | Value                                                                                                                              |
| -------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| Actor          | App                                                                                                                                |
| Description    | Setting peer                                                                                                                       |
| Pre-conditions | The user has logged in and requested VPN access                                                                                    |
| Result         | Peer must be created. Output includes public key, allowed IPs, endpoint, persistent leep alive and string configuration of tunnel. |

### UC-4 Deleting peer

| Atribute       | Value                                                        |
| -------------- | ------------------------------------------------------------ |
| Actor          | App                                                          |
| Description    | Deletting peer                                               |
| Pre-conditions | The user has logged in and requested to remove VPN access    |
| Result         | Peer must be created. It must notify if peer is not created. |
