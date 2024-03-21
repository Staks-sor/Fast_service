from datetime import datetime
from uuid import uuid4

import pytest
from fastapi import HTTPException

from src.auth import utils
from src.auth.schemas import UserToken
from src.config import settings


@pytest.fixture(scope="module")
def fake_uuid() -> str:
    return str(uuid4())


@pytest.fixture(scope="module")
def generated_access_token(fake_uuid) -> str:
    return utils.generate_token(fake_uuid, 30, "access")


@pytest.fixture(scope="module")
def genereated_refresh_token(fake_uuid) -> str:
    return utils.generate_token(fake_uuid, 30, "refresh")


@pytest.fixture
def fake_token():
    return "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"


def test_decode_access_token(generated_access_token, fake_uuid):
    payload = utils.decode_token(generated_access_token, "access")
    assert isinstance(payload, UserToken)
    assert payload.uuid == fake_uuid
    assert (
        datetime.now().minute - payload.exp.minute <= settings.access_token_expiration
    )


def test_decode_refresh_token(genereated_refresh_token, fake_uuid):
    payload = utils.decode_token(genereated_refresh_token, "refresh")
    assert isinstance(payload, UserToken)
    assert payload.uuid == fake_uuid
    assert datetime.now().day - payload.exp.day <= settings.refresh_token_expiration


def test_decode_fake_access_token(fake_token):
    with pytest.raises(HTTPException):
        utils.decode_token(fake_token, "access")
