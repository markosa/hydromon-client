from distutils.core import setup, Extension
 
module1 = Extension('HCSR04', sources = ['HCSR04.c'])
 
setup (name = 'HCSR04',
        version = '1.0',
        description = 'Simple module for reading HCSR04 sensor',
        ext_modules = [module1])
