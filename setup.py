import re
import setuptools
import sys

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('dragonfly/__init__.py', 'r') as fd:
    version = re.search(
        r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
        fd.read(),
        re.MULTILINE
    ).group(1)

with open('requirements.txt') as f:
    requirements = f.read().splitlines()
try:
    from semantic_release import setup_hook
    setup_hook(sys.argv)
except ImportError:
    pass

setuptools.setup(
    name="lbt-dragonfly",
    version=version,
    author="ladybug-tools",
    description="Dragonfly is a python library for urban climate + urban energy modeling.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ladybug-tools/dragonfly",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.6",
        "Operating System :: OS Independent",
    ],
)
