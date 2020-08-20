from setuptools import setup, find_packages


setup(
    name='aioapple',
    version='0.2',
    description='Asyncio-based client for Apple Service',
    author='Rocky Feng',
    author_email='folowing@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['aiohttp>=3.6.2', 'PyJWT'],
    zip_safe=False,
)
