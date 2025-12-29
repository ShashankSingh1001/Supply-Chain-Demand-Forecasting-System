"""
Setup configuration for Supply Chain Optimization project
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_file = Path(__file__).parent / "README.md"
long_description = ""
if readme_file.exists():
    with open(readme_file, "r", encoding="utf-8") as f:
        long_description = f.read()

# Read requirements
requirements_file = Path(__file__).parent / "requirements.txt"
requirements = []
if requirements_file.exists():
    with open(requirements_file, "r", encoding="utf-8") as f:
        requirements = [
            line.strip() 
            for line in f 
            if line.strip() and not line.startswith("#")
        ]

setup(
    name="supply-chain-optimization",
    version="0.1.0",
    author="Shashank Singh",
    author_email="shashanksinghofficial101@gmail.com",
    description="ML-powered supply chain demand forecasting and inventory optimization",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ShashankSingh1001/Supply-Chain-Demand-Forecasting-System",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "black>=23.12.1",
            "flake8>=6.1.0",
            "isort>=5.13.2",
            "mypy>=1.7.1",
            "pytest>=7.4.3",
            "pytest-cov>=4.1.0",
        ],
        "notebooks": [
            "jupyter>=1.0.0",
            "notebook>=7.0.6",
            "ipykernel>=6.27.1",
        ],
    },
    entry_points={
        "console_scripts": [
            "supply-chain=main:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)