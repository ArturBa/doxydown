import unittest
from doxydown.classes import Function, Define
from doxydown.comments import function_comment, define_comment


class TestFunctionMethods(unittest.TestCase):

    def setUp(self):
        pass

    def test_function(self):
        test_code = ['/**\n',
                     ' * @brief Check if number is odd\n',
                     ' * This function checks if given number is odd\n',
                     ' * @attention Works only with integer\n',
                     ' * @param a number to check\n',
                     ' * @return True if odd, false if even\n',
                     ' * /\n',
                     'bool IsOdd(int a){\n']
        function_test = function_comment(test_code, len(test_code) - 2)
        function = Function()
        function.name = 'bool IsOdd(int a)'
        function.brief = 'Check if number is odd'
        function.attentions = ['Works only with integer']
        function.description = ['This function checks if given number is odd']
        function.params = ['a number to check']
        function.returns = ['True if odd, false if even']
        self.assertEqual(function_test.name, function.name)
        self.assertEqual(function_test.brief, function.brief)
        self.assertEqual(function_test.attentions, function.attentions)
        self.assertEqual(function_test.description, function.description)
        self.assertEqual(function_test.params, function.params)


class TestDefineMethods(unittest.TestCase):

    def setUp(self):
        pass

    def test_define(self):
        test_code = ['/**\n',
                     ' * @def Number defines\n',
                     ' * @brief basic number defines\n',
                     ' * Defines numbers to strings\n',
                     ' */\n',
                     ' #define ONE 1\n',
                     ' #define TWENTY_ONE 21\n']
        define_test = define_comment(test_code, 4)
        define = Define()
        define.name = 'Number defines'
        define.description = ['Defines numbers to strings']
        define.code = ['#define ONE 1', '#define TWENTY_ONE 21']
        define.brief = 'basic number defines'
        self.assertEqual(define.name, define_test.name)
        self.assertEqual(define.brief, define_test.brief)
        self.assertEqual(define.description, define_test.description)
        self.assertEqual(define.code, define_test.code)

    def test_define_1(self):
        test_code = ['/**\n',
                     ' @def Number defines\n',
                     ' @brief basic number defines\n',
                     ' Defines numbers to strings\n',
                     ' */\n',
                     ' #define ONE 1\n',
                     ' #define TWENTY_ONE 21\n']
        define_test = define_comment(test_code, 4)
        define = Define()
        define.name = 'Number defines'
        define.description = ['Defines numbers to strings']
        define.code = ['#define ONE 1', '#define TWENTY_ONE 21']
        define.brief = 'basic number defines'
        self.assertEqual(define.name, define_test.name)
        self.assertEqual(define.brief, define_test.brief)
        self.assertEqual(define.description, define_test.description)
        self.assertEqual(define.code, define_test.code)


if __name__ == '__main__':
    unittest.main()
