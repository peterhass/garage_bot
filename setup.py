from setuptools import setup

setup(name='garage_bot',
    version='0.2',
    description='',
    scripts=['bin/garage_bot', 'bin/garage_bot_config'],
    packages=['garage_bot', 'garage_bot.resources'],
    package_data={
        'garage_bot.resources': ['*']
        },
    install_requires=[
        'python-telegram-bot',
        'rpi.gpio'
    ])
