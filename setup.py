#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

import os
import re
import sys
import uuid
from glob import glob
from os.path import basename, splitext

try:  # for pip >= 10
    # noinspection PyProtectedMember,PyPackageRequirements
    from pip._internal.req import parse_requirements
except ImportError:  # for pip <= 9.0.3
    # noinspection PyPackageRequirements
    from pip.req import parse_requirements

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup


def requirements(path):
    items = parse_requirements(path, session=uuid.uuid1())
    items = [";".join((str(r.req), str(r.markers))) if r.markers else str(r.req) for r in items]
    import pprint
    pprint.pprint(items)
    return items


tests_require = requirements(os.path.join(os.path.dirname(__file__), "requirements.txt"))
install_requires = requirements(os.path.join(os.path.dirname(__file__), "requirements.txt"))


def get_version(*file_paths):
    """Retrieves the version from path"""
    filename = os.path.join(os.path.dirname(__file__), *file_paths)
    print("Looking for version in: {}".format(filename))
    version_file = open(filename).read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError('Unable to find version string.')


version = get_version("src", "secure_share_kiss", "__init__.py")

setup(
    name='secure-share',
    version=version,
    description="""A test project for job application""",
    long_description="""tob""",
    author="Janusz Skonieczny",
    author_email='js+pypi@bravelabs.pl',
    url='https://github.com/wooyek/secure_share_kisss',
    packages=find_packages('src', exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    entry_points={
        'console_scripts': [
            'secure_share=secure_share.cli:main'
        ]
    },
    include_package_data=True,
    exclude_package_data={
        '': ['test*.py', 'tests/*.env', '**/tests.py'],
    },
    python_requires='>=3.6',
    install_requires=install_requires,
    license="MIT license",
    zip_safe=False,
    keywords='secure-share',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        # 'Framework :: Django :: 1.10',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    tests_require=tests_require,
    # https://docs.pytest.org/en/latest/goodpractices.html#integrating-with-setuptools-python-setup-py-test-pytest-runner
    setup_requires=['pytest-runner'],
)
