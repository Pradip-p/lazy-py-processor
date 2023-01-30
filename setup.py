from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='lazy_crawler',
    version='0.1',
    description='Scrapy boiler plate for LazyScraping',
    url='git@github.com:Pradip-p/lazy-py-processor.git',
    author='Pradip Thapa',
    author_email='lazy_crawler@gmail.com',
    license='private',
    package_data={
        '': ['*.ini', '*.cfg'],
    },
    include_package_data=True,
    packages=find_packages(exclude=("deploy",)),
    install_requires=requirements,
    zip_safe=False
    )
