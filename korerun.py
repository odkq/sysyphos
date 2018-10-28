#!/usr/bin/env python3
import pprint
import uuid


class Function:
    def __init__(self, parameters, expressions):
        self.parameters = parameters
        self.expressions = expressions


class BuiltInFunction:
    def __init__(self, callback):
        self.callback = callback


class Variable:
    def __init__(self, vartype, frame, value=None):
        vartypes = ['word', 'dword', 'byte', 'address', 'string', 'bool']
        if vartype not in vartypes:
            raise ValueError("Unknown var type {}".format(vartype))
        self.vartype = vartype
        self.frame = frame
        self.value = value


class KoreParser:
    def __init__(self):
        self.variables = {}
        self.functions = {}
        self.current_frame = 0
        self.load_builtin_functions()

    def parse(self, filename):
        f = open(filename, 'r')
        tokens = self._tokenize_input(f.read())
        self.ast = self._parse_ast(tokens)
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(self.ast)

    def _symbol_eval(self, symbol):
        ''' If it is not a list it can be a symbol to be resolved, or an
            inmediate variable '''
        if symbol in self.variables:
            print(" *** found symbol {} to ve a variable".format(symbol))
            return self.variables[symbol]
        else:
            if symbol[0] == '"':
                var = Variable('string', self.current_frame, symbol[1:-1])
            elif symbol[0].isdigit():
                tchar = symbol[-1]
                if tchar == 'w':
                    var = Variable('word', self.current_frame)
                elif tchar == 'd':
                    var = Variable('dword', self.current_frame)
                elif tchar == 'b':
                    var = Variable('byte', self.current_frame)
                else:
                    msg = "Unknown suffix {} for inmediate"
                    raise ValueError(msg.format(tchar))
                var.value = int(symbol[:-1])
            return self._temporary_var(var)

    def _temporary_var(self, var):
        uid = str(uuid.uuid4())
        self.variables[uid] = var
        return self.variables[uid]

    def add_callback(self, values):
        total = 0
        for v in values:
            value = int(v.value)
            total += value
        return self._temporary_var(Variable('word', self.current_frame,
                                            total))

    def print_callback(self, values):
        print(values[0])
        return None

    def _return_trueval(self):
        return self._temporary_var(Variable('bool', self.current_frame,
                                            True))

    def _return_falseval(self):
        return self._temporary_var(Variable('bool', self.current_frame,
                                            False))

    def gt_callback(self, values):
        print(" *** {} > {} ? ".format(values[0].value, values[1].value))
        if values[0].value > values[1].value:
            return self._return_trueval()
        else:
            return self._return_falseval()

    def lt_callback(self, values):
        print(" *** {} < {} ? ".format(values[0].value, values[1].value))
        if values[0].value < values[1].value:
            return self._return_trueval()
        else:
            return self._return_falseval()

    def plus_callback(self, values):
        print(" *** {} < {} ? ".format(values[0].value, values[1].value))
        if values[0].value < values[1].value:
            return self._return_trueval()
        else:
            return self._return_falseval()

    def address_callback(self, values):
        ''' Return the 'address' of a variable '''
        return self._temporary_var(Variable('address', self.current_frame,
                                   1234))

    def plus_callback(self, values):
        result = 0
        for value in values:
            print('Adding {}'.format(value.value))
            result += int(value.value)
        # TODO: Type promotion and juggling (do not return always w)
        return self._temporary_var(Variable('word', self.current_frame,
                                   result))


    def load_builtin_functions(self):
        self.functions['add'] = BuiltInFunction(self.add_callback)
        self.functions['print'] = BuiltInFunction(self.print_callback)
        self.functions['gt'] = BuiltInFunction(self.gt_callback)
        self.functions['lt'] = BuiltInFunction(self.lt_callback)
        self.functions['address'] = BuiltInFunction(self.address_callback)
        self.functions['plus'] = BuiltInFunction(self.plus_callback)

    def _frame_eval(self, expression):
        self.current_frame += 1
        print('Entering frame {}'.format(self.current_frame))

        return_value = None
        if type(expression[0]) != str:
            raise ValueError("Syntax error")
        fname = expression[0]
        if fname == 'function':
            # Function declaration
            # it is in the form (function <fname> <parameter1> ..
            #                    <parametern> <expression1> <expression>)
            #
            # fname and parameters need to be symbols, not expressions
            parameters = []
            expressions = []
            for symbol in expression[2:]:
                if type(symbol) == list:
                    expressions.append(symbol)
                else:
                    parameters.append(symbol)
            self.functions[expression[1]] = Function(parameters,
                                                     expressions)
        elif fname == 'declare':
            # Variable declaration
            # It is in the form (declare <varname> <type>)
            if len(expression) != 3:
                raise ValueError("declare accept 2 parameters")
            self.variables[expression[2]] = Variable(expression[1],
                                                     frame=0)
        elif fname == 'set':
            if len(expression) != 3:
                raise ValueError("set accept 2 parameters")
            if expression[1] not in self.variables.keys():
                msg = "setting {} not declared"
                raise ValueError(msg.format(expression[1]))
            self.variables[expression[1]] = self.eval(expression[2])

        elif fname == 'while':
            if len(expression) < 3:
                raise ValueError("while needs at least 3 parameters")
            condition = expression[1]
            expressions = expression[2:]
            while True:
                test = self.eval(condition)
                if test.value is True:
                    return_value = self.eval(expressions)
                else:
                    break
        elif fname == 'if':
            if len(expression) < 4:
                raise ValueError("if needs 2 or 3 parameters")
            condition = expression[1]
            if_expression = expression[2]
            if len(expression) > 3:
                else_expression = expression[3]
            else:
                else_expression = None
            test = self.eval(condition)
            if test.value is True:
                return_value = self.eval(if_expression)
            else:
                if else_expression is not None:
                    return_value = self.eval(else_expression)
        else:
            if fname not in self.functions:
                # pp = pprint.PrettyPrinter(indent=4)
                # pp.pprint(expression)
                msg = "Calling undefined function {}"
                raise ValueError(msg.format(fname))
            values = []
            for symbol in expression[1:]:
                value = self.eval(symbol)
                values.append(value)
            print('About to call {} with values {}'.format(fname, values))
            function = self.functions[fname]
            if function.__class__ == BuiltInFunction:
                return_value = function.callback(values)
            else:
                # XXX: Call defined function after setting frame variables
                pass

        # XXX: Delete variables of frame
        print('Exiting frame {}'.format(self.current_frame))
        self.current_frame -= 1
        if (return_value is not None):
            print(' ***** [{}] ***** '.format(return_value.value))
        return return_value

    def eval(self, ast=None):
        ''' Evaluate a series of expressions inside a branch of the AST,
            recursively resolving subbranches before evaluating functions '''
        return_value = None

        print('-----------')
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(ast)
        print('-----------')

        if ast is None:
            ast = self.ast

        if type(ast) != list:
            return self._symbol_eval(ast)

        if type(ast[0]) == list:
            for expression in ast:
                return_value = self._frame_eval(expression)
        else:
            return_value = self._frame_eval(ast)

        print("variables {} functions {}".format(self.variables,
              self.functions))
        return return_value

    def _tokenize_input(self, string):
        inside_quotes = False
        in_comment = False
        in_backslash = False
        current_string = ""
        output = []
        for c in string:
            if c == ';' and not inside_quotes:
                in_comment = True
            elif in_comment:
                if c == '\n':
                    in_comment = False
            elif c == '"':
                current_string += '"'
                if in_backslash:
                    in_backslash = False
                elif inside_quotes:
                    inside_quotes = False
                else:
                    inside_quotes = True
            elif in_backslash:
                current_string += '\\'
                current_string += c
                in_backslash = False
            elif c == '\\' and inside_quotes:
                in_backslash = True
            elif c.isalnum() or c == '-' or c == '_':
                current_string += c
                # elif not c.isspace():
            else:
                if c.isspace():
                    if inside_quotes:
                        current_string += c
                    elif current_string is not "":
                        output.append(current_string)
                        current_string = ""
                else:
                    if current_string is not "":
                        output.append(current_string)
                        current_string = ""
                    output.append(c)
        return output

    def _parse_ast(self, tokens):
        ast = []
        i = 0
        while i < len(tokens):
            symbol = tokens[i]
            if symbol == '(':
                subtokens = []
                parenthesis = 1
                while parenthesis != 0:
                    i += 1
                    if i > len(tokens):
                        raise ValueError("Unbalanced parenthesis")
                    symbol = tokens[i]
                    if symbol == '(':
                        parenthesis += 1
                    elif symbol == ')':
                        parenthesis -= 1
                    if parenthesis != 0:
                        subtokens.append(symbol)
                ast.append(self._parse_ast(subtokens))
            elif symbol == ')':
                raise ValueError("Unbalanced close parens")
            else:
                try:
                    ast.append(int(symbol))
                except ValueError:
                    ast.append(symbol)
            i += 1
        return ast


def main():
    parser = KoreParser()
    parser.parse('test.kore')
    parser.eval()


if __name__ == '__main__':
    main()
