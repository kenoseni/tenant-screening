from setuptools import setup, find_packages

setup(
    name="tenant_screening",
    version="0.1",
    description="A tenant screening tool to evaluate blacklist matches based on various criteria.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Olusola Oseni",
    author_email="kenolusola@gmail.com",
    url="https://github.com/kenoseni/tenant-screening",
    packages=find_packages(),
    py_modules=["main"],
    install_requires=[
        "pytest",
        "pytest-cov",
        "requests",
        "ollama",
        "python-dotenv",
        "pytest-mock",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires=">=3.11",
    keywords="prospective tenant screening, blacklist match, classification",
    entry_points={
        "console_scripts": [
            "tenant-screening=main:main",
        ],
    },
)
