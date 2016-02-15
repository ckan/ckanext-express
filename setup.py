from setuptools import setup, find_packages
import sys, os

version = '0.0'

setup(
    name='ckanext-express',
    version=version,
    description="",
    long_description='''
    ''',
    classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords='',
    author='',
    author_email='',
    url='',
    license='',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    namespace_packages=['ckanext', 'ckanext.express'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        # -*- Extra requirements: -*-
    ],
    entry_points='''
        [ckan.plugins]
        # Add plugins here, e.g.
        up_to_n_editors=ckanext.express.plugin:UpToNEditorsPlugin
        customizable_featured_image=ckanext.express.customizable_featured_image:CustomizableFeaturedImagePlugin
        express=ckanext.express.plugin:ExpressPlugin

    ''',
)
