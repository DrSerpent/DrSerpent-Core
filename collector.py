import os, sys, importlib

def get_tests(top, directory_naming_convention):
    directory_dictionaries = []
    for (dirpath, dirnames, filenames) in os.walk(top):
        if dirpath.rpartition('/')[-1] == directory_naming_convention:
            test_modules = []
            for filename in filenames:
                if filename[0:5] == "test_" and filename[-3:] == ".py":
                    test_modules.append(filename[0:-3])
            directory_dictionaries.append({"directory":dirpath, "modules":test_modules})
    return directory_dictionaries

def extract_tests(directory_dictionary,tests):
    directory = directory_dictionary['directory']
    modules = directory_dictionary['modules']
    sys.path.append(directory)
    for test_file in modules:
        module = importlib.import_module(test_file)
        attributes = dir(module)
        for attribute in attributes:
            if attribute[0:5] == "test_":
                test = getattr(module, attribute)
                if callable(test):
                    tests.append(test)

def extract_module_dictionaries(directory_dictionary):
    directory = directory_dictionary['directory']
    modules = directory_dictionary['modules']
    sys.path.append(directory)
    module_dictionaries = []
    for test_file in modules:
        tests = []
        module = importlib.import_module(test_file)
        attributes = dir(module)
        for attribute in attributes:
            if attribute[0:5] == "test_":
                test = getattr(module, attribute)
                if callable(test):
                    tests.append(test)
        module_dictionaries.append({"module":test_file,"tests":tests})
    return module_dictionaries

def reset_sys_path(original_sys_path):
    to_remove = [path for path in sys.path if path not in original_sys_path]
    for path in to_remove:
        sys.path.remove(path)

def no_tests_found():
    intelligent_error_message = """
        No tests have been found -
        please note that there are strict naming conventions:
        1. Directory name are named "tests"
        2. Test files start with "test_"
        3. Test functions start with "test_"
        e.g. repository_path/src/tests/test_descriptive_name contains def test_describe
        """
    print(intelligent_error_message)
