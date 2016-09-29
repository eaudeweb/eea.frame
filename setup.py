from setuptools import setup
from frame import __version__ as VERSION


setup(
    name='eea.frame',
    version=VERSION,
    description='EEA Frame',
    packages=['frame'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Django>=1.6',
        'requests>=2.2',
    ],
)
