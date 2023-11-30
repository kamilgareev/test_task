from inspect import signature, Parameter
from functools import wraps


def my_decorator(dict_: dict):
    def wrapper(function):
        @wraps(function)
        def internal_wrapper(*args, **kwargs):
            # "Парсим" аргументы функции и находим изначальную сигнатуру функции
            sig = signature(function)
            all_args = [param
                        for param in sig.parameters if param]
            positional_only_args = [param.name
                                    for param in sig.parameters.values()
                                    if param.kind == param.POSITIONAL_ONLY]
            key_or_pos_args = [param.name
                               for param in sig.parameters.values()
                               if param.kind == param.POSITIONAL_OR_KEYWORD]

            key_args = [param.name
                        for param in sig.parameters.values()
                        if param.kind == param.KEYWORD_ONLY]

            # Находим default-ные значения и значения, которые будут использоваться для вызова функции
            to_be_used = {}
            default_values = {}
            for index in range(len(args)):
                to_be_used[all_args[index]] = args[index]
            for key, value in kwargs.items():
                to_be_used[key] = value
            for key, value in dict_.items():
                if key not in all_args:
                    continue
                if key in positional_only_args:
                    raise ValueError('Positional argument can not be assigned with a default value')
                if not to_be_used.get(key):
                    to_be_used[key] = value
                default_values[key] = value

            # Формируем новую сигнатуру (с соблюдением изначальных типов аргументов)
            function_sig = signature(function)
            new_sig_values = []
            for item in positional_only_args:
                new_sig_values.append(Parameter(name=item, kind=Parameter.POSITIONAL_ONLY))
            for item in key_or_pos_args:
                try:
                    if default_values[item]:
                        new_sig_values.append(
                            Parameter(name=item, default=default_values[item], kind=Parameter.POSITIONAL_OR_KEYWORD))
                    else:
                        new_sig_values.append(
                            Parameter(name=item, kind=Parameter.POSITIONAL_OR_KEYWORD))
                except KeyError:
                    pass
            new_sig_values.append(Parameter(name='args', kind=Parameter.VAR_POSITIONAL))
            for item in key_args:
                try:
                    if default_values[item]:
                        new_sig_values.append(
                            Parameter(name=item, default=default_values[item], kind=Parameter.KEYWORD_ONLY))
                    else:
                        new_sig_values.append(Parameter(name=item, kind=Parameter.KEYWORD_ONLY))
                except KeyError:
                    pass
            new_sig_values.append(Parameter(name='kwargs', kind=Parameter.VAR_KEYWORD))
            new_sig = function_sig.replace(parameters=new_sig_values, return_annotation=True)

            # Наконец, присваиваем функции новую сигнатуру
            function.__signature__ = new_sig

            # Готовим аргументы для вызова функции
            args_to_use = []
            for arg in positional_only_args:
                args_to_use.append(to_be_used[arg])
            keys_to_be_deleted = []
            for key in to_be_used.keys():
                if key in positional_only_args:
                    keys_to_be_deleted.append(key)
            for k in keys_to_be_deleted:
                del to_be_used[k]

            # Вызываем функцию
            return function(*args_to_use, **to_be_used)
        return internal_wrapper
    return wrapper


def foo(a, /, b, *args, c=5, d, **kwargs):
    """My function"""
    print(f'{a=} {b=} {args=} {c=} {d=} {kwargs=}')


@my_decorator({'b': 15, 'd': 17, 'c': 8})
def foo_wrapped(a, /, b, *args, c=5, d, **kwargs):
    """My wrapped function"""
    print(f'{a=} {b=} {args=} {c=} {d=} {kwargs=}')


help(foo)
help(foo_wrapped)
foo(10, 20, d=11)
foo_wrapped(10, d=22)