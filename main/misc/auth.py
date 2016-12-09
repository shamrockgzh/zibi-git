# -*- coding: utf-8 -*-
#拦截器,面向方向编程


from functools import wraps
from flask import request, jsonify, g
from cerberus import Validator
from app import UserOrdinary

#验证token格式,
def auth_required(f):
    @wraps(f)
    def wrapper(*args,**kwargs):
        token = request.headers.get('Token')
        document = {'Token':token}
        #验证器
        validator = Validator({
            'Token': {'type': 'string', 'minlength': 1},
        })

        #token 为空
        if token is None:
            resp_data = {
                'status': 'fail',
                'data': {
                    'message': 'NO_TOKEN',
                    'code': 0
                },
            }
            return jsonify(**resp_data)
        #token 格式错误
        if not validator.validate(document):
            resp_data = {
                'status': 'fail',
                'data': {
                    'message': 'TOKEN_ERROR',
                    'code':1
                },
            }
            return jsonify(**resp_data)
        #无此用户
        user = UserOrdinary.query.get(int(token))
        if not user:
            resp_data = {
                'status': 'fail',
                'data': {
                    'message': 'NOT_FIND_USER',
                    'code': 2,
                },
            }
            return jsonify(**resp_data)

        g.user = user
        return  f(*args,**kwargs)
    return wrapper
