"""
    File: api.py
    Namespace: basis_testing
    Date: 26 April 2020

    Defines functions usable in templates.
"""

import numpy
import random
import itertools
import pkg_resources
BACKLOG = []
VARIABLES = {}
ALIASES = {}
BAD_WORDS = {}

def __load_bad_words():
    """
        Function __load_bad_words
        Loads the list of bad words into the set BAD_WORDS

        Inputs: None

        Output: None
    """
    global BAD_WORDS

    # Load datafile
    data = pkg_resources.resource_string(__name__, 'data/bad_words.txt').decode("utf-8")

    # Fill BAD_WORDS
    BAD_WORDS = {word.strip() for word in data.splitlines()}

def get_variables():
    global VARIABLES
    return VARIABLES

def clear_variables():
    global VARIABLES
    global ALIASES
    VARIABLES = {}
    ALIASES = {}

def set_backlog(in_backlog):
    """
        Function set_backlog
        Sets the choice backlog

        Inputs: 
        - in_backlog: the choice backlog to set

        Output: None
    """
    global BACKLOG
    BACKLOG = in_backlog

def choice(choices):
    """
        Function choice
        Make a choice between options

        Inputs: 
        - choices: the possible options

        Output: One of the options
    """
    global BACKLOG
    if not BACKLOG:
        sys_random = random.SystemRandom()
        return sys_random.choice(choices)
    else:
        return BACKLOG.pop(0)

def alias(alias, reference):
    """
        Function alias
        Defines a new alias

        Inputs: 
        - alias: the reference of the alias to define
        - reference: the reference to define the alias as

        Output: None
    """
    global ALIASES
    ALIASES[alias] = reference

def __generate_var(length = 3, depth = 0):
    """
        Function __generate_var
        Generates a random variable name of the specified length

        Inputs: 
        - length: the length of the variable to generate

        Output: A new random variable name
    """
    global VARIABLES
    global BAD_WORDS
    vowels = 'aeiou'
    consonants = 'bcdfghjklmnpqrstvwxyz'
    variable = ''

    # Generate some pseudo-language variable
    for i in range(length):
        # Randomly determine to use consonants or vowels
        random_number = random.random()
        if random_number < 0.5:
            variable += random.choice(consonants)
        else: 
            variable += random.choice(vowels)
    
    # Determine invalid variable names
    invalid = set(VARIABLES.values())

    # Recursively generate a different variable name if the variable name is invalid
    if variable in invalid or variable in BAD_WORDS:
        # Don't run forever!
        if depth > 100:
            raise Exception('No more variable names available')

        return __generate_var(length, depth + 1)
        
    return variable

def var(reference):
    """
        Function var
        Returns a known or new variable name based on the provided reference

        Inputs: 
        - reference: the reference of the variable, optionally with a variable length

        Output: Known or new variable name
    """
    global VARIABLES
    global ALIASES

    # Split actual reference from length specification
    reference_split = reference.split(':')
    assert 1 <= len(reference_split) <= 2, f'Variable reference \'{reference}\' is invalid.'

    # Attempt to find the variable in the known references
    if reference_split[0] in VARIABLES:
        return VARIABLES[reference_split[0]]

    # Attempt to find the variable in the known aliases
    if reference_split[0] in ALIASES:
        return VARIABLES[ALIASES[reference_split[0]]]

    # Attempt to indentify if the reference is a combination of known variables (max 5)
    for i in range(1, 6):
        # Determine possible combinations for this specific length
        permutations = itertools.permutations(VARIABLES, i)
        joint_variables = {''.join(permutation) : permutation for permutation in permutations}
        
        # Compare to the provided reference and create new alias if found
        if reference_split[0] in joint_variables:
            alias(reference_split[0], random.choice(joint_variables[reference_split[0]]))
            return VARIABLES[ALIASES[reference_split[0]]]

    # Generate random variable
    if len(reference_split) == 1:
        random_var = __generate_var()
    else:
        random_var = __generate_var(length = int(reference_split[1]))

    # Assign and return new variable
    VARIABLES[reference_split[0]] = random_var
    return VARIABLES[reference_split[0]]

v = var

def relop():
    """
        Function relop
        Return a random comparison operator

        Inputs: None

        Output: a string containing a random comparison operator
    """
    return random.choice(["==", "<=", ">", "<", ">=", "!="])

def integer(start, end, steps=1):
    """
        Function integer
        Return a random integer

        Inputs:
        - start: minimum allowed value
        - end: maximum allowed value (inclusive)
        - steps: the interval from which to select the random integers

        Output: a string containing a random integer
    """
    return str(int(random.randrange(start, end + 1, steps)))

i = integer

def floating(start, end, steps=0.5, max_decimals=2):
    """
        Function floating
        Return a random float

        Inputs:
        - start: minimum allowed value
        - end: maximum allowed value (inclusive)
        - steps: the interval from which to select the random floats
        - max_decimals: maximum number of decimals

        Output: a string containing a random float
    """
    return round(float(random.choice(numpy.arange(start, end + 1, steps))), max_decimals)

f = floating

def number(start, end, steps=1, max_decimals=2):
    """
        Function number
        Return a random number

        Inputs:
        - start: minimum allowed value
        - end: maximum allowed value (inclusive)
        - steps: the interval from which to select the random numbers
        - max_decimals: maximum number of decimals

        Output: a string containing a random number, int or float
    """
    is_int = random.choice([2, 3])

    if is_int == 2:
        stps = round(steps)
        if stps < 1:
            stps = 1

        return integer(start, end, steps=stps)
    else:
        return floating(start, end, steps=steps, max_decimals=max_decimals)

n = number

def intlist(start, end, minlength, maxlength, intsteps=1, lengthsteps=1):
    """
        Function intlist
        Return a list of random length containing random integers

        Inputs:
        - start: minimum allowed integer value
        - end: maximum allowed integer value (inclusive)
        - minlength: the minimum amount of integers in the list
        - maxlength: the maximum amount of integers in the list (inclusive)
        - intsteps: the interval from which to select the random integers
        - lengthsteps: the interval from which to select the amount of integers in the list

        Output: a string containing a list of random integers
    """
    # Determine length of the list 
    length = int(random.randrange(minlength, maxlength + 1, lengthsteps))

    # Generate and return list
    return str([int(random.randrange(start, end + 1, intsteps)) for _ in range(length)])

__load_bad_words()

def compex(variable, start, end, steps):
    sys_random = random.SystemRandom()
    return var(variable) + ' ' + sys_random.choice(['<', '>', '==', '!=', '<=', '>=']) + ' ' + str(number(start, end, steps))
