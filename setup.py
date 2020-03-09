from setuptools import find_packages, setup

setup(
    name='bo',
    version='0.7.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
    ],
)
