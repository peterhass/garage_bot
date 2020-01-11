from setuptools import setup

setup(name='garage_bot',
    version='0.1',
    description='',
    scripts=['bin/garage_bot'],
    packages=['garage_bot'],
    install_requires=[
        'python-telegram-bot',
        'rpi.gpio'
    ])
