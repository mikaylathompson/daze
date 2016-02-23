from setuptools import setup


setup(
        name='daze',
        version='0.1',
        py_modules=['daze', 'dazeutils'],
        install_requires=['click'],
        entry_points='''
            [console_scripts]
            daze=daze:cli
        ''',
)
