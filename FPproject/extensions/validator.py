from flask import request, jsonify  # request 是全局的
from FPproject.helper.code import Code
import functools

# 类装饰器，初始化时可传的参数是字段以及其格式化类型
class Validator(object):

    def __init__(self, **parameter_template):
        self.pt = parameter_template

    def __call__(self, f):
        # 保留被装饰函数的属性,如__name__和__doc__
        @functools.wraps(f)
        def decorate_function(*args, **kwargs):  # 被装饰的视图函数需要传递的参数,注意都是通过get请求传参的,故不用试图函数特意接收
            request.params = {}
            try:
                for k, v in self.pt.items():
                    request.params[k] = v(request.values[k])  # 使用flask的全局变量request的values属性获得浏览器传递的值，
                    # 使用装饰器接收的字段类型函数将其格式化，如int，并以字典的形式存储到自定义的request属性params中

                    # print(1, type(request.values))  # 1 <class 'werkzeug.datastructures.CombinedMultiDict'>
                    # print(2, request.values[k])

            # 如果使用类型范化函数对get请求传递的值操作不成功，如int('abc')，那么就到这一步
            except Exception:
                # 自定义一个response对象，返回Code中定义的信息，自定义状态码100，必要参数缺失
                response = jsonify(
                    rc=Code.required_parameter_missing.value,
                    msg=Code.required_parameter_missing.name,
                    data={'require_param': k}  # k是字段，提示哪个字段缺失参数的字段
                )
                response.status_code = 400
                return response
            return f(*args, **kwargs)
        return decorate_function

class ValidationError(Exception):
    def __init__(self,message, values):
        super().__init__(message)
        self.values =values

def multi_int(values, sperator=','):
    return [int(i) for i in values.split(sperator)]

def complex_int(values, sperator = '-'):
    # 1-200-5000
    digits = values.split(sperator)
    result = []
    for digit in digits:
        if not digit.isdigit():
            raise ValidationError('complex int error:%s' % values, values)
        result.append(int(digit))
    return result

def multi_complex_int(values, sperator=','):
    # 1-200-5000,2-200-5000
    return [complex_int(i) for i in values.split(sperator)]


