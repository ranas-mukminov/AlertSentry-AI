import pytest

from src.threat_intel.indicators import file_hash, public_ip


@pytest.mark.parametrize(
    "value",
    [
        "192.168.1.100",  # RFC1918 (the Splunk sample alert)
        "10.0.0.5",
        "172.16.3.4",
        "127.0.0.1",
        "169.254.169.254",  # link-local / cloud metadata
        "100.64.0.1",  # CGNAT
        "::1",
        "fd00::1",
        "::ffff:10.0.0.1",
        "8.8.8.8/../../files/x",
        "not-an-ip",
        "",
        None,
    ],
)
def test_public_ip_rejects_internal_and_malformed(value):
    assert public_ip(value) is None


def test_public_ip_accepts_and_canonicalises_global():
    assert public_ip(" 8.8.8.8 ") == "8.8.8.8"
    assert public_ip("::ffff:8.8.8.8") == "8.8.8.8"
    assert public_ip("2001:4860:4860:0000:0000:0000:0000:8888") == "2001:4860:4860::8888"


def test_file_hash():
    sha256 = "E3B0C44298FC1C149AFBF4C8996FB92427AE41E4649B934CA495991B7852B855"
    assert file_hash(sha256) == sha256.lower()
    assert file_hash("d41d8cd98f00b204e9800998ecf8427e") is not None
    assert file_hash("da39a3ee5e6b4b0d3255bfef95601890afd80709") is not None
    assert file_hash("../ip_addresses/8.8.8.8") is None
    assert file_hash("zz" * 16) is None
    assert file_hash(None) is None
