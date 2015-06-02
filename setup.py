from setuptools import setup, find_packages

setup(
    name='crawler',
    install_requires=[
        "pyvirtualdisplay",
        "selenium",
        "redis",
        'jsonpickle',
	'xvfbwrapper'
    ],
)
