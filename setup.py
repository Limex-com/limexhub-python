from setuptools import setup, find_packages
 
setup(
    name='limexhub',
    version='0.1.3',
    packages=find_packages(),
    include_package_data=True,
    description='A simple API wrapper for Limex DataHub',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/arbuzovv/limexhub-python',
    author='V.Arbuzov',
    author_email='varbuzov@limex.com',
    license='MIT',
    install_requires=[
        'requests',
    ],
    python_requires='>=3.6',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)