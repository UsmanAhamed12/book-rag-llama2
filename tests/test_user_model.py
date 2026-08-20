import pytest

from app.models.database.user import UserDB


def test_user_constructor_maps_password_hash() -> None:
    user = UserDB(
        email="reader@example.com",
        password_hash="stored-hash",
    )

    assert user.email == "reader@example.com"
    assert user.hashed_password == "stored-hash"


def test_user_constructor_requires_password_hash() -> None:
    with pytest.raises(ValueError, match="password hash is required"):
        UserDB(email="reader@example.com")
