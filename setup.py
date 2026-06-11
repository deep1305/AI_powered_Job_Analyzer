from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name= "AI Powered Job Analyzer",
    version= "1.0.0",
    author= "Deep",
    packages=find_packages(),
    install_requires=requirements,
)