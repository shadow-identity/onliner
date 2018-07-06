from setuptools import setup

setup(
    name='onliner_notify',
    version='1.1',
    packages=['onliner_notify'],
    url='https://github.com/shadow-identity/onliner',
    license='MIT',
    author='Pavel Nedrigailov',
    author_email='pavel.nedr@gmail.com',
    description='Notify about new royal estate advertisement on Onliner.by',
    zip_safe=False, install_requires=['tinydb']
)
