import json
import random
from TestClass import TestClass 
from MySolution import MySolution 
import os
import inspect

dir_path = os.path.dirname(os.path.realpath(__file__))
config_path = os.path.join(dir_path, 'config.json')

with open(config_path) as f:
    config = json.load(f)

def setup():
    global executed_methods, successful_methods, missing_methods
    
    successful_tests = 0
    executed_tests = 0
    successful_methods = 0
    executed_methods = 0
    missing_methods = []
    
    test_cases = config['testcases']
    for test_case_name, test_case in test_cases.items():
        executed_tests += 1
        print(f'Running test case: {test_case_name}')
        constructor_values = generate_parameters(test_case['constructor'])
        
        try:
            test_class_instance = TestClass(*constructor_values)
            my_solution_instance = MySolution(*constructor_values)
        except Exception as e:
            print('Error creating instances of classes')
            return

        print('Running constructor values:', constructor_values)

        for method in test_case['methods']:
            run_method(test_class_instance, my_solution_instance, method)
            
        print(f'Test case {test_case_name} finished')
        print(f'Executed methods: {executed_methods}, successful methods: {successful_methods}, Percentage: {percentage(successful_methods, executed_methods)}%\n\n')
        if successful_methods == executed_methods:
            successful_tests += 1
            
        executed_methods = 0
        successful_methods = 0
        
    print(f'Executed tests: {executed_tests}, successful tests: {successful_tests}, Percentage: {percentage(successful_tests, executed_tests)}%')
    print(f'Missing methods: {missing_methods}')

def run_method(test_class_instance, my_solution_instance, method):
    global executed_methods, successful_methods, missing_methods
    executed_methods += 1
    method_name = method['method']
    all_methods = find_same_methods()
    if method_name not in all_methods:
        if not inspect.ismethod(getattr(test_class_instance, method_name, None)):
            print(f"Method '{method_name}' does not exist in TestClass")
            if method_name not in missing_methods:
                missing_methods.append(method_name)
            return
    
    test_class_method = getattr(test_class_instance, method_name)
    my_solution_method = getattr(my_solution_instance, method_name)
    if len(inspect.signature(test_class_method).parameters) != len(inspect.signature(my_solution_method).parameters):
        print(f"Method '{method_name}' in TestClass and MySolution have different number of parameters")
        if method_name not in missing_methods:
            missing_methods.append(method_name)
        return
    
    if 'parameters' not in method:
        method['parameters'] = []
    generated_params = generate_parameters(method['parameters'])
    test_class_result = test_class_method(*generated_params or [])
    my_solution_result = my_solution_method(*generated_params or [])
    if test_class_result == my_solution_result:
        print(f"Method '{method_name}' with values", generated_params, f"passed returned {my_solution_result}")
        successful_methods += 1
    else:
        print(f"Method '{method_name}' with values", generated_params, f"failed expected {my_solution_result} but got {test_class_result}")

def generate_parameters(parameters):
    args = []
    for param in parameters:
        if param[0] == 'i':
            args.append(get_int_value(param[1:]))
        elif param[0] == 's':
            args.append(param[1:])
        elif param[0] == 'c':
            args.append(param[1])
        elif param[0] == 'e':
            args.append(random.choice(config[param[1:]]))
        else:
            print('Invalid parameter type')
            return
    return args

def get_int_value(value):
    t = value[0]
    x = value[1:].split(',')[0]
    if x.isdigit():
        max_numeric_value = int(x)
    val = 0
    if t == 'P':
        val = 1 + random.random() * max_numeric_value
    elif t == 'N':
        val = -random.random() * max_numeric_value
    elif t == 'Z':
        val = 0
    elif t == 'R':
        val = -max_numeric_value + random.random() * (2 * max_numeric_value + 1)
    elif t == 'X':
        val = float(value[1:].split(',')[0])
    elif t == 'I':
        interv = value[1:].split(',')
        val = float(interv[0]) + random.randint(0, float(interv[1]) - float(interv[0]) + 1)
    return int(val)

def find_same_methods():
    test_class_methods = inspect.getmembers(TestClass, predicate=inspect.isfunction)
    my_solution_methods = inspect.getmembers(MySolution, predicate=inspect.isfunction)
    same_methods = []
    for test_class_method in test_class_methods:
        for my_solution_method in my_solution_methods:
            if test_class_method[0] == my_solution_method[0] and are_method_signature_equal(test_class_method[1], my_solution_method[1]):
                same_methods.append(test_class_method[0])
    return same_methods

def are_method_signature_equal(test_class_method, my_solution_method):
    return len(inspect.signature(test_class_method).parameters) == len(inspect.signature(my_solution_method).parameters)

def percentage(part, whole):
    return round(100 * part / whole, 2) if whole != 0 else 0

setup()
