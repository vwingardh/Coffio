import string
import secrets

c = string.ascii_letters + string.digits + string.punctuation

secret_key = ''.join(secrets.choice(c) for i in range(67))

print(secret_key)
