"""Minimal smoke test so CI has a tests/ tree."""


def test_import_src_package():
    import src  # noqa: F401
