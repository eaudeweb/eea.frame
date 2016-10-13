import os
from setuptools import setup

from frame import __version__ as VERSION

README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

setup(
    name='eea.frame',
    version=VERSION,
    packages=[
        'frame',
        'frame.migrations',
    ],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Django>=1.9',
        'requests>=2.2',
    ],
    description='Django integration middleware for EEA Zope websites',
    long_description=README,
)
