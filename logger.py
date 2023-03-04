import inspect
from datetime import datetime


class Logger:

    include = [
        '*',
    ]
    exclude = [

    ]

    def __init__(self, include=None, exclude=None):
        allowed_types = (list, tuple, set)

        assert ((include is None)
            or any(isinstance(include, t) for t in allowed_types)
        ), f"allowed data types for include are: {allowed_types}"

        assert ((exclude is None)
            or any(isinstance(exclude, t) for t in allowed_types)
        ), f"allowed data types for exclude are: {allowed_types}"

        # args overide class variable
        self.include = include if include is not None else self.include
        self.exclude = exclude if exclude is not None else self.exclude

    def get_timestamp(self):
        return datetime.utcnow().strftime('%y/%m/%d %H:%M:%S.%f')

    def format_function(self, function_name):
        return function_name.ljust(25)

    def format_module(self, module_name):
        return module_name.ljust(50)

    def log(self, *args, important=False):

        # include=[], exclude=[]                    => False
        # include=[], exclude=['*']                 => False

        # include=['*'], exclude=[]                 => True
        # include=['*', 'func1'], exclude=[]        => True

        # include=['*'], exclude=['*']              => True

        # include=['*'], exclude=['func1']          => True, func1=False
        # include=['*', 'func1'], exclude=['func1'] => True, func1=False
        # include=['*', 'func1'], exclude=['func2'] => True, func2=False

        # include=['func1'], exclude=[]             => False, func1=True
        # include=['func1'], exclude=['func2']      => False, func1=True
        # include=['func1'], exclude=['func1']      => False

        frame = inspect.stack()[1]
        function = frame.function
        module = inspect.getmodule(frame[0]).__name__
        condition = (
            self.include
            and (function not in self.exclude)
            and (('*' in self.include) or (function in self.include))
        )

        if condition or important:
            self.write_log(
                self.get_timestamp(),
                self.format_function(function),
                self.format_module(module),
                *args,
            )

    def write_log(self, *args):
        print(*args, flush=True)
