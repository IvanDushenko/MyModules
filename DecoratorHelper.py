def wraps(wrapper, wrapped):
    try:
        wrapper.__doc__ = wrapped.__doc__
        wrapper.__name__ = wrapped.__name__
        wrapper.__module__ = wrapped.__module__
        wrapper.__qualname__ = wrapped.__qualname__
        wrapper.__annotations__ = wrapped.__annotations__
    except Exception as e:
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

        if hasattr(args[0], '__call__'):
            self.function = args[0]
            self.__decorator_with_args = False
        else:
            self.decorator_args = *args, kwargs
            self.__decorator_with_args = True

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
            return Wrapper(self.function,
                           self.decorator_args,
                           self.function_args,
                           ).__call__()


def a(obj):
    def b():
        print('bla', obj.function_args)

    obj.pre_function = b
    return obj


if __name__ == '__main__':
    pass
    # @a
    # @DecoratorHelper(100, 'l', d=5)
    # def foo(*args, **kwargs):
    #     return 'Result: ', *args
    #
    #
    # print("-"*30,'5 type', type(foo))
    # print("-"*30,'6 function_args', foo.function_args)
    # print("-"*30,'7 inst', (foo()))
    # print("-"*30,'8 function_args', foo.function_args)
    # print("-"*30,'9 inst', (foo(5)))
    # print("-"*30,'10 decorator_args', foo.decorator_args)
    # print("-"*30,'11 function_args', foo.function_args)
    # print("-"*30,'12 __name__', foo.__name__)
    #
    # @a
    # @DecoratorHelper
    # def bar(*args, **kwargs):
    #     return 'Result: ', *args
    #
    #
    # print("-"*30,'type', type(bar))
    # print("-"*30,'inst', (bar(5)))
    # print("-"*30,'decorator_args', bar.decorator_args)
    # print("-"*30,'function_args', bar.function_args)
    # print("-"*30,'__name__', bar.__name__)
    #
    #
    # @a
    # @DecoratorHelper(1)
    # class Foo:
    #     def __init__(self, *args, **kwargs):
    #         self.b = None
    #     def test(self, a):
    #         return a
    #
    #
    # print("-"*30)
    # print('Foo_inst', Foo)
    # print('Foo_inst', Foo(5).test(20))
    # print('decorator_args', Foo.decorator_args)
    # print('function_args', Foo.function_args)
    # print('Foo_inst __name__', Foo.__name__)
    #
    #
    # @a
    # @DecoratorHelper
    # class Bar:
    #     def test(self):
    #         return '1'
    #
    #
    # print("-" * 30, 'Bar_inst', Bar)
    # print("-" * 30, 'decorator_args', Bar.decorator_args)
    # print("-" * 30, 'function_args', Bar.function_args)
    # print("-" * 30, 'Bar_inst', Bar().test())
    # print("-" * 30, 'Bar_inst __name__', Bar.__name__)
