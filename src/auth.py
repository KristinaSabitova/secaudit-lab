import hashlib
import hmac


def check_password(user, password):
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(),
                                 bytes.fromhex(user["salt"]), 200_000)
    return hmac.compare_digest(digest.hex(), user["password_hash"])
