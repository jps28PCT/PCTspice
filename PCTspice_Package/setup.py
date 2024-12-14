from setuptools import setup, find_packages

setup(
    name="PCTspice",
    author="Jacob Smithmyer",
    author_email="jps28@pct.edu",
    version="1.1.0",
    packages=find_packages(),
    install_requires=[
        'sympy'
    ],

    entry_points={
        "console_scripts": [
            "PCTspice = PCTspice:runPCTspice"
        ],
    },
)