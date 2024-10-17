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
        #TODO: detailed dependencies 
        # "numpy >= 1.19.5",
        # "pandas",
  ],
    entry_points={
        'console_scripts': []
        }
)