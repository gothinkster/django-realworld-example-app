import os

from setuptools import find_packages, setup

CWD = os.path.dirname(__file__)  # FIXME __file__ is not freeze-proof

with open(os.path.join(CWD, 'README.md')) as readme:
    README = readme.read()

with open(os.path.join(CWD, 'requirements.txt')) as f:
    install_reqs = [
        s for s in [
            line.strip(' \n') for line in f
        ] if not s.startswith('#') and s != ''
    ]

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='conduit',  # FYI this clashes with an existing package on PYPI!
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    license='BSD License',  # example license
    description='Example Django DRF codebase containing real world examples (CRUD, auth, advanced patterns, etc) that adheres to the RealWorld API spec.',
    long_description=README,
    url='https://github.com/gothinkster/realworld-example-apps',
    author='Your Name',
    author_email='yourname@example.com',
    install_requires=install_reqs,
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.11',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
