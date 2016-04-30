from setuptools import setup, find_packages

setup(
    name="ytfetch",
    version="0.0.1",
    author="Ben Greenberg",
    packages=find_packages(),
    install_requires=["youtube-dl"],
    entry_points={
        'console_scripts': ['ytsync=ytsync.cmd:main']
    }
)
