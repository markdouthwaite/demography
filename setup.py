from setuptools import setup
from setuptools import find_packages

from demography import __version__

long_description = """
This package implements a simple mechanism for quickly loading demographic data based
on post codes. This is currently only implemented for the UK.
"""

setup(
    name="demography",
    version=__version__,
    description="Demographic mapping based on UK ONS & census data.",
    long_description=long_description,
    author="Mark Douthwaite",
    author_email="mark@douthwaite.io",
    url="https://github.com/markdouthwaite/demography",
    license="MIT",
    extras_require={"tests": ["pytest", "markdown", "black"]},
    classifiers=[
        # 'Development Status :: 5 - Production/Stable',
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    packages=find_packages(),
)
