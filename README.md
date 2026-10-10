# Pi-hole with Unbound

This project runs Pi-hole with Unbound as the upstream recursive DNS resolver.

## Raspberry Pi quick start

Use this during the first setup of a Raspberry Pi that will act as the network DNS server.

1. Install Raspberry Pi OS Lite or Desktop on the SD card with Raspberry Pi Imager.
2. Enable SSH if needed, set a hostname, and choose a static or reserved IP on your network.
3. Boot the Pi and log in.
4. Install Docker and the Compose plugin:

```bash
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER
newgrp docker
```

5. Clone this project or copy the files onto the Pi:

```bash
git clone <your-repo-url> ~/mini
cd ~/mini
cp .env.example .env
```

6. Edit `.env` and set the actual host IP and password:

```env
PIHOLE_PASSWORD=your-strong-password
PIHOLE_HOST_IP=192.168.1.50
```

7. Start the stack:

```bash
docker compose up -d
```

8. Open the Pi-hole web UI at `http://192.168.1.50/admin`.
9. Log in with the password from `.env`.
10. Set your router DHCP to hand out the Pi as the DNS server, or configure each device manually to use `192.168.1.50`.

This is the simplest way to get the service running early in the Pi setup flow with minimal changes.

## Raspberry Pi OS Lite: one-command bootstrap

This is the most minimal path for a fresh Raspberry Pi OS Lite install. Run these commands on the Pi after the first boot:

```bash
curl -fsSL https://get.docker.com | sh && \
  sudo usermod -aG docker "$USER" && \
  newgrp docker && \
  git clone <your-repo-url> ~/mini && \
  cd ~/mini && \
  cp .env.example .env && \
  sed -i 's#PIHOLE_HOST_IP=.*#PIHOLE_HOST_IP=192.168.1.50#' .env && \
  sed -i 's#PIHOLE_PASSWORD=.*#PIHOLE_PASSWORD=change-me-now#' .env && \
  docker compose up -d
```

Then open:

```text
http://192.168.1.50/admin
```

Log in with the password from `.env`, then set your router or devices to use the Pi as the DNS server.

## Requirements

- Docker
- Docker Compose
- A Linux, macOS, or Windows host with Docker Desktop or a compatible Docker engine

## Quick start

1. Copy the sample environment file:
   cp .env.example .env
2. Update the values in .env to match the host.
3. Start the stack:
   docker compose up -d
4. Open the Pi-hole admin interface at http://localhost/admin.
5. Use the default password from .env or change it before production use.

## Default ports

- DNS: 53/tcp and 53/udp
- Web UI: 80/tcp and 443/tcp
- Unbound: 5353/udp and 5353/tcp for internal resolver use

## Bypass specific clients

Pi-hole can be bypassed for selected devices by defining DHCP tags in the dnsmasq config file at `data/dnsmasq/99-bypass.conf`.

Example:

```conf
dhcp-host=aa:bb:cc:dd:ee:ff,media-box,set:skip_pihole
dhcp-host=11:22:33:44:55:66,printer,set:skip_pihole
dhcp-option=tag:skip_pihole,6,1.1.1.1,1.0.0.1
```

Replace the sample MAC addresses and hostnames with the devices you want to skip. When a host matches one of the configured entries, Docker's dnsmasq will send it to the upstream DNS server instead of Pi-hole.

## Backup and restore

- Backup:
  ./scripts/backup.sh
- Restore:
  ./scripts/restore.sh /path/to/backup.tar.gz

The backup script archives the Pi-hole and Unbound data directories so they can be restored on the same or another host.

## Notes

- The project is intentionally lightweight and simple.
- The default network mode is bridge networking.
- Set PIHOLE_HOST_IP to the LAN address of the host when you want Pi-hole to advertise the correct local IP.
