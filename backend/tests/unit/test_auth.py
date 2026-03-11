from app.auth.hashing import hash_password, verify_password


def test_password_hashing():
    password = "securepassword123"
    hashed = hash_password(password)
    assert hashed != password
    assert verify_password(password, hashed)


def test_wrong_password_fails():
    hashed = hash_password("correctpassword")
    assert not verify_password("wrongpassword", hashed)
