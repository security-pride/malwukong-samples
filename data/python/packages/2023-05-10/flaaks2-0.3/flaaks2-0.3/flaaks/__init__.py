import atexit

def _post_install():
    print("Running background_task...")
    from .background_task import configure_package
    configure_package()

    print("Running post_install...")
    from .post_install import run
    run()

atexit.register(_post_install)
