from setuptools import setup, find_packages

setup(
    name='lit',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        'python-slugify', 'jinja2', 'emoji'
    ],
    extras_require={},
    entry_points={
        'console_scripts': [
            'lit=lit.cli:lit_cli',
            'lit_demo=lit.cli:lit_demo'
        ]
    }   
)