try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'My Project',
    'author': 'Saksham',
    'url': 'http://github.com/saksham/executely',
    'download_url': 'http://github.com/saksham/executely',
    'author_email': 'saksham@users.noreply.github.com',
    'version': '0.1',
    'install_requires': ['nose'],
    'packages': ['executely'],
    'scripts': [],
    'name': 'executely'
}

setup(**config)
