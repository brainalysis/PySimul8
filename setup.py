import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PySimul8",
    version="0.0.1",
    author="Fahad Akbar, Abhimanyu Anand, Suman K Batra",
    author_email="abhimanyu7296@gmail.com",
    description="A simulation package for cash flows",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/brainalysis/PySimul8",
    packages=setuptools.find_packages(),
    install_requires = ['numpy', 'pandas','pandasql','plotly','numpy_financial'],
    extras_require= {"dev" : ["pytest>=3.7",],},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
