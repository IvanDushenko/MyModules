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
    #
    # print("-" * 150)
    # @a
    # @c
    # @DecoratorHelper(100, 'l', d=5)
    # def foo(*args, **kwargs):
    #     return 'Result: ', *args
    #
    #
    # print("-" * 30, 'type(foo)', type(foo))
    # print("-" * 30, 'foo.__name__', foo.__name__)
    # print("-" * 30, 'foo.__dict__', foo.__dict__)
    # print("-" * 30, '(foo(5))', (foo(5)))
    # print("-" * 30, 'foo.decorator_args', foo.decorator_args)
    # print("-" * 30, 'foo.function_args', foo.function_args)
    #
    # print("-" * 150)
    # @a
    # @c
    # @DecoratorHelper
    # def bar(*args, **kwargs):
    #     return 'Result: ', *args
    #
    #
    # print("-" * 30, 'type(bar)', type(bar))
    # print("-" * 30, '(bar(5))', (bar(5)))
    # print("-" * 30, 'bar.decorator_args', bar.decorator_args)
    # print("-" * 30, 'bar.function_args', bar.function_args)
    # print("-" * 30, 'bar.__name__', bar.__name__)
    # print("-" * 30, 'bar.__dict__', bar.__dict__)
    #
    # print("-" * 150)
    # @a
    # @c
    # @DecoratorHelper(1)
    # class Foo:
    #     def __init__(self, *args, **kwargs):
    #         self.b = None
    #     def test(self, a):
    #         return a
    #
    #
    # print("-"*30, 'type(Foo)', type(Foo))
    # print("-"*30, 'Foo', Foo)
    # print("-"*30, 'Foo(5).test(20)', Foo(5).test(20))
    # print("-"*30, 'Foo.decorator_args', Foo.decorator_args)
    # print("-"*30, 'Foo.function_args', Foo.function_args)
    # print("-"*30, 'Foo.__name__', Foo.__name__)
    # print("-"*30, 'Foo.__dict__', Foo.__dict__)
    #
    # print("-" * 150)
    # @a
    # @c
    # @DecoratorHelper
    # class Bar:
    #     def __init__(self, *args, **kwargs):
    #         self.b = None
    #     def test(self):
    #         return '1'
    #
    # print("-" * 30, 'type(Bar)', type(Bar))
    # print("-" * 30, 'Bar(2).test()', Bar(2).test())
    # print("-" * 30, 'Bar.decorator_args', Bar.decorator_args)
    # print("-" * 30, 'Bar.function_args', Bar.function_args)
    # print("-" * 30, 'Bar.__name__', Bar.__name__)
    # print("-" * 30, 'Bar.__dict__', Bar.__dict__)
