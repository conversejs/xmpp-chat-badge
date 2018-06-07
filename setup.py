#!/usr/bin/env python3
import os.path
import runpy

import setuptools
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

install_requires = [
    'flask~=0.12',
    'sleekxmpp~=1.3.1'
]

setup(
    name="xmpp-chat-badge",
    version="0.0.1",
    description="Renders a badge which shows the number of occupants in an XMPP chatroom",
    long_description=long_description,
    url="https://github.com/conversejs/xmpp-chat-badge",
    author="JC Brand",
    author_email="jc@opkode.com",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Operating System :: POSIX",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Topic :: Communications :: Chat",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: XMPP",
    ],
    keywords="xmpp http",
    install_requires=install_requires,
)
