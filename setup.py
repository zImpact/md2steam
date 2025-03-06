from setuptools import setup, find_packages

setup(
    name="md2steam",
    version="1.0.1",
    author="Andrey Kataev",
    author_email="kata3v.andrey@yandex.ru",
    description="Markdown to Steam BBCode converter",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/zImpact/md2steam",
    packages=find_packages(),
    python_requires=">=3.10",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
