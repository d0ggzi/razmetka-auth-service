import bcrypt


def hash_password(password):
    password_bytes = password.encode("utf-8")
    hashed_bytes = bcrypt.hashpw(password_bytes, bcrypt.gensalt(12))
    return hashed_bytes.decode("utf-8")


def check_password(password, hashed_password):
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))
