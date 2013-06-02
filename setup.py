from distutils.core import setup

setup(
    name='textbites',
    version='0.2.0',
    author='John Lehmann',
    author_email='john.lehmann@gmail.com',
    packages=['textbites', 'textbites.bible'],
    package_data={'textbites': ['data/*']},
    scripts=[],
    url='',
    license='LICENSE.txt',
    description='Code and data for the textbites.',
    long_description=open('README.md').read(),
    install_requires=[
    ],
)
