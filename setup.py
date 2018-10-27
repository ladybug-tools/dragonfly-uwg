import re
from setuptools import setup
import sys

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('dragonfly/__init__.py', 'r') as fd:
    version = re.search(
        r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
        fd.read(),
        re.MULTILINE
    ).group(1)

try:
    from semantic_release import setup_hook
    setup_hook(sys.argv)
except ImportError:
    pass

setup(
    name="antoine_dragonfly",
    version=version,
    author="ladybug-tools",
    description="Dragonfly is a utility API to work with UWG",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ladybug-tools/dragonfly",
    packages=['dragonfly'],
    include_package_data=True,
    dependency_links=[
        "https://github.com/ladybug-tools/uwg/archive/master.zip"
    ],
    entry_points='''
        [console_scripts]
        semantic-release=semantic_release.cli:main
    ''',
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "Operating System :: OS Independent",
    ],
)
