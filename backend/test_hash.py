from app.security.hashing import hash_password, verify_password

password = "Bcommune@123"

hashed = hash_password(password)

print(hashed)
print(verify_password(password, hashed))