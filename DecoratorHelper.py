class DecoratorHelper:

    def __init__(self, *args, **kwargs):
        self.function = None
        self.decorator_args = None
        self.decorator_kwargs = None
        self.function_args = None
        self.function_kwargs = None

        if hasattr(args[0], '__call__'):
            self.function = args[0]
            self.decorator_with_args = False
        else:
            self.decorator_args = args
            self.decorator_kwargs = kwargs
            self.decorator_with_args = True

    def __call__(self, *args, **kwargs):
        if self.decorator_with_args:
            self.function = args[0]
        else:
            self.function_args = args
            self.function_kwargs = kwargs

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
                         decorator_kwargs,
                         args,
                         kwargs,
                         ):
                self.function = function
                self.decorator_args = decorator_args
                self.decorator_kwargs = decorator_kwargs
                self.function_args = args
                self.function_kwargs = kwargs

                wraps(self, self.function)

            def __call__(self, *args, **kwargs):
                self.function_args = args
                self.function_kwargs = kwargs
                return self.function(*self.function_args, **self.function_kwargs)

        wraps(self, self.function)

        if self.decorator_with_args:
            return Wrapper(self.function,
                           self.decorator_args,
                           self.decorator_kwargs,
                           self.function_args,
                           self.function_kwargs,
                           )
        else:
            return Wrapper(self.function,
                           self.decorator_args,
                           self.decorator_kwargs,
                           self.function_args,
                           self.function_kwargs,
                           ).__call__(*self.function_args,
                                      **self.function_kwargs
                                      )



# @DecoratorHelper(100, 'l')
# def foo(*args, **kwargs):
#     return 'Result: ', *args
#
#
# print("-"*30)
# print('type', type(foo))
# print('inst', (foo(5)))
# print('decorator_args', foo.decorator_args)
# print('function_args', foo.function_args)
# print('__name__', foo.__name__)
#
#
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
