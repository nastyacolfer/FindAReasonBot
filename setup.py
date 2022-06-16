from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="FindAReason_bot",
    version="1.0.0",
    author="nastyacolfer",
    author_email="nastyakolfer@gmail.com",
    description="Telegram bot which helps you find a reason",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nastyacolfer/FindAReasonBot",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Freeware",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    python_requires=">=3.10",
)
