DEBUG = False

def dbgPrint(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)