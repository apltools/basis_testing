import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="basis_testing",
    version="0.0.5",
    author="Minor Programmeren",
    author_email="help@mprog.nl",
    description="A package to dynamically generate programming assignments based on templates.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/apltools/basis_testing",
    packages=setuptools.find_packages(),
    entry_points={
        "console_scripts": ["basis_testing=basis_testing.__main__:main"]
    },
    classifiers=[
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Topic :: Education",
        "Topic :: Utilities",
        "Development Status :: 1 - Planning"
    ],
    install_requires=[
        'xeger', 'basis @ https://api.github.com/repos/jelleas/basis/tarball',
    ],
    python_requires='>=3.6',
    include_package_data=True,
)
