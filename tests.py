import unittest

from datetime import datetime

from logger import Logger


class TestLogger(Logger):

    include = []  # "reset" include default for more clear test results

    def __init__(self, *args, **kwargs):
        self.logs = []
        super().__init__(*args, **kwargs)

    def format_function(self, function_name):
        return function_name # discard formatting

    def format_module(self, module_name):
        return module_name # discard formatting

    def write_log(self, *args):
        self.logs.append(args)


class IncludeLogger(TestLogger):
    include = [
        'function',
        'another_function',
    ]


class ExcludeLogger(TestLogger):
    include = [
        '*',
    ]
    exclude = [
        'function',
    ]


class CustomFormattedLogger(TestLogger):

    def get_timestamp(self):
        return datetime.utcnow().isoformat()

    def format_function(self, function_name):
        return f'*** {function_name} ***'

    def format_module(self, module_name):
        return f'### {module_name} ###'


def function(logger, msg='...!'):
    logger.log(msg)

def another_function(logger, msg='...?'):
    logger.log(msg)


class TestStringMethods(unittest.TestCase):

    def call(self, function, logger, msg=None, should_succeed=False):
        count = len(logger.logs)
        kwargs = {'msg': msg} if msg is not None else {}
        function(logger, **kwargs)
        # int(False)=0 & int(True)=1
        self.assertEqual(len(logger.logs), count + should_succeed)

    # include=['func'], exclude=[] => False, func=True
    def test__basic(self):
        logger = TestLogger(include=['function'])

        # another_function => False
        self.assertEqual(len(logger.logs), 0)
        another_function(logger)
        self.assertEqual(len(logger.logs), 0)

        # function => True
        self.assertEqual(len(logger.logs), 0)
        function(logger)
        self.assertEqual(len(logger.logs), 1)

        log = logger.logs[0]
        self.assertEqual(log[1], 'function')
        self.assertEqual(log[2], '__main__')
        self.assertEqual(log[3], '...!')

    # include=['func1'], exclude=['func2'] => False, func1=True
    def test__basic_with_exclude(self):
        logger = TestLogger(
            include=['function'],
            exclude=['another_function']
        )
        self.assertEqual(len(logger.logs), 0)
        function(logger)
        self.assertEqual(len(logger.logs), 1)
        another_function(logger)
        self.assertEqual(len(logger.logs), 1)

    # include=['func1'], exclude=['func1'] => False
    def test__basic_mutually_exclusive(self):
        logger = TestLogger(
            include=['function'],
            exclude=['function']
        )
        self.assertEqual(len(logger.logs), 0)
        function(logger)
        self.assertEqual(len(logger.logs), 0)
        another_function(logger)
        self.assertEqual(len(logger.logs), 0)

    # include=['*'], exclude=[] => True
    def test__catch_all(self):
        logger = TestLogger(include=['*'])

        self.assertEqual(len(logger.logs), 0)
        function(logger)
        self.assertEqual(len(logger.logs), 1)

        log = logger.logs[0]
        self.assertEqual(log[1], 'function')
        self.assertEqual(log[2], '__main__')
        self.assertEqual(log[3], '...!')

        self.assertEqual(len(logger.logs), 1)
        another_function(logger)
        self.assertEqual(len(logger.logs), 2)

        log = logger.logs[1]
        self.assertEqual(log[1], 'another_function')
        self.assertEqual(log[2], '__main__')
        self.assertEqual(log[3], '...?')

    # include=['*', 'func1'], exclude=[] => True
    def test__catch_all_misconfigured(self):
        logger = TestLogger(include=['*', 'function'])

        self.assertEqual(len(logger.logs), 0)
        function(logger)
        self.assertEqual(len(logger.logs), 1)
        another_function(logger)
        self.assertEqual(len(logger.logs), 2)

    # include=['*'], exclude=['*'] => True
    def test__exclude_mutually_exclusive_wildcards(self):
        logger = TestLogger(include=['*'], exclude=['*'])

        self.assertEqual(len(logger.logs), 0)
        another_function(logger)
        self.assertEqual(len(logger.logs), 1)
        function(logger)
        self.assertEqual(len(logger.logs), 2)

    # include=['*'], exclude=['func'] => True, func=False
    def test__catch_all_with_exclude(self):
        logger = TestLogger(include=['*'], exclude=['function'])

        self.assertEqual(len(logger.logs), 0)
        function(logger)
        self.assertEqual(len(logger.logs), 0)
        another_function(logger)
        self.assertEqual(len(logger.logs), 1)

        log = logger.logs[0]
        self.assertEqual(log[1], 'another_function')
        self.assertEqual(log[2], '__main__')
        self.assertEqual(log[3], '...?')

    # include=['*', 'func1'], exclude=['func1'] => True, func1=False
    def test__catch_all_with_exclude_misconfigured_1(self):
        logger = TestLogger(include=['*', 'function'], exclude=['function'])

        self.assertEqual(len(logger.logs), 0)
        function(logger)
        self.assertEqual(len(logger.logs), 0)
        another_function(logger)
        self.assertEqual(len(logger.logs), 1)

    # include=['*', 'func1'], exclude=['func2'] => True, func2=False
    def test__catch_all_with_exclude_misconfigured_2(self):
        logger = TestLogger(
            include=['*', 'function'],
            exclude=['another_function']
        )

        self.assertEqual(len(logger.logs), 0)
        function(logger)
        self.assertEqual(len(logger.logs), 1)
        another_function(logger)
        self.assertEqual(len(logger.logs), 1)

    # include=[], exclude=['*'] => False
    def test__exclude_wildcard(self):
        logger = TestLogger(exclude=['*'])

        self.assertEqual(len(logger.logs), 0)
        function(logger)
        self.assertEqual(len(logger.logs), 0)
        another_function(logger)
        self.assertEqual(len(logger.logs), 0)

    def test__include_logger(self):

        logger = IncludeLogger()
        self.assertEqual(len(logger.logs), 0)
        function(logger)
        self.assertEqual(len(logger.logs), 1)
        another_function(logger)
        self.assertEqual(len(logger.logs), 2)

        logger = IncludeLogger(include=['function'])  # reset include
        self.assertEqual(len(logger.logs), 0)
        function(logger)
        self.assertEqual(len(logger.logs), 1)
        another_function(logger)
        self.assertEqual(len(logger.logs), 1)

    def test__exclude_logger(self):

        logger = ExcludeLogger()
        self.assertEqual(len(logger.logs), 0)
        function(logger)
        self.assertEqual(len(logger.logs), 0)
        another_function(logger)
        self.assertEqual(len(logger.logs), 1)

        logger = ExcludeLogger(exclude=['another_function'])  # reset exclude
        self.assertEqual(len(logger.logs), 0)
        function(logger)
        self.assertEqual(len(logger.logs), 1)
        another_function(logger)
        self.assertEqual(len(logger.logs), 1)

    def test__custom_formatted_logger(self):
        logger = CustomFormattedLogger(include=['*'])
        self.call(function, logger, should_succeed=True)
        log = logger.logs[0]
        self.assertIn('T', log[0])
        self.assertIn('***', log[1])
        self.assertIn('###', log[2])

    def test__init(self):
        with self.assertRaises(AssertionError) as e:
            Logger(include='*')
        with self.assertRaises(AssertionError) as e:
            Logger(exclude='function')


if __name__ == '__main__':
    unittest.main()
