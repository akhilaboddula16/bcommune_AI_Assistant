from app.security.jwt_handler import (
    create_access_token,
    decode_token,
)

token = create_access_token(
    {
        "sub": "1",
        "email": "admin@bcommune.com",
    }
)

print("Generated Token:")
print(token)

print("\nDecoded Payload:")
print(decode_token(token))