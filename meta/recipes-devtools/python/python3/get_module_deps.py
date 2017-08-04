# This script is launched on separate task for each python module
# It checks for dependencies for that specific module and prints 
# them out, the output of this execution will have all dependencies
# for a specific module, which will be parsed an dealt on create_manifest.py


# We can get a log per module, for all the dependencies that were found, but its messy.
debug=False

import sys

# We can get a list of the modules which are currently required to run python
# so we run python-core and get its modules, we then import what we need
# and check what modules are currently running, if we substract them from the
# modules we had initially, we get the dependencies for the module we imported.

core_deps=set(sys.modules)

# We use importlib to achieve this, so we also need to know what modules importlib needs
import importlib
importlib_deps=set(sys.modules)


def fix_path(dep_path):
    import os
    # We DONT want the path on our HOST system
    pivot='recipe-sysroot-native'
    dep_path=dep_path[dep_path.find(pivot)+len(pivot):]

    if '/usr/bin' in dep_path:
        dep_path = dep_path.replace('/usr/bin''${bindir}')

    # Handle multilib, is there a better way?
    if '/usr/lib32' in dep_path:
        dep_path = dep_path.replace('/usr/lib32','${libdir}')
    if '/usr/lib64' in dep_path:
        dep_path = dep_path.replace('/usr/lib64','${libdir}')
    if '/usr/lib' in dep_path:
        dep_path = dep_path.replace('/usr/lib','${libdir}')
    if '/usr/include' in dep_path:
        dep_path = dep_path.replace('/usr/include','${includedir}')
    if '__init__.' in dep_path:
        dep_path =  os.path.split(dep_path)[0]
    return dep_path


# Module to import was passed as an argument
current_module =  str(sys.argv[1]).rstrip()
if(debug==True):
    log = open('log_%s' % current_module,'w')
    log.write("Module %s generated the following dependencies:\n" % current_module)
try: 
    importlib.import_module('%s' % current_module)
except ImportError as e:
    if (debug==True):
        log.write("Module was not found")
    pass


# Get current module dependencies, dif will contain a list of specific deps for this module
module_deps=set(sys.modules)

# We handle the core package (1st pass on create_manifest.py) as a special case
if current_module == 'python-core-package':
    dif = core_deps
else:
    dif = module_deps-core_deps
    # We know this is not the core package, so there must be a difference,
    # What happens here is that importlib likely depends on the module we are
    # currently checking

# Check where each dependency came from
for item in dif:
    dep_path=""
    try:
        if (debug==True):
            log.write("Calling: sys.modules[" + "%s" % item + "].__file__\n")
        dep_path = sys.modules['%s' % item].__file__
    except AttributeError as e:
        # Deals with thread (builtin module) not having __file__ attribute
        if debug==True:
            log.write(item + ' ')
            log.write(str(e))
            log.write("\n")
        pass
    except NameError as e:
        # Deals with NameError: name 'dep_path' is not defined
        # because module is not found (wasn't compiled?), e.g. bddsm
        if (debug==True):
            log.write(item+' ') 
            log.write(str(e))                                              
        pass

    # Site-customize is a special case since we (OpenEmbedded) put it there manually
    if 'sitecustomize' in dep_path:
        dep_path = '${libdir}/python2.7/sitecustomize.py'
        # Prints out result, which is what will be used by create_manifest
        print (dep_path)
        continue

    dep_path = fix_path(dep_path)

    import sysconfig
    soabi=sysconfig.get_config_var('SOABI')
    # Check if its a shared library and deconstruct it
    if soabi in dep_path:
        if (debug==True):
            log.write("Shared library found in %s" % dep_path)
        dep_path = dep_path.replace(soabi,'*')
        print (dep_path)
        continue

    if (debug==True):
        log.write(dep_path+"\n")
    # Prints out result, which is what will be used by create_manifest
    print (dep_path)


    import imp
    cpython_tag = imp.get_tag() 
    cached=""
    # Theres no naive way to find *.pyc files on python3
    try:
        if (debug==True):
            log.write("Calling: sys.modules[" + "%s" % item + "].__cached__\n")
        cached = sys.modules['%s' % item].__cached__
    except AttributeError as e:
        # Deals with thread (builtin module) not having __cached__ attribute
        if debug==True:
            log.write(item + ' ')
            log.write(str(e))
            log.write("\n")
        pass
    except NameError as e:
        # Deals with NameError: name 'cached' is not defined
        if (debug==True):
            log.write(item+' ') 
            log.write(str(e))                                              
        pass
    if cached is not None:
        if (debug==True):
            log.write(cached)
        cached = fix_path(cached)
        cached = cached.replace(cpython_tag,'*')
        print (cached)

if debug==True:
    log.close()
