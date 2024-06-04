from setuptools import setup, find_packages

setup(
    name='myline',
    version='0.1.1',
    packages=find_packages(),
    install_requires=[
        'line-bot-sdk',
        'flask',
    ],
    url='https://github.com/lupin-oomura/myline.git',
    author='Shin Oomura',
    author_email='shin.oomura@gmail.com',
    description='A simple Line Messaging API functions',
)
