from distutils.core import setup

setup(
    name='pybooks',
    version='0.1.0',
    author='John Lehmann',
    author_email='john.lehmann@gmail.com',
    packages=['pybooks'],
    #package_data={'pybible': ['data/*']},
    scripts=[],
    url='',
    license='LICENSE.txt',
    description='Code and data for the pybooks.',
    long_description=open('README.md').read(),
    install_requires=[
    ],
)
