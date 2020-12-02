import setuptools


NAME = 'sars'
VERSION = '0.0.1'
DESCRIPTION = 'Modelling & analysis of SARS measures'
AUTHOR = 'greyhypotheses'
URL = 'https://github.com/plausibilities/sars'
PYTHON_REQUIRES = '=3.7.1'


with open('README.md') as f:
    readme_text = f.read()


setuptools.setup()(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=readme_text,
    author=AUTHOR,
    url=URL,
    python_requires=PYTHON_REQUIRES,
    license='',
    packages=setuptools.find_packages(exclude=['docs', 'tests'])
)
