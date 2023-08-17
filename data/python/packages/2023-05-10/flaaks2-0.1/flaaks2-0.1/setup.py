from setuptools import setup

setup(
    name='flaaks2',
    version='0.1',
    license='MIT',
    author="Mario Nascimento",
    author_email='marionascimento047@gmail.com',
    packages=['flaaks'],
    keywords='example project',
    install_requires=[
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'background_task=flaaks.background_task:configure_package',
            'post_install=flaaks.post_install:run',
        ]
    }
)
