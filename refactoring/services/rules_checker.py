"""Contain class that checks code on clean code rules"""

from collections import defaultdict

from refactoring.services.constants import (
    ERROR_PREFIX_GET, ERROR_PREFIX_IS, ERROR_SNAKE_CASE_FUNCTIONS,
    ERROR_CAMEL_CASE_CLASSES, ERROR_DOCUMENTATION_FOR_FUNCTION,
    ERROR_DOCUMENTATION_FOR_CLASS,
    ERROR_TYPE_HINT_FOR_FUNCTION,
    ERROR_TYPE_HINT_FOR_FUNCTION_ARGUMENT,
)


def is_bool_function_correct(name: str, type_: str) -> bool:
    """Check function that returned a boolean

    Return True if the function starts with «is» prefix"""

    match name, type_:
        case str(name), str(type_):
            is_function_correct = type_ == 'return bool' \
                and name.startswith('is') \
                and name != 'is' \
                and name != 'is_'
        case _:
            is_function_correct = False

    return bool(is_function_correct)


def is_get_function_correct(name: str, type_: str) -> bool:
    """Check function that returned a value (exclude bool)

    Return True if the function starts with «get» prefix"""

    match name, type_:
        case str(name), str(type_):
            is_function_correct = type_ == 'return' \
                and name.startswith('get') \
                and name != 'get' \
                and name != 'get_'
        case _:
            is_function_correct = False

    return bool(is_function_correct)


class NamingStyle:
    """Naming styles for functions, methods, classes, etc"""

    snake_case = 'Snake Case'

    camel_case = 'Camel case'


class CodeRulesChecker:
    """Check code on clean code rules"""

    def __init__(self, code_modules: dict):
        self.code_modules = code_modules
        print('AAAAAAAAAAAA')
        print(self.code_modules['functions'][0].docstring)
        self.errors = defaultdict(list)

    def _check_all_rules(self) -> None:
        """Check code for all the rules"""

        self.__get_functions_starts_with_get()
        self.__bool_functions_starts_with_is()
        self.__functions_naming_style_is_snake_case()
        self.__classes_naming_style_is_camel_case()
        self.__all_modules_have_documentation()
        self.__all_functions_have_type_hint()
        self.__all_functions_have_type_hint_for_arguments()

    @property
    def __functions(self) -> tuple:
        """Return functions from the code"""

        if 'functions' in self.code_modules.keys():
            code_functions = self.code_modules['functions']
        else:
            code_functions = []

        return tuple(code_functions)

    @property
    def __classes(self) -> tuple:
        """Return classes from the code"""

        if 'classes' in self.code_modules.keys():
            code_classes = self.code_modules['classes']
        else:
            code_classes = []

        return tuple(code_classes)

    def __get_naming_style(self, name: str) -> NamingStyle:
        """Return naming style for the name.

        Possible naming styles:
        1) Snake case - get_user_login
        2) Camel case - getUserLogin or GetUserLogin

        """

        naming_style = ''

        if name.islower() and '_' in name:
            naming_style = NamingStyle.snake_case
        else:
            naming_style = NamingStyle.camel_case

        return naming_style

    def __all_modules_have_documentation(self) -> None:
        """Check that all modules have documentation"""

        for func in self.__functions:
            if not func.docstring:
                self.errors[
                    ERROR_DOCUMENTATION_FOR_FUNCTION
                ].append(func.name)

        for class_ in self.__classes:
            if not class_.docstring:
                self.errors[
                    ERROR_DOCUMENTATION_FOR_CLASS
                ].append(class_.name)

    def __all_functions_have_type_hint_for_arguments(self) -> None:
        """Check that all functions have type annotation for arguments"""

        for func in self.__functions:
            for arg in func.args:
                if not arg.annotation:
                    self.errors[
                        ERROR_TYPE_HINT_FOR_FUNCTION_ARGUMENT
                    ].append(f'аргумент "{arg.arg}" для функции {func.name}')

    def __all_functions_have_type_hint(self) -> None:
        """Check that all functions have type annotation (e.g. -> str)"""

        for func in self.__functions:
            if not func.type_hint:
                self.errors[
                    ERROR_TYPE_HINT_FOR_FUNCTION
                ].append(func.name)

    def __functions_naming_style_is_snake_case(self) -> None:
        """Check that functions and methods have Snake case naming style"""

        for func in self.__functions:
            naming_style = self.__get_naming_style(func.name)

            if naming_style != NamingStyle.snake_case:
                self.errors[ERROR_SNAKE_CASE_FUNCTIONS].append(func.name)

    def __classes_naming_style_is_camel_case(self) -> None:
        """Check that classes have Camel case naming style"""

        for class_ in self.__classes:
            naming_style = self.__get_naming_style(class_.name)

            if naming_style != NamingStyle.camel_case:
                self.errors[ERROR_CAMEL_CASE_CLASSES].append(class_.name)

    def __get_functions_starts_with_get(self) -> None:
        """Check that return functions start with the «get» prefix

        Example:
        1) get_value - not error
        2) server_handling - error
        3) getUserId - not error
        4) calculatePrise - error

        """

        for func in self.__functions:
            if func.type == 'return' and \
                    not is_get_function_correct(func.name, func.type):
                self.errors[ERROR_PREFIX_GET].append(func.name)

    def __bool_functions_starts_with_is(self) -> None:
        """Check that bool return functions start with the «is» prefix

        Example:
        1) is_empty - not error
        2) check_empty - error
        3) isValid - not error
        4) valid - error

        """

        for func in self.__functions:
            if func.type == 'return bool' \
                    and not is_bool_function_correct(func.name, func.type):
                self.errors[ERROR_PREFIX_IS].append(func.name)
