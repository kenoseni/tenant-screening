from setuptools import setup, find_packages

setup(name='tenant_screening',
    version='0.1',
    description="A tenant screening tool to evaluate blacklist matches based on various criteria.",
    packages=find_packages(),
    install_requires=['pytest'],
    classifiers=[],
    python_requires='>=3.11',
    keywords='tenant screening, blacklist match, exclusion score',
)