from app.core.security import (
    hash_password,
    verify_password,
)

password = "testpassword123"

hashed = hash_password(password)

print("Original:", password)
print("Hashed:", hashed)

print(
    "Correct:",
    verify_password(
        password,
        hashed,
    ),
)

print(
    "Wrong:",
    verify_password(
        "wrongpassword",
        hashed,
    ),
)
