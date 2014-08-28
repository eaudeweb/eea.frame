from setuptools import setup


setup(
    name='eea.frame',
    version='0.2',
    description='EEA Frame',
    packages=['frame'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Django==1.6.3',
        'requests==2.2.1',
    ],
)
