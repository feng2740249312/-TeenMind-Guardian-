import hashlib

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def mask_email(email: str) -> str:
    try:
        name, domain = email.split('@')
        return f"{name[0]}***@{domain}"
    except Exception:
        return email
