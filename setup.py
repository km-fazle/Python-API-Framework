from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="km-pyapi",
    version="0.1.0",
    author="KM Fazle Rabbi",
    author_email="contact@kmfazle.dev",
    description="A lightweight FastAPI-inspired REST API framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/km-fazle/Python-API-Framework",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Internet :: WWW/HTTP :: HTTP Servers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=[
        "fastapi>=0.115.0",
        "uvicorn[standard]>=0.32.0",
        "pydantic[email]>=2.7.0",
        "pydantic-settings>=2.0.0",
        "sqlalchemy>=2.0.25",
        "alembic>=1.13.1",
        "python-jose[cryptography]>=3.3.0",
        "passlib[bcrypt]>=1.7.4",
        "python-multipart>=0.0.6",
        "email-validator>=2.1.0",
        "httpx>=0.25.0",
    ],
    entry_points={
        'console_scripts': [
            'km-pyapi=py_api_framework.cli:main',
        ],
    },
    include_package_data=True,
    zip_safe=False,
) 