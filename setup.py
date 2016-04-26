from setuptools import setup, find_packages

setup(
        name="ternya",
        version="0.1.1",
        author="ndrlslz",
        author_email="ndrlslz@163.com",
        keywords="openstack notification",
        description="lightweight python library for openstack notification",
        url="https://github.com/ndrlslz/ternya",
        license="MIT",
        packages=['ternya'],
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Intended Audience :: Developers',
            'Topic :: Software Development :: Libraries :: Python Modules',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 3',
        ],
        install_requires=['kombu'],




)
