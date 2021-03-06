import io
from setuptools import setup, find_packages
from processing_protos import __version__

def read(file_path):
    with io.open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

readme = read('README.md')
requirements = read('requirements.txt')

setup(
    # metadata
    name='processing_protos',
    version=__version__,
    author='Andrey Grabovoy',
    description='Proto files for ProcessorProtos',
    long_description=readme,

    # options
    packages=find_packages(),
    install_requires='\n'.join([requirements]),
    include_package_data=True,
)