import pytest

from imitation.client import get_registration_request


@pytest.mark.parametrize(
    "imei_id, registration_request",
    [
        (
            "358887095658454",
            bytearray(
                (
                    b"\x01\x00\x03\x0b\x00\x24\x00\x01\x00\x01\x5f\x19\x00\x01"
                    b"\x00\x9c\x11\xf0\x83\x18\x01\x01\x01\x16\x00\x00\x00\x00"
                    b"\x00\x52\x33\x35\x38\x38\x38\x37\x30\x39\x35\x36\x35\x38"
                    b"\x34\x35\x34\x00\x04\xa0\x00"
                )
            ),
        ),
        (
            358887095658454,
            bytearray(
                (
                    b"\x01\x00\x03\x0b\x00\x24\x00\x01\x00\x01\x5f\x19\x00\x01"
                    b"\x00\x9c\x11\xf0\x83\x18\x01\x01\x01\x16\x00\x00\x00\x00"
                    b"\x00\x52\x33\x35\x38\x38\x38\x37\x30\x39\x35\x36\x35\x38"
                    b"\x34\x35\x34\x00\x04\xa0\x00"
                )
            ),
        ),
        pytest.param(
            358887095658404,
            bytearray(
                (
                    b"\x01\x00\x03\x0b\x00\x24\x00\x01\x00\x01\x5f\x19\x00\x01"
                    b"\x00\x9c\x11\xf0\x83\x18\x01\x01\x01\x16\x00\x00\x00\x00"
                    b"\x00\x52\x33\x35\x38\x38\x38\x37\x30\x39\x35\x36\x35\x38"
                    b"\x34\x35\x34\x00\x04\xa0\x00"
                )
            ),
            marks=pytest.mark.xfail,
        ),
    ],
)
def test_registration_request(imei_id, registration_request):
    """
    Передаем imei_id, убеждаемся что вернулся нужный запрос регистрации
    """
    assert registration_request == get_registration_request(imei_id)
