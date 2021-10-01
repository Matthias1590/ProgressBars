from setuptools import setup

def readme():
    with open("README.md", "r") as f:
        return f.read()

setup(
    name="progressbars",
    version="1.1.8",
    description="A python package to display progress of loops to the user",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/Matthias1590/ProgressBars",
    author="Matthias Wijnsma",
    author_email="matthiasx95@gmail.com",
    license="MIT",
    packages=["progressbars"]
)