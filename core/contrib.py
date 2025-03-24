def replace_asterix_with_italic(msg: str) -> str:
    asterix_count = msg.count('*')
    for _ in range(asterix_count//2):
        msg = msg.replace('*', '<i>', 1)
        msg = msg.replace('*', '</i>', 1)
    msg = msg.replace('*', '')
    return msg