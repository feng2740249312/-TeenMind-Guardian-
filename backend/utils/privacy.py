def anonymize_user_id(user_id: str) -> str:
    return f"anon_{hash(user_id) & 0xffff}"

def remove_pii(text: str) -> str:
    # 极简占位：实际可加入手机号/邮箱/地址等识别
    return text.replace('\n', ' ').strip()
