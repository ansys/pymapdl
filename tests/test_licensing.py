"""Test PyMAPDL license.py module."""

import pytest

from ansys.mapdl.core import licensing, errors


FAKE_LICENSE_CONFIG = """
GARBAGE-LINE
;SERVER=1055@mysrv
;ANSYSLI_SERVERS=2325@mysrv
SERVER=1055@255.166.88.70
ANSYSLI_SERVERS=2325@255.166.88.70
SERVER=1055@localhost
ANSYSLI_SERVERS=2325@localhost
"""

# TEST-NET-3 (not quite a black hole, but set aside by RFC 5737)
test_net_3 = "203.0.113.0"


# check if there is any license info
try:
    LIC_CONFIG = licensing.get_license_server_config()
except FileNotFoundError:
    LIC_CONFIG = ""

skip_no_lic_srv = pytest.mark.skipif(not LIC_CONFIG, reason="Requires license server config")


def test_parse_lic_config(tmpdir):
    # temporarily write to disk to read this later
    lic_config_path = tmpdir.join('ansyslmd.ini')
    with open(lic_config_path, 'w') as fid:
        fid.write(FAKE_LICENSE_CONFIG)

    servers = licensing.parse_lic_config(lic_config_path)

    # ensure order is preserved
    expected = [
        (1055, '255.166.88.70'),
        (2325, '255.166.88.70'),
        (1055, 'localhost'),
        (2325, 'localhost'),
    ]

    assert servers == expected


@skip_no_lic_srv
def test_ping_lic_srv():
    port, host = LIC_CONFIG[0]
    assert licensing.check_port(host, port)


def test_ping_local_host():
    assert licensing.check_port('localhost')


def test_check_port_fail():
    # Expect this to fail
    assert not licensing.check_port(test_net_3, timeout=1)


@skip_no_lic_srv
def test_checkout_license():
    output = licensing.checkout_license('meba')


def test_checkout_license_fail():
    output = licensing.checkout_license('meba', test_net_3, 1055)
    assert "CHECKOUT FAILED" in output


@skip_no_lic_srv
def test_check_mech_license_available():
    licensing.check_mech_license_available()


def test_check_mech_license_available_fail():
    with pytest.raises(errors.LicenseServerConnectionError):
        licensing.check_mech_license_available(test_net_3)
