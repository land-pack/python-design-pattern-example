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
            def __wrapper(*args, **kwargs):
                target_f = getattr(cls, name)
                cls.run(target_f)
                ret = f(*args, **kwargs)
                return ret
            return __wrapper
        return _wrapper

    @classmethod
    def after(cls, name):
        def _wrapper(f):
            target_f = getattr(cls, name)
            target_f[f.func_name] = f
            def __wrapper(*args, **kwargs):
                pass
            return __wrapper
        return _wrapper


class HookManager(BaseManager):
    hook_after_login = {}


@HookManager.install('hook_after_login')
def login_api():
    print 'i am login api...'

print 'install trigger hook -----------------successful ~'

@HookManager.after('hook_after_login')
def i_do_something():
    print 'i am collection ....'

print 'install plugin hook -----------------successful ~'





if __name__ == '__main__':
    login_api()
