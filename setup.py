from setuptools import setup 

setup( 
	name='localEvaluation', 
	version='0.0.1', 
	description='Python package for local evaluation of Amplitude feature flags.', 
	author='Chandrajeet Nagar', 
	author_email='chandrajeetn@lambdatest.com', 
	packages=['localEvaluation'], 
	install_requires=[ 
		'dataclasses', 
		'os', 
        'amplitude_experiment'
	], 
) 
