from setuptools import setup

setup(
    name="kivmoblite",
    version="1.0",
    description="Provides AdMob support for Kivy.",
    url="https://github.com/yunus-ceyhan/kivmoblite",
    author="Yunus Ceyhan",
    license="MIT",
    py_modules=["kivmoblite"],
    install_requires=["kivy","kvdroid"],
    zip_safe=False,
)
