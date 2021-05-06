def wraps(wrapper, wrapped):
    try:
        wrapper.__doc__ = wrapped.__doc__
        wrapper.__name__ = wrapped.__name__
        wrapper.__module__ = wrapped.__module__
        wrapper.__qualname__ = wrapped.__qualname__
        wrapper.__annotations__ = wrapped.__annotations__
    except Exception:
        pass


class Wrapper:
    """Wrapping decorated object"""

    def __init__(self,
                 function,
                 decorator_args,
                 function_args,
                 ):

        self.function = function
        self.decorator_args = decorator_args
        self.function_args = function_args
        self.pre_function = None
        self.post_function = None

        wraps(self, self.function)

    def __make_function(self, ):
        if hasattr(self.pre_function, '__call__'):
            self.pre_function()

        if type(self.function_args[0]) != dict:
            self.res = self.function(self.function_args)
        else:
            self.res = self.function()

        if hasattr(self.post_function, '__call__'):
            self.post_function()
        return self.res

    def __call__(self, *args, **kwargs):
        if args or kwargs:
            self.function_args = *args, kwargs

        return self.__make_function()


class DecoratorHelper:
    """This class is intended for decorating called objects.
    Adds attributes that store arguments to an object and returns it."""

    def __init__(self, *args, **kwargs):
        self.function = None
        self.decorator_args = None
        self.function_args = None
        self.pre_function = None
        self.post_function = None

        if hasattr(args[0], '__call__'):
            self.function = args[0]
            self.__decorator_with_args = False
        else:
            self.decorator_args = *args, kwargs
            self.__decorator_with_args = True

    def __make_function(self, ):
        if hasattr(self.pre_function, '__call__'):
            self.pre_function()

        if type(self.function_args[0]) != dict:
            self.res = self.function(self.function_args)
        else:
            self.res = self.function()

        if hasattr(self.post_function, '__call__'):
            self.post_function()
        return self.res

    def __call__(self, *args, **kwargs):
        if self.__decorator_with_args:
            self.function = args[0]
            self.function_args = *args[1:], kwargs
        else:
            self.function_args = *args, kwargs

        wraps(self, self.function)
        if self.__decorator_with_args:
            return Wrapper(self.function,
                           self.decorator_args,
                           self.function_args,
                           )
        else:
            return self.__make_function()


def a(obj):
    def b():
        print('pre_function', obj.function_args)

    obj.pre_function = b
    return obj


def c(obj):
    def d():
        print('post', obj.decorator_args)

    obj.post_function = d
    return obj


if __name__ == '__main__':
    pass


    def testing(func):
        print("-" * 150)
        print("-" * 30, f'type({func.__name__!r})', type(func))
        print("-" * 30, f'{func.__name__!r}.__name__', func.__name__)
        print("-" * 30, f'{func.__name__!r}.__dict__', func.__dict__)
        print("-" * 30, f'({func.__name__!r}(5))', (func(5)))
        print("-" * 30, f'{func.__name__!r}.decorator_args', func.decorator_args)
        print("-" * 30, f'{func.__name__!r}.function_args', func.function_args)
        return func


    @a
    @c
    @DecoratorHelper(100, 'l', d=5)
    def foo(*args, **kwargs):
        return 'Result: ', *args


    testing(foo)


    @a
    @c
    @DecoratorHelper
    def bar(*args, **kwargs):
        return 'Result: ', *args


    bar(5)
    testing(bar)


    @a
    @c
    @DecoratorHelper(1)
    class Foo:
        def __init__(self, *args, **kwargs):
            self.b = None

        def test(self, a):
            return a


    Foo(5).test(20)
    testing(Foo)


    @a
    @c
    @DecoratorHelper
    class Bar:
        def __init__(self, *args, **kwargs):
            self.b = None

        def test(self):
            return '1'


    Bar(2).test()
    testing(Bar)
