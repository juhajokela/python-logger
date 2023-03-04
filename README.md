# python-logger

A simple and customizable logger implementation. For fun, obviously ;)

## Run tests

`python3 tests.py`

## Usage

### 1. SIMPLE: catch all

``` python
logger = Logger()

def function():
    logger.log('...!')
```

### 2. SIMPLE: include

``` python
logger = Logger(include=['function'])

def function():
    logger.log('...!')
```

### 3. SIMPLE: exclude

``` python
logger = Logger(exclude=['function'])

def function():
    logger.log('...!')
```

### 4. CLASS VARIABLES

``` python
class IncludeLogger(Logger):
    include = [
        'function_1',
        'function_2',
    ]

class ExcludeLogger(Logger):
    exclude = [
        'function_3',
    ]

logger = IncludeLogger(include=['function_1'])  # reset include
...

logger = ExcludeLogger(exclude=['function_1'])  # reset exclude
...
```

### 5. CUSTOM FORMATTING

``` python
class CustomLogger(Logger):

    def get_timestamp(self):
        return datetime.utcnow().isoformat()

    def format_function(self, function_name):
        return function_name  # no spacing

    def format_module(self, module_name):
        return module_name  # no spacing
```

### 6. CUSTOM WRITER

``` python
class CustomLogger(Logger):

    def write_log(self, timestamp, function, module, *args):
        # 1. omit timestamp, function and module names
        # 2. make sure that args are strings
        write_to_file(str(x) for x in args)
```

### ...

For more usage examples, check tests. :)