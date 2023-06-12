from distutils.core import setup
# from setuptools import setup, find_packages

setup(name='TermProject',
      version='1.0',
      py_modules=['PythonFiles/main', 'PythonFiles/naverweather', 'PythonFiles/openmap',
                  'PythonFiles/option', 'PythonFiles/readparticulatesXML',
                  'PythonFiles/setup', 'PythonFiles/SpamTest', 'PythonFiles/telegrambot'],
      packages=['PythonFiles', 'PythonFiles/Resource', 'PythonFiles/Resource/FaceIcon', 'PythonFiles/Resource/WeatherIcon'],
      package_data={'': ['*.png']}
    )