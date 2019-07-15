#!/usr/bin/env python

from os.path import isfile

from setuptools import setup


def _read_file(path):
    with open(path) as fp:
        return fp.read().strip()


PROJECT_VERSION = _read_file("VERSION.txt")

REQUIREMENTS = _read_file("requirements.txt").split("\n")
DEV_REQUIREMENTS = _read_file("requirements_dev.txt").split("\n")


if isfile("README.md"):
    long_description = _read_file("README.md")
else:
    long_description = ""

setup(
    name="html-to-draftjs",
    author="NyanKiyoshi",
    author_email="hello@vanille.bid",
    url="https://github.com/NyanKiyoshi/html-to-draftjs/",
    description="Convert basic HTML into DraftJS JSON format.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    version=PROJECT_VERSION,
    packages=["html_to_draftjs"],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    install_requires=REQUIREMENTS,
    extras_require={"dev": DEV_REQUIREMENTS},
    zip_safe=False,
)
