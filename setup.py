from setuptools import setup, find_packages
 
setup(
    name='maas-cli',
    version='0.3.0',
    packages=find_packages(),
    install_requires=[
        'click>=8.0',
        'boto3>=1.26'
    ],
    entry_points={
        'console_scripts': [
            'maas=maas.cli:maas',
        ],
    },
    author='CEP',
    description='CLI Maas to trigger Stepfunction on AWS',
)
