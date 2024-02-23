from setuptools import setup, find_packages

# https://stackoverflow.com/questions/6323860/sibling-package-imports/50193944#50193944

# Para trasnformar seu projeto em um pacote do pip:

# pip install -e .

setup(name="myproject", version="1.0", packages=find_packages())