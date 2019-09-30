from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='fireo',
    version='0.0.1',
    description='FireStore ORM',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/octabytes/FireO.git",
    author="OctaByte",
    author_email="Dev@octabyte.io",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU General Public License v3.0",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers"
    ],
    py_modules=["helloworld"],
    package_dir={'': 'src'}
)