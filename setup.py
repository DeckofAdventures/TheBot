from setuptools import setup, find_packages
from os import path

pkg_name = 'the_bot'
here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), 'r') as f:
    long_description = f.read()

with open(path.join(here, 'requirements.txt')) as f:
    requirements = f.read().splitlines()

with open(path.join(here, pkg_name, 'version.py')) as f:
    exec(f.read())

setup(
    name='TheBot',
    version=__version__,
    description="Deck of Adventures Discord Bot for posting GitHub issues",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='CBroz1',
    author_email='broz@deckofadventures.com',
    license='MIT',
    url='https://github.com/DeckofAdventures/TheBot',
    keywords='TTRPG Discord GitHub',
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    scripts=[],
    install_requires=requirements,
)
