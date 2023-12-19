from setuptools import setup, find_packages

setup(
    name='web-rover-kayarn',
    version='0.1.0',  # Replace with your desired version
    description='A Python Package to Scrap Web Assets',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    url='https://github.com/agent87/WebRover',  # Update with your repository URL
    author='Arnaud Kayonga',
    author_email='arnauldkayonga1@gmail.com',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    package_data={'': ['requirements.txt']}, 
    python_requires=">=3.7",
    include_package_data=True,
    install_requires=[
        "requests",
        "validators",
        "bs4"
    ],
    extras_require={
        "dev": ["pytest>=7.0", "twine>=4.0.2"],
    },
    entry_points='''
        [console_scripts]
        webrover=rover
    ''',
    zip_safe=False
)
