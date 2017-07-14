from functools import wraps


class PubSub(object):

    @classmethod
    def run(cls, target_function_list={}, ret=None, **public_kwargs):
        for f_name, func in target_function_list.items():
            func(ret, **public_kwargs)

    @classmethod
    def pub(cls, name, condition=lambda *args, **kwargs: True):
        """

        if you want to trigger something by someone function 
        you install it to that function ~ 
        """
        target_f = getattr(cls, name, None)
        if target_f == None:
            setattr(cls, name, {})

        def _wrapper(f):
            @wraps(f)
            def __wrapper(*args, **kwargs):
                target_f = getattr(cls, name, None)
                ret = f(*args, **kwargs)
                if condition(*args, **kwargs):
                    cls.run(target_f, ret, **kwargs)
                
                return ret
            return __wrapper
        return _wrapper

    @classmethod
    def sub(cls, name):
        target_f = getattr(cls, name, None)
        if target_f == None:
            setattr(cls, name, {})

        def _wrapper(f):
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

@PubSub.pub('collection_channel')
@PubSub.pub('notify_channel')
@PubSub.pub('condition_channel', my_condition)
def i_am_login(uid, age):
    print 'login with ~~', uid, 'age', age
    return age


@PubSub.sub('condition_channel')
def after_con_hook(ret, **public_kwargs):
    print '[x] query database for uid=123', public_kwargs

@PubSub.sub('notify_channel')
def notify_everyone(ret, **public_kwargs):
    print '[P] a new one login with', public_kwargs

@PubSub.sub('notify_channel')
def notify_everyone_2(ret, **public_kwargs):
    print '[P-2] a new one login with', public_kwargs


@PubSub.sub('collection_channel')
def notify_everyone(ret, **public_kwargs):
    print '[C] a new one login with, collection return value', ret


if __name__ == '__main__':
    i_am_login('123', age=29)
    i_am_login(uid='833', age=19)
