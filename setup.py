try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
config = {
    'description': 'Python tweeter bot',
    'author': 'vly',
    'url': 'github.com/vly/py_tweetbot', 'download_url': 'git@github.com:vly/py_tweetbot.git',
        'author_email': 'val@plstr.com',
    'version': '0.1',
    'install_requires': ['nose'], 'packages': ['xlrd', 'socks', 'requests', 'sqlite3', 'oauth-hook'],
    'scripts': [],
    'name': 'py_tweetbot'
}