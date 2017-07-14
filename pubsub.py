from functools import wraps

class PubSub(object):


    @classmethod
    def run(cls, target_function_list={}, **public_kwargs):
        for f_name, func in target_function_list.items():
            func(**public_kwargs)


    @classmethod
    def pub(cls, name):
        """
        if you want to trigger something by someone function 
        you install it to that function ~ 
        """
        target_f = getattr(cls, name, None)
        if target_f == None:
            setattr(cls, name, {})
            target_f = getattr(cls, name, None)

        def _wrapper(f):
            @wraps(f)
            def __wrapper(*args, **kwargs): 
                target_f = getattr(cls, name, None)       
                cls.run(target_f, **kwargs)
                ret = f(*args, **kwargs)
                return ret
            return __wrapper
        return _wrapper
    
    @classmethod
    def pub_if(cls, name, condition):
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
                if condition(*args, **kwargs):
                    cls.run(target_f, **kwargs)
                else:
                    print 'condition no true'
                ret = f(*args, **kwargs)
                return ret
            return __wrapper
        return _wrapper


    @classmethod
    def sub(cls, name):
        target_f = getattr(cls, name, None)
        if target_f==None:
            setattr(cls, name, {})

        def _wrapper(f):
            target_f[f.func_name] = f
            @wraps(f)
            def __wrapper(*args, **kwargs):
                pass
            return __wrapper
        return _wrapper


@PubSub.pub('after_login')
def login_api():
    print 'i am login api'


@PubSub.sub('after_login')
def i_do_something(**public_kwargs):
    print 'i am collection all login user information....'


def my_condition(*args, **kwargs):
    uid = kwargs['uid']
    if uid =='123':
        return True
    else:
        return False

@PubSub.pub('hook_after_login')
@PubSub.pub_if('condition_hook', my_condition)
def i_am_login(uid, age):
    print 'login with ~~',uid, 'age',age

@PubSub.sub('condition_hook')
def after_con_hook(**public_kwargs):
    print 'i am do some collection only for uid=123', public_kwargs


if __name__ == '__main__':
    #login_api()
    i_am_login(uid='123',age=29)
    print '=test 2---------------------'
    i_am_login(uid='833',age=19)
