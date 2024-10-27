import setuptools

setuptools.setup(
    name="fioer",
    version="0.0.1",
    author="xiong ke",
    author_email="unamed@enterprise.com",
    description="fio wrapper and postprocessing",
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires='>=3.8',
    install_requires=[
        "pydantic>=1.10.11",
        "numpy >= 1.24.1",
        "matplotlib >= 3.4.2",
        "pytest >=7.1.2"
  ],
    entry_points={
        'console_scripts': []
        }
)