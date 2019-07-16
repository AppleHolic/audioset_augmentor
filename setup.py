from typing import List
from setuptools import setup, find_packages
import os


README_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'README.md')


with open(README_PATH, 'r', encoding='utf-8') as r:
    long_description = r.read()


def get_requirements(filename: str = 'requirements.txt') -> List[str]:
    deps = []
    with open(filename, 'r') as f:
        for pkg in f.readlines():
            if pkg.strip():
                deps.append(pkg)
    return deps


setup(
    name='audioset_augmentor',
    version='0.0.1',
    description='',
    author='ILJI CHOI',
    author_email='choiilji@gmail.com',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords='audioset,sound,fl',
    packages=find_packages(),
    install_requires=get_requirements(),
    python_requires='>=3'
)
