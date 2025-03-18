from setuptools import setup, find_packages

setup(
    name="mountain-gorilla-cli",
    version="0.1.0",
    description="Mountain Gorilla Command Center - ASCII-based AI Bot Manager",
    author="Your Name",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "mgcc=mountain_gorilla.cli:mgcc_cli",
        ],
    },
    install_requires=[
        "click>=8.0.0",
    ],
    python_requires=">=3.7",
)
