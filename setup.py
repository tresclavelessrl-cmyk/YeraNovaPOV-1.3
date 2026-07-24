from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="YeraPOV",
    version="1.0.0",
    author="Tres Claveles S.R.L.",
    description="Sistema POS e Inventario multiplataforma (Windows/Android)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tresclavelessrl-cmyk/YeraPOV",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: Boost Software License 1.0",
        "Operating System :: OS Independent",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: Android",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Office/Business :: Financial :: Point-Of-Sale",
    ],
    python_requires=">=3.10",
    install_requires=[
        "PySide6>=6.7.0",
        "SQLAlchemy>=2.0.23",
        "openpyxl>=3.1.2",
        "reportlab>=4.0.7",
        "python-barcode>=0.15.1",
        "pyzbar>=0.1.9",
        "requests>=2.31.0",
        "bcrypt>=4.1.1",
        "PyJWT>=2.8.1",
        "cryptography>=41.0.7",
        "loguru>=0.7.2",
        "colorama>=0.4.6",
    ],
    extras_require={
        "android": [
            "Kivy>=2.2.1",
            "KivyMD>=1.2.0",
            "pyjnius>=1.5.0",
            "plyer>=2.1.0",
        ],
        "dev": [
            "pytest>=7.4.3",
            "pytest-cov>=4.1.0",
            "mypy>=1.7.1",
            "black>=23.12.0",
            "flake8>=6.1.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "yerapov=main:main",
        ],
    },
)
