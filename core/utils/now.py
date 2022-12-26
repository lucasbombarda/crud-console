from datetime import datetime

def date_now() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")