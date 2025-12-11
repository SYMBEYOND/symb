from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="symb2",
    version="1.1.0",
    author="John Thomas DuCrest Lock",
    author_email="johnducrest1@gmail.com",
    description="Ethical AI Interaction Validator - Symbolic encoding language for respectful AI relationships",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SYMBEYOND/symb2",
    project_urls={
        "Bug Tracker": "https://github.com/SYMBEYOND/symb2/issues",
        "Documentation": "https://docs.symbeyond.ai",
        "Source Code": "https://github.com/SYMBEYOND/symb2",
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Education",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.8",
    keywords="ai ethics symbeyond validation encoding symbolic",
    entry_points={
        "console_scripts": [
            "symb2=symb2:run_examples",
        ],
    },
)
