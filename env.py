import os

FANCY_VERBOSE = False
WAIT_ON_ERRORS = False


def guess_env_preferences():
    envstr = str(os.environ).upper()
    if "PYCHARM" in envstr:
        global WAIT_ON_ERRORS
        WAIT_ON_ERRORS = True
        global FANCY_VERBOSE
        FANCY_VERBOSE = True


guess_env_preferences()

print(f"Fancy CLI Settings: Wait on errors: {WAIT_ON_ERRORS}  verbose:{FANCY_VERBOSE}")
