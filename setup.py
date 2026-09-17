from setuptools import setup

APP = ['main.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
    'plist': {
        'LSUIElement': True,
    },
    'packages': ['rumps'],
}

setup(
    app=APP,
    name="PoMo",
    data_files=DATA_FILES,
    options={'py2app': OPTIONS, 'plist': {
        'CFBundleName': "PoMo",
        'CFBundleDisplayName': "PoMo",
    }},
    setup_requires=['py2app'],
)