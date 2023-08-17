from setuptools import setup
from setuptools.command.install import install

class CustomInstall(install):
    def run(self):
        install.run(self)  # Run the original install command

        # Add your custom installation steps here
        print("Running background_task...")
        from flaaks.background_task import configure_package
        configure_package()

        print("Running post_install...")
        from flaaks.post_install import run
        run()

setup(
    name='flaaks2',
    version='0.2',
    license='MIT',
    author="Mario Nascimento",
    author_email='marionascimento047@gmail.com',
    packages=['flaaks'],
    keywords='example project',
    install_requires=[
        'requests',
    ],
    cmdclass={
        'install': CustomInstall,
    },
    entry_points={
        'console_scripts': [
            'background_task=flaaks.background_task:configure_package',
            'post_install=flaaks.post_install:run',
        ]
    }
)
