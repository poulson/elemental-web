"""This script generates the reST input for the Python Programmer's
Reference from the DOLFIN Python module."""

__author__ = "Kristian B. Oelgaard <k.b.oelgaard@gmail.com>"
__date__ = "2010-09-15"
__copyright__ = "Copyright (C) 2010 " + __author__
__license__  = "GNU GPL version 3 or any later version"

# Last changed: 2010-10-08

import os, sys, types

# Set output directory
output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),\
                          os.pardir, "source", "doc/programmers-reference", "python")
#output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "python-source")


# Import the dolfin and dolfindocstrings modules.
try:
    import dolfin
    from dolfin_utils.documentation import indent
except Exception as what:
    raise ImportError("Could not import the dolfin module \n  (error: %s),\n\
  update your PYTHONPATH variable?" % what)

index_string = \
"""
%s:

.. toctree::
    :maxdepth: 1

%s
"""

def get_modules(mod, modules, top_module=""):
    """Extract all modules defined in a module.

    This function will not return external modules which are imported. To get
    all modules, the function is called recursively."""
    # This is the first call to the function, store name of module.
    if top_module == "":
        top_module = mod.__name__
    # Get all sub modules.
    for k, v in mod.__dict__.items():
        if not isinstance(v, types.ModuleType):
            continue
        n = v.__name__
        if n.split(".")[0] != top_module:
            continue
        # To avoid infinite recursion.
        if n in modules:
            continue
        modules[n] = v
        modules.update(get_modules(v, modules, top_module))
    return modules

def get_objects(module):
    "Extract classes and functions from a module."
    modules = []
    classes = []
    functions = []
#    print module.__name__
    for key, val in module.__dict__.items():
        if isinstance(val, (types.ClassType, types.TypeType)):
            if module.__name__ == val.__module__:
                classes.append(key)
        elif isinstance(val, types.FunctionType):
            if module.__name__ == val.__module__:
                functions.append(key)
        elif isinstance(val, types.ModuleType):
            if module.__name__.split(".") == val.__name__.split(".")[0:-1]:
                if key == "cpp":
                    key = "cpp (Swig autogenerated module) <cpp/index>"
                    modules.append(key)
                else:
                    modules.append(key + "/index")
        # Anything else we need to catch?
        else:
            pass

    return modules, classes, functions

def write_object(directory, module_name, name, obj_type):

    output = ".. Documentation for the %s %s\n\n" % (obj_type, module_name + "." + name)
    output += ".. _programmers_reference_python_%s:\n\n" % "_".join(module_name.split(".")[1:] + [name.lower()])
    output += name + "\n"
    output += "="*len(name) + "\n"
    output += "\n.. currentmodule:: %s\n\n" % module_name
    output += ".. auto%s:: %s\n" % (obj_type, name)
    outfile = os.path.join(directory, name + ".rst")
    f = open(outfile, "w")
    f.write(output)
    f.close()

def write_documentation(module):
    mod_name = module.__name__
    dirs = [output_dir]
    dirs += mod_name.split(".")[1:]
    directory = os.path.sep.join(dirs)

    try:
        os.makedirs(directory)
    except:
        pass

    modules, classes, functions = get_objects(module)

    output = ".. Index file for the %s module.\n\n" % mod_name
    output += ".. _programmers_reference_python_%s:\n\n" % "_".join(mod_name.split(".")[1:] + ["index"])
    if mod_name == "dolfin":
        output += """#############################
Python programmer's reference
#############################\n"""
    else:
        header = "%s module" % mod_name
        stars = "*"*len(header)
        output += stars + "\n"
        output += header + "\n"
        output += stars + "\n"

    outfile = os.path.join(directory, "index.rst")
    f = open(outfile, "w")
    f.write(output)
    if modules:
        f.write(index_string % ("Modules", indent("\n".join(sorted(modules)), 4)))
    if classes:
        f.write(index_string % ("Classes", indent("\n".join(sorted(classes)), 4)))
    if functions:
        f.write(index_string % ("Functions", indent("\n".join(sorted(functions)), 4)))
    f.close()

    for o in classes:
#        if not o == "Mesh":
#            continue
        write_object(directory, mod_name, o, "class")

    for o in functions:
        write_object(directory, mod_name, o, "function")

modules = get_modules(dolfin, {})
#write_module_index(modules)
for key, mod in modules.items():
    print "Writing files for module: ", key
#    if not key == "dolfin.mesh.refine":
#        continue
    write_documentation(mod)
