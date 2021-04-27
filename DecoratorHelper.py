class DecoratorHelper:
    """This class is intended for decorating called objects.
    Adds attributes that store arguments to an object and returns it."""

    def __init__(self, *args, **kwargs):
        self.function = None
        self.decorator_args = None
        self.function_args = None

        if hasattr(args[0], '__call__'):
            self.function = args[0]
            self.decorator_with_args = False
        else:
            self.decorator_args = *args, kwargs
            self.decorator_with_args = True

    def __call__(self, *args, **kwargs):
        if self.decorator_with_args:
            self.function = args[0]
        else:
            self.function_args = *args, kwargs

        def wraps(wrapper, wrapped):
            try:
                wrapper.__doc__ = wrapped.__doc__
                wrapper.__name__ = wrapped.__name__
                wrapper.__module__ = wrapped.__module__
                wrapper.__qualname__ = wrapped.__qualname__
                wrapper.__annotations__ = wrapped.__annotations__
            except:
                pass

        class Wrapper:

            def __init__(self,
                         function,
                         decorator_args,
                         args,
                         ):
                self.function = function
                self.decorator_args = decorator_args
                self.function_args = args
                self.pre_function = None

                wraps(self, self.function)

            def __call__(self, *args, **kwargs):
                self.function_args = *args, kwargs
                if hasattr(self.pre_function, '__call__'):
                    self.pre_function()
                return self.function(*self.function_args)

        wraps(self, self.function)

        if self.decorator_with_args:
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
    print("-" * 80)
    print('1 decorator_args', obj.decorator_args)
    obj.function_args = 2
    print('2 function_args', obj.function_args)
    print(obj(2))
    print('3 function_args', obj.function_args)
    print('4 function', obj.function())
    print("-" * 80)
    def b():
        print('bla')
    obj.pre_function = b
    return obj

@a
@DecoratorHelper(100, 'l', d=5)
def foo(*args, **kwargs):
    return 'Result: ', *args


# print("-"*30)
# print('5 type', type(foo))
# print('6 function_args', foo.function_args)
# print('7 inst', (foo()))
# print('8 function_args', foo.function_args)
# print('9 inst', (foo(5)))
# print('10 decorator_args', foo.decorator_args)
# print('11 function_args', foo.function_args)
# print('12 __name__', foo.__name__)

# @DecoratorHelper
# def bar(*args, **kwargs):
#     return 'Result: ', *args
#
#
# print("-"*30)
# print('type', type(bar))
# print('inst', (bar(5)))
# print('decorator_args', bar.decorator_args)
# print('function_args', bar.function_args)
# print('__name__', bar.__name__)
#
#
# @DecoratorHelper(1)
# class Foo:
#     def test(self, a):
#         return a
#
#
# print("-"*30)
# print('Foo_inst', Foo)
# print('Foo_inst', Foo().test(20))
# print('decorator_args', Foo.decorator_args)
# print('function_args', Foo.function_args)
#
# print('Foo_inst __name__', Foo.__name__)
#
#
# @DecoratorHelper
# class Bar:
#     def test(self):
#         return '1'
#
# print("-"*30)
# print('Bar_inst', Bar)
# print('decorator_args', Bar.decorator_args)
# print('function_args', Bar.function_args)
#
# print('Bar_inst', Bar().test())
# print('Bar_inst __name__', Bar.__name__)
