import setuptools
from b4sh.settings import VERSION


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="b4sh",
    version=VERSION,
    scripts=['./scripts/b4sh'],
    author="Sanix-darker",
    author_email="s4nixd@gmail.com",
    description="Create, use and share bashs commands",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sanix-darker/b4sh",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
