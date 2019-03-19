# Upload package to PyPi.

from setuptools import setup

setup(name='tbapy',
      version='1.3.1',
      description='Library for interacting with The Blue Alliance API.',
      url='https://github.com/frc1418/tbapy',
      author='FRC Team 1418, Erik Boesen',
      author_email='robotics1418@gmail.com',
      license='MIT',
      packages=['tbapy'],
      install_requires=['requests'],
      zip_safe=False)
