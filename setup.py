import setuptools
import versioneer


with open('README.rst') as f:
    readme = f.read()


setuptools.setup(
    name='exttr',
    author='Kyle Altendorf',
    description='Integrating extra metadata into attr.ib()',
    long_description=readme,
    long_description_content_type='text/x-rst',
    url='https://github.com/altendky/exttr',
    packages=setuptools.find_packages('src'),
    package_dir={'': 'src'},
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    license='MIT',
    classifiers=[
        # complete classifier list:
        #   https://pypi.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    install_requires=[
        'attrs',
    ],
    extras_require={
        'dev': [
            'coverage',
            'gitignoreio',
            'pytest',
            'pytest-cov',
            'tox',
        ],
    },
)
