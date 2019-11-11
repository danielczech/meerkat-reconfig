from setuptools import setup

setup(
    name = 'meerkat-reconfig',
    version = '0.1',
    author_email = 'daniel.czech@protonmail.com',
    packages = ['meerkat-reconfig'],
    entry_points = {
        'console_scripts': ['meerkat-reconfig = meerkat-reconfig.cli:cli']},
    install_requires = [
                       #'numpy == 1.14.1',
                       #'redis == 2.10.6'
                       ],
) 
