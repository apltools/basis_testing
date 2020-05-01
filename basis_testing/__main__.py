"""
    File: __main__.py
    Namespace: basis_testing
    Date: 26 April 2020

    The main entrypoint for running the basis_testing command.
"""

import argparse
from basis_testing import Template

def main():
    """
        Function main
        This function is called when the basis_testing command is ran.
    """
    # Initialize the arg parser
    parser = argparse.ArgumentParser(prog = 'basis_testing', description = 'Converts a test template into a complete test.')

    # Add first argument: the file containing the template
    parser.add_argument('template', default = 'test.template', help = 'The path to the template file')

    # Add second argument: the file to store the test in
    parser.add_argument('-o', '--output', default = 'test.basis', help = 'The path to store the resulting test')

    # Add third argument: the validator to use
    parser.add_argument('-v', '--validator', default = 'basis', choices = ['basis', 'none'], help = 'The validator class used to validate the resulting test')

    # Run parser
    args = parser.parse_args()

    # Read input file into a string:
    with open(args.template, 'r') as f:
        template_text = f.read()

    # Initalize template
    template = Template(template_text, validator = args.validator)

    # Run template
    template.complete()

    # Store result into file
    with open(args.output, 'w') as f:
        f.write(template.full_test)
