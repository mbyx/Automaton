import requests
import setuptools

PROJECT_REPOSITORY: str = "https://github.com/Abdul-Muiz-Iqbal/Automaton"

PROJECT_VERSION: str = requests.get(f"{PROJECT_REPOSITORY}/releases/latest").url.split(
    "/"
)[-1]

with open("README.md", "r") as f:
    PROJECT_DESCRIPTION: str = f.read()

setuptools.setup(
    name="automaton-linux",
    packages=setuptools.find_packages(),
    version=PROJECT_VERSION,
    license="MIT",
    description="An automation library for linux.",
    long_description=PROJECT_DESCRIPTION,
    long_description_content_type="text/markdown",
    author="Abdul Muiz Iqbal",
    author_email="parkermuiz0@gmail.com",
    url="https://github.com/Abdul-Muiz-Iqbal/Automaton/",
    download_url=f"{PROJECT_REPOSITORY}/archive/refs/tags/{PROJECT_VERSION}.tar.gz",
    keywords=["automation", "linux", "uinput"],
    install_requires=["evdev", "multiprocess"],
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
    ],
)
