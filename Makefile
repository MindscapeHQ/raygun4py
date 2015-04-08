bootstrap:
	pip install nose
	pip install jsonpickle

tests: bootstrap
	PYV=$(shell python -c "import sys;t='{v[0]}.{v[1]}'.format(v=list(sys.version_info[:2]));sys.stdout.write(t)");
	ifeq ($(PYV), 2)
		cd python2
	else
		cd python3
	endif
	nosetests