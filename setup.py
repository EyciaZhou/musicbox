#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
__   ___________________________________________
| \  ||______   |   |______|_____||______|______
|  \_||______   |   |______|     |______||______
                                                
________     __________________________  _____ _     _
|  |  ||     ||______  |  |      |_____]|     | \___/ 
|  |  ||_____|______|__|__|_____ |_____]|_____|_/   \_


+ ------------------------------------------ +
|   NetEase-MusicBox               320kbps   |
+ ------------------------------------------ +
|                                            |
|   ++++++++++++++++++++++++++++++++++++++   | 
|   ++++++++++++++++++++++++++++++++++++++   |
|   ++++++++++++++++++++++++++++++++++++++   |
|   ++++++++++++++++++++++++++++++++++++++   |
|   ++++++++++++++++++++++++++++++++++++++   |
|                                            |
|   A sexy cli musicbox based on Python      |
|   Music resource from music.163.com        |
|                                            |
|   Built with love to music by omi          |
|                                            |
+ ------------------------------------------ +

'''

from setuptools import setup, find_packages


setup(
    name='NetEase-MusicBox',
    version='0.1.4',
    packages=find_packages(),

    include_package_data=True,

    install_requires=[
        'requests',
        'BeautifulSoup4',
    ],

    entry_points={
        'console_scripts': [
            'musicbox = src:start'
        ],
    },

    author='eycia',
    author_email='zhou.eycia@gmail.com',
    url='https://github.com/EyciaZhou/musicbox',
    description='A sexy command line interface musicbox',
    keywords=['music', 'netease', 'cli', 'player'],
    zip_safe=False,
)
