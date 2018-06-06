import codecs
import os
from setuptools import setup, find_packages


HERE = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    with codecs.open(os.path.join(HERE, *parts), "rb", "utf-8") as f:
        return f.read()


def get_base_requirements():
    return read("requirements/base.txt").split("\n")


def get_prod_requirements():
    requires = get_base_requirements() + read("requirements/production.txt").split("\n")
    requires = [req for req in requires if req not in ["", "-r base.txt"]]
    return requires


def get_test_requirements():
    requires = get_base_requirements() + read("requirements/dev.txt").split("\n")
    requires = [req for req in requires if req not in ["", "-r base.txt"]]
    return requires


setup(
    name="lebombo",
    version="0.0.1",
    description="Additional functionality for RapidPro",
    long_description=read("readme.md"),
    long_description_content_type="text/markdown",
    keywords="rapidpro webhook randomization surveys",
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
    ],
    author="Praekelt.org",
    author_email="dev@praekelt.org",
    url="http://github.com/praekeltfoundation/lebombo",
    license="BSD",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=get_prod_requirements(),
    tests_require=get_test_requirements(),
    entry_points={},
)
