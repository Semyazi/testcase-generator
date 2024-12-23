from setuptools import setup,find_packages
setup(
    name='tcg',
    packages=find_packages(),
    entry_points={
        'console_scripts':['tcg=tcg.command_line:cli']
    }
)