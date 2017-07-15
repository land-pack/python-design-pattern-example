from functools import wraps


class PubSub(object):

    @classmethod
    def run(cls, target_function_list={}, ret=None, *input_args, **input_kwargs):
        for f_name, func in target_function_list.items():
            func(ret, *input_args, **input_kwargs)

    @classmethod
    def pub(cls, name, condition=lambda *args, **kwargs: True):
        target_f = getattr(cls, name, None)
        if target_f == None:
            setattr(cls, name, {})
        def _wrapper(f):
            @wraps(f)
            def __wrapper(*args, **kwargs):
                target_f = getattr(cls, name, None)

                ret = f(*args, **kwargs)
                if condition(*args, **kwargs):
                    cls.run(target_f, ret, *args, **kwargs)
                return ret
            return __wrapper
        return _wrapper

    @classmethod
    def sub(cls, name):
        target_f = getattr(cls, name, None)
        if target_f == None:
            setattr(cls, name, {})

        def _wrapper(f):
            target_f = getattr(cls, name, None)
            target_f[f.func_name] = f
            @wraps(f)
            def __wrapper(*args, **kwargs):
                pass
            return __wrapper
        return _wrapper


def my_condition(*args, **kwargs):
    uid = kwargs.get('uid')
    if uid == '123':
        return True
    else:
        return False


@PubSub.sub('with_condition_channel_1')
def abserver_with_condition(ret, *input_args, **input_kwargs):
    """
    If my condition is true, I care about that information!
    else ignore me!
    """
    print '[ S ] query database for uid=123', public_kwargs


@PubSub.pub('without_condition_channel_3')
@PubSub.pub('without_condition_channel_2')
@PubSub.pub('with_condition_channel_1', my_condition)
def user_login_api(*args, **kwargs):
    """
    if you like to call function with name the params, as below code show
        user_login_api(1234, 25)
    you should read the params by access the args tuple, as below code show
        uid, age = args
    How to define this function is up to you!
    """
    age = kwargs.get('age')
    uid = kwargs.get('uid')

    age = age if age else args[1]
    uid = uid if uid else args[0]

    print '[ P ] login with uid={} age={}'.format(uid, age)
    return kwargs.get('uid')


@PubSub.sub('without_condition_channel_2')
def abserver_without_condition_1(ret, *input_args, **input_kwargs):
    print '[ A ] a new user login with', input_kwargs


@PubSub.sub('without_condition_channel_2')
def abserver_without_condition_2(ret, *input_args, **input_kwargs):
    print '[ A ] a new one login with', input_args


@PubSub.sub('without_condition_channel_3')
def abserver_without_condition(ret, *input_args, **input_kwargs):
    print '[ C ] a new one login with, collection return value', ret

if __name__ == '__main__':
    print '=' * 15 + 'Test 1' + '='*40
    user_login_api('123', age=29)  # the both `args` and `kwargs`
    print '=' * 15 + 'Test 2' + '='*40
    user_login_api(uid='833', age=19)  # only `kargs`
