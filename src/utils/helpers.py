import ctypes
import time

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def request_admin(executable, file):
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", executable, file, None, 1
    )


def create_message(identifier, msg_type, data):
    return {
        "id": identifier,
        "timestamp": time.time(),
        "data": {"type": msg_type, **data}
    }