import hashlib
import os


def hash_password(password):
    salt = os.urandom(32)
    encoded_password = password.encode('utf-8')
    password_hash = hashlib.sha256(salt + encoded_password).hexdigest()
    return password_hash, salt


def check_password(password, password_hash, salt):
    encoded_password = password.encode('utf-8')
    hash_result = hashlib.sha256(salt + encoded_password).hexdigest()
    return hash_result == password_hash
