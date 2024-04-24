from setuptools import find_packages, setup

HYPHEN_E_DOT = '-e .'
def get_requirements(file_path):
    """
    Returns a list of requirements
    """
    requirements = list()
    with open(file_path) as f:
        requirements = f.readlines()
        requirements = [req.replace('\n', '') for req in requirements]
        
        if HYPHEN_E_DOT in requirements:
            requirements.remove(HYPHEN_E_DOT)

    return requirements

setup(
    name='solar_scan',
    version='0.0.1',
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt')
)