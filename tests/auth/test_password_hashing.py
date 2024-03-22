import pytest

from src.auth import utils


@pytest.fixture
def fake_db_pass() -> str:
    return utils.hash_password("pass1234")


@pytest.fixture()
def plain_pass():
    return "pass1234"


def test_success_hash(plain_pass, fake_db_pass):
    assert utils.check_password(plain_pass, fake_db_pass)


@pytest.mark.parametrize("fake_pass", [("pa$s1234"), ("pass!234")])
def test_wrong_pass(fake_pass, fake_db_pass):
    assert not utils.check_password(fake_pass, fake_db_pass)
