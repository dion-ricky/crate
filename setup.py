from distutils.core import setup
import io
import os

VERSION = '0.1.3'

setup(
    name="crate",
    packages=["crate"],
    version=VERSION,
    license="MIT",
    description="Twitter scraper",
    author="Dion Ricky Saputra",
    author_email="code@dionricky.com",
    url="https://github.com/dion-ricky/crate",
    download_url="https://github.com/dion-ricky/crate/archive/refs/tags/v0.1.2.tar.gz",
    keywords=["twitter", "scraper", "crawl", "scrape", "tweet"],
    install_requires=[
        "async-generator==1.10",
        "attrs==21.4.0",
        "certifi==2021.10.8",
        "cffi==1.15.0",
        "chromedriver-autoinstaller==0.3.1",
        "cryptography==36.0.1",
        "h11==0.12.0",
        "idna==3.3",
        "outcome==1.1.0",
        "pycparser==2.21",
        "pyOpenSSL==21.0.0",
        "selenium==3.14.1",
        "six==1.16.0",
        "sniffio==1.2.0",
        "sortedcontainers==2.4.0",
        "trio==0.19.0",
        "trio-websocket==0.9.2",
        "urllib3==1.26.7",
        "wsproto==1.0.0"
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ]
)