import os
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent


def test_compose_has_expected_services():
    compose = yaml.safe_load((ROOT / "docker-compose.yml").read_text())
    services = compose["services"]

    assert {"pihole", "unbound"}.issubset(set(services))
    assert services["pihole"]["ports"][0] == "53:53/tcp"
    assert services["unbound"]["ports"][0] == "5353:5353/udp"
    assert services["pihole"]["environment"]["PIHOLE_DNS_"] == "172.20.0.2#5353"


def test_unbound_config_has_expected_settings():
    config = (ROOT / "config" / "unbound" / "unbound.conf").read_text()

    assert "port: 5353" in config
    assert "interface: 0.0.0.0" in config
    assert "forward-addr: 1.1.1.1" in config


def test_core_scripts_exist_and_are_executable():
    for relative_path in ["scripts/backup.sh", "scripts/restore.sh"]:
        path = ROOT / relative_path
        assert path.exists()
        assert os.access(path, os.X_OK)


def test_dnsmasq_bypass_config_exists():
    path = ROOT / "data" / "dnsmasq" / "99-bypass.conf"
    assert path.exists()

    config = path.read_text()
    assert "dhcp-host=" in config
    assert "tag:skip_pihole" in config
    assert "1.1.1.1" in config
