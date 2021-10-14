from setuptools import setup, find_packages

setup(
    name="anrg.mobscript",
    version="0.0.1",
    author="Oliver Eisenberg",
    packages=find_packages(),
    install_requires=[
        "networkx~=2.6.3",
        "Shapely~=1.7.1",
        "pygame~=2.0.1",
    ],
    entry_points={
        "console_scripts": [
            "mobscript=mobscript.main:main"
        ]
    }
)