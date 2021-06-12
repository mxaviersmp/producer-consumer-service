from setuptools import find_packages, setup

with open('requirements.txt') as f:
    DEPENDENCIES = [dep.strip() for dep in f.readlines()]

LICENSE = 'MIT License'

CLASSIFIERS = [
    'Development Status :: 1 - Planning',
    'Programming Language :: Python :: 3',
    'Operating System :: OS Independent',
]
if LICENSE:
    CLASSIFIERS.append(f'License :: OSI Approved :: {LICENSE}')

print(DEPENDENCIES)

setup(
    name='app',
    version='0.0.1',
    author='Matheus Xavier',
    author_email='matheus.sampaio011@gmail.com',
    license=LICENSE,
    python_requires='>=3.7',
    description='A Producer and a Consumer service that will \
        be connected through a Queue',
    long_description_content_type='text/markdown',
    url='consumer-producer-service',
    packages=find_packages(),
    classifiers=CLASSIFIERS,
    install_requires=DEPENDENCIES,
    include_package_data=True
)
