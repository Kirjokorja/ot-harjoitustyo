from bcrypt import gensalt, hashpw, checkpw

class PasswordService:
    """Tarjoaa salasanapalveluja."""

    def hash_password(self, password):
        salt = gensalt()
        password_bytes = password.encode("utf-8")
        return hashpw(password_bytes, salt)

    def password_match(self, password_hash, password_confirm):
        confirm_bytes = password_confirm.encode('utf-8')
        return checkpw(confirm_bytes, password_hash)
