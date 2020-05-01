"""
    File: __init__.py
    Namespace: basis_testing
    Date: 24 April 2020

    The main Template class used for completing templates.
"""

from basis_testing.api import *

class Template:
    def __init__(self, template_text, validator = 'basis'):
        """
            Method __init__
            Initializes the Template object with some basic values

            Inputs: 
            - template_text: the template to convert in text-format
            - validator: which validator to use to validate the resulting test (optional)

            Output: Template object
        """
        self.template_text = template_text
        self.validator = validator

    def __fill_template(self):
        """
            Method __fill_template
            Fills in the template

            Inputs: None

            Output: Template object
        """
        # Basic imports and initialization
        import re
        from xeger import Xeger
        xeger = Xeger()
        self.full_test = ''

        # Split the template by line
        self.__split = self.template_text.splitlines()

        # Run through the template line-by-line
        for line in self.__split:
            # Detect and skip comments
            if re.match(r'^\s*//.*$', line):
                continue

            # Detect and skip lines with only whitespace if there is no output yet
            if re.match(r'^\s*$', line) and self.full_test == '':
                continue

            # Detect and run code to run in the background, then skip
            match_background = re.match(r'^\s*\.\.\s+(.+)\s*$', line)
            if match_background:
                eval(match_background.group(1))
                continue

            # Detect and replace dynamic variables
            line = re.sub(r'\$\s*([\w_\-:]+)\s*\$', lambda match : v(match.group(1)), line)

            # Detect and fill RegEx
            line = re.sub(r'#([^#]+)#', lambda match : str(xeger.xeger(match.group(1))), line)

            # Detect, run and replace inline Python
            line = re.sub(r'@([^@]+)@', lambda match : str(eval(match.group(1))), line)

            # Write resulting line to output
            self.full_test += line + '\n'

        return self

    def complete(self):
        """
            Method complete
            Fills in the template in order to create a finished test, then validates it and stores the output

            Inputs: None

            Output: Template object
        """
        # Repeat untill validation succeeds
        while True:
            # Fill the template
            self.__fill_template()

            # TODO: Add validation steps
            return self
