#!/usr/bin/env python
"""
Created on 2015-03-05
@author: j.hachmann
"""

# TODO: adapt from PyQuante

from setuptools import setup, find_packages

setup(name='GradeMasterMohammadShakia',
      version='0.1.17',
      author='Johannes Hachmann, Mohammad Shakiba',
      author_email='hachmann@buffalo.edu',
      url='http://hachmannlab.cbe.buffalo.edu',
#       download_url='http://www.my_program.org/files/',
      description='GradeMaster for computing the grading for students using their grades in the semester',
      long_description='GradeMaster for computing the grading for students using their grades in the semester',

      packages = find_packages(),
      include_package_data = True,
      #package_data = {
      #  '': ['*.txt', '*.rst'],
      #  'CheML': ['data/*.html', 'data/*.css'],
      #},
      #exclude_package_data = { '': ['README'] },
      
      #scripts = ['bin/cheml'],
      
      #keywords='python tools utils internet www',
      license='BSD',
      #classifiers=['Development Status :: 1 - Development',
      #             'Natural Language :: English',
      #             'Operating System :: OS Independent',
      #             'Programming Language :: Python :: 2',
      #             'License :: OSI Approved :: BSD License',
      #             'Topic :: Internet',
      #             'Topic :: Internet :: WWW/HTTP',
      #            ],
                  
      #setup_requires = ['python-stdeb', 'fakeroot', 'python-all'],
      install_requires = ['setuptools'],
     )
