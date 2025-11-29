"""
GenAI Platform - Enterprise AI Orchestration System
Setup configuration
"""

from setuptools import setup, find_packages
import os

# Read README for long description
def read_file(filename):
    with open(os.path.join(os.path.dirname(__file__), filename), encoding='utf-8') as f:
        return f.read()

# Read requirements
def read_requirements():
    with open('requirements.txt', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name='genai_platform',
    version='1.0.0',
    description='Enterprise-grade GenAI platform with multi-division architecture, knowledge graph, and comprehensive connectors',
    long_description=read_file('README.md') if os.path.exists('README.md') else '',
    long_description_content_type='text/markdown',
    author='GenAI Platform Team',
    author_email='platform@genai.example.com',
    url='https://github.com/example/genai_platform',
    
    packages=find_packages(exclude=['tests', 'docs', 'scripts']),
    
    install_requires=read_requirements(),
    
    python_requires='>=3.10',
    
    entry_points={
        'console_scripts': [
            'genai-platform=gui.main_window:main',
            'genai-cli=backend.cli:main',
            'genai-server=backend.api.server:main',
        ],
    },
    
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Enterprise',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Operating System :: OS Independent',
    ],
    
    include_package_data=True,
    
    package_data={
        'genai_platform': [
            'config/*.yaml',
            'data/*/*.csv',
            'data/*/*.xlsx',
            'data/*/*.json',
            'data/*/*.pdf',
        ],
    },
    
    extras_require={
        'dev': [
            'pytest>=7.4.4',
            'pytest-cov>=4.1.0',
            'black>=24.1.0',
            'flake8>=7.0.0',
            'mypy>=1.8.0',
        ],
        'neo4j': [
            'neo4j>=5.15.0',
        ],
        'hive': [
            'pyhive>=0.7.0',
            'thrift>=0.16.0',
        ],
    },
)
