from functools import wraps

class BaseManager(object):


    @classmethod
    def run(cls, target_function_list={}):
        for f_name, func in target_function_list.items():
            func()


    @classmethod
    def install(cls, name):
        """
        if you want to trigger something by someone function 
        you install it to that function ~ 
        """

        def _wrapper(f):
            @wraps(f)
            def __wrapper(*args, **kwargs):
                target_f = getattr(cls, name)
                cls.run(target_f)
                ret = f(*args, **kwargs)
                return ret
            return __wrapper
        return _wrapper
    
    @classmethod
    def install_if(cls, name, condition):
        """
        if you want to trigger something by someone function 
        you install it to that function ~ 
        """
        def _wrapper(f):
            @wraps(f)
            def __wrapper(*args, **kwargs):
                target_f = getattr(cls, name)
                if condition(*args, **kwargs):
                    cls.run(target_f)
                else:
                    print 'condition no true'
                ret = f(*args, **kwargs)
                return ret
            return __wrapper
        return _wrapper


    @classmethod
    def after(cls, name):
        def _wrapper(f):

            target_f = getattr(cls, name)
            target_f[f.func_name] = f
            @wraps(f)
            def __wrapper(*args, **kwargs):
                pass
            return __wrapper
        return _wrapper


class HookManager(BaseManager):
    hook_after_login = {}


@HookManager.install('hook_after_login')
def login_api():
    print 'i am login api...'

@HookManager.after('hook_after_login')
def i_do_something():
    print 'i am collection all login user information....'


# Condition Hook Test

class ConditionHook(BaseManager):
    condition_hook = {}

def my_condition(*args, **kwargs):
    uid = kwargs['uid']
    if uid =='123':
        return True
    else:
        return False

@HookManager.install('hook_after_login')
@ConditionHook.install_if('condition_hook', my_condition)
def i_am_login(uid, age):
    print 'login with ~~',uid, 'age',age

@ConditionHook.after('condition_hook')
def after_con_hook():
    print 'i am do some collection only for uid=123'


if __name__ == '__main__':
    #login_api()
    i_am_login(uid='123',age=29)
    print '=test 2---------------------'
    i_am_login(uid='833',age=19)
