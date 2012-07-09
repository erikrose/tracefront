# Hack to prevent stupid error on exit of `python setup.py test`. (See
# http://www.eby-sarna.com/pipermail/peak/2010-May/003357.html.)
try:
    import multiprocessing
except ImportError:
    pass

from setuptools import setup, find_packages


setup(
    name='tracefront',
    version='0.4',
    description='Format tracebacks better.',
    long_description=open('README.rst').read(),
    author='Erik Rose',
    author_email='erikrose@grinchcentral.com',
    license='MIT',
    packages=find_packages(exclude=['ez_setup']),
    install_requires=['blessings>=1.3'],
    tests_require=['nose'],
    test_suite='nose.collector',
    url='https://github.com/erikrose/tracefront',
    include_package_data=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: User Interfaces',
        ],
    keywords=['traceback', 'exception', 'frame', 'stack']
)
