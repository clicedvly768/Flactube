from setuptools import setup

APP = ['Downloads.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
    'iconfile': 'TItYs46QPidtB3bHWybVd7ZpdNhlAcy9.icns',
    'plist': {
        'CFBundleName': "FlacTube",
        'CFBundleShortVersionString': "2.0",
    }
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)