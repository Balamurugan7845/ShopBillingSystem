from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

password = "admin123"

hashed_password = bcrypt.generate_password_hash(
    password
).decode('utf-8')

print("\nHashed Password:\n")
print(hashed_password)