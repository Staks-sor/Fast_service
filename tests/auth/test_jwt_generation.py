from fastapi import HTTPException
import pytest
from uuid import uuid4

from src.auth import utils
from src.auth.schemas import UserToken
from datetime import datetime

@pytest.fixture(scope='module')
def fake_uuid() -> str:
    return str(uuid4())

@pytest.fixture(scope='module')
def generated_access_token(fake_uuid) -> str:
    return utils.generate_token(fake_uuid, 30, 'access')

@pytest.fixture(scope='module')
def genereated_refresh_token(fake_uuid) -> str:
    return utils.generate_token(fake_uuid, 30, 'refresh')


@pytest.fixture
def fake_acces_token():
    return "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"


def test_decode_access_token(generated_access_token, fake_uuid):
    payload = utils.decode_token(generated_access_token, 'access')
    assert isinstance(payload, UserToken)
    assert payload.uuid == fake_uuid
    assert datetime.now().minute - payload.exp.minute <= 30 



def test_decode_fake_access_token(fake_acces_token):
    with pytest.raises(HTTPException):
        utils.decode_token(fake_acces_token, 'access')