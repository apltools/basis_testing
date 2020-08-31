"""
    File: __init__.py
    Namespace: basis_testing
    Date: 24 April 2020

    The main Template class used for completing templates.
"""

from basis_testing.api import *
import basis
import basis.eval.factories.restricted
import copy
import os
import itertools

STORE = {}

class Template:
    def __init__(self, template_text, validator = 'basis', choice_backlog=[]):
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
        self.choice_backlog = choice_backlog
        self.variables = None
        self.end_values = {}
        self.evaluate = ''

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
        self.end_values = {}
        self.variables = None

        set_backlog(copy.deepcopy(self.choice_backlog))
        clear_variables()

        # Split the template by line
        self.__split = self.template_text.splitlines()

        global STORE
        STORE = {}

        # Run through the template line-by-line
        for line in self.__split:
            # Detect and skip comments
            if re.match(r'^\s*//.*$', line):
                continue

            # Detect and skip lines with only whitespace if there is no output yet
            if re.match(r'^\s*$', line) and self.full_test == '':
                continue

            # Detect and replace dynamic variables
            line = re.sub(r'\$\s*([\w_\-:]+)\s*\$', lambda match : v(match.group(1)), line)

            # Detect and fill RegEx
            line = re.sub(r'#([^#]+)#', lambda match : str(xeger.xeger(match.group(1))), line)

            # Detect, run and replace inline Python
            line = re.sub(r'@([^@]+)@', lambda match : str(eval(match.group(1))), line)

            # Detect and run code to run in the background, then skip
            match_background = re.match(r'^\s*\.\.\s+(.+)\s*$', line)
            if match_background:
                exec(str(match_background.group(1)))
                continue

            # Write resulting line to output
            self.full_test += line + '\n'

        self.variables = get_variables()

        return self

    def discover(self):
        """
            Method discover
            Discovers all choices within the template

            Inputs: None

            Output: Template object
        """
        # Init
        import re
        self.choices = []

        # Split the template by line
        self.__split = self.template_text.splitlines()

        # Run through the template line-by-line
        for line in self.__split:
            # Check if this is a choice of some kind
            match = re.match(r'[^c]*choice\(([^\(\)]+)\)[^\)]*', line)
            if match:
                # If it is a choice, add the choices to the list
                choice_group = eval(match.group(1))
                self.choices.append(choice_group)

        return self

    def find_variants(self):
        self.variants = []
        for element in itertools.product(*self.choices):
            self.variants.append(element)

        return self

    def complete(self, choice_backlog = []):
        """
            Method complete
            Fills in the template in order to create a finished test, then validates it and stores the output

            Inputs: None

            Output: Template object
        """
        self.choice_backlog = choice_backlog
        # Repeat untill validation succeeds, or we have tried 3 times
        count = 0
        while True:
            # Check count
            if count >= 3:
                return self

            # Fill the template
            self.__fill_template()

            try:
                os.remove('tempfile.basis')
            except:
                pass

            with open('tempfile.basis', 'w') as f:
                f.write(self.full_test)

            try:
                output = basis.interpret('tempfile.basis', factory=basis.eval.factories.restricted)
            except:
                os.remove('tempfile.basis')
            else:
                os.remove('tempfile.basis')
                return self

            count += 1

    def calc_end_values(self):
        for variable in self.variables:
            line_add = 'print(' + self.variables[variable] + ')\n'
            temp_test = copy.deepcopy(self.full_test)
            temp_test += line_add

            try:
                os.remove('tempfile.basis')
            except:
                pass

            with open('tempfile.basis', 'w') as f:
                f.write(temp_test)

            result = basis.interpret('tempfile.basis')[0]

            os.remove('tempfile.basis')
            
            self.end_values[self.variables[variable]] = result

        return self

    def calc_evaluate(self):
        temp_test = ''
        temp_split = self.full_test.splitlines()
        for i, line in enumerate(temp_split):
            temp_test += 'print(' + line.strip() + ')'
            if i < len(temp_split) - 1:
                temp_test += '\n'

        try:
            os.remove('tempfile.basis')
        except:
            pass

        with open('tempfile.basis', 'w') as f:
            f.write(temp_test)

        result = basis.interpret('tempfile.basis')[0]
        os.remove('tempfile.basis')
            
        self.evaluate = result
