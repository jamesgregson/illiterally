from setuptools import setup, find_packages

setup(
    name='illiterally',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        'python-slugify', 'jinja2', 'emoji'
    ],
    extras_require={},
    entry_points={
        'console_scripts': [
            'illiterally=illiterally.cli:illiterally_cli',
            'illiterally_demo=illiterally.cli:illiterally_demo',
            'illiterally_dogfood=illiterally.cli:illiterally_dogfood'
        ]
    }   
)