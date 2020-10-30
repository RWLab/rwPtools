from setuptools import setup

setup(
    name='rwptools',
    version='0.1',
    description="RobotWealth Python Tools",
    author="Robot Wealth",
    author_email="ajet@robotwealth.com",
    packages=['rwptools'],
    install_requires=[
          'gcloud>=0.18.3',
          'google-auth>=1.22.1',
          'google-cloud-storage>=1.32.0',
          'pandas>=1.0',
          'pyarrow'
          ]

)