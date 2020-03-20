import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="yorkpy",
    version="0.0.10",
    author="Tinniam V Ganesh",
    author_email="tvganesh.85@gmail.com",
    description="Analyze T20 matches based on data from Cricsheet-http://cricsheet.org",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tvganesh/yorkpy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
