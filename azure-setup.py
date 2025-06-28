from setuptools import setup, find_packages

setup(
    name='maas-cli-azure',
    version='0.3.0',
    py_modules=['azure_cli'],  # single-file CLI
    install_requires=[
        'click>=8.0',
        'azure-identity>=1.15',
        'requests>=2.28'
    ],
    entry_points={
        'console_scripts': [
            'maas=azure_cli:maas',  # maps `maas` command to `azure_cli.py`'s `maas()` group
        ],
    },
    author='CEP',
    description='CLI Maas to trigger Logic Apps on Azure',
)