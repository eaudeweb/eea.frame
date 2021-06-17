import os
from setuptools import setup

from frame import __version__ as VERSION

README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

setup(
    name='eea.frame',
    version=VERSION,
    description='Django integration middleware for EEA Zope websites',
    author='Diana Boiangiu',
    author_email='diana.boiangiu@eaudeweb.ro',
    url='https://github.com/eea/eea.frame',
    packages=[
        'frame',
        'frame.migrations',
    ],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Django>=2.2',
        'requests>=2.25.1',
    ],
    long_description=README,
)
