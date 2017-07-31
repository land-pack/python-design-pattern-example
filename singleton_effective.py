from collections import defaultdict
import redis


r = redis.Redis("localhost", 6379)

class SingletonEffective(object):

    _all_counter_prefix = 'singleton:effective:counter:{}'
    _all_done_counter_prefix = 'singleton:effective:counter:done:{}'
    _all_prefix = 'singleton:effective:all:{}'
    _done_prefix = 'singleton:effective:done:{}'
    _done_flag = 1
    _default_flag = 0
    _watch_with_counter = True
    expire_time = 120 * 60
    members = []

    @classmethod
    def load(cls, redis_handler):
        cls.redis_handler = redis_handler

    @classmethod
    def is_ava(cls, name, members):
        """
            if have available chance, will return True else False.
            if the current field is True (task have done), will stop
            record, pop up True. Next time come will ignore previous
            done-but-used key.
        """

        done_members = set(r.smembers(cls._done_prefix.format(name)) or [])
        undo_members = set(members) - done_members
        
        cls.members = members
        cls.all_done_members = list(done_members)

        member_do_flags = []
        for key in undo_members:
            value = int(cls.redis_handler.hget(cls._all_prefix.format(name), key) or cls._default_flag)
            member_do_flags.append(value)
            if str(value) == str(cls._done_flag) and cls._watch_with_counter:
                cls.redis_handler.sadd(cls._done_prefix.format(name), key)
                # if find one effective, close this operation by set flag
                cls._watch_with_counter = False

        cls.redis_handler.set(cls._all_counter_prefix.format(name), sum(member_do_flags))
        cls.redis_handler.set(cls._all_done_counter_prefix.format(name), len(done_members))

        cls.redis_handler.expire(cls._all_done_counter_prefix.format(name), cls.expire_time)
        cls.redis_handler.expire(cls._all_counter_prefix.format(name), cls.expire_time)
        cls.redis_handler.expire(cls._all_prefix.format(name), cls.expire_time)
        cls.redis_handler.expire(cls._done_prefix.format(name), cls.expire_time)
        return any(member_do_flags)



    @classmethod
    def is_done(cls, name):
        return len(cls.members) == len(cls.all_done_members)
    
    @classmethod
    def is_used(cls, name):
        return len(cls.members) == int(cls.redis_handler.get(cls._all_counter_prefix.format(name)))


    @classmethod
    def counter(cls, name):
        return cls.redis_handler.get(cls._all_done_counter_prefix.format(name))

    @classmethod 
    def done(cls, name, key):
        cls.redis_handler.hset(cls._all_prefix.format(name), key, cls._done_flag)

if __name__ == '__main__':
    SingletonEffective.load(r)
    name = 'frank'
    members = ['aa', 'bb', 'cc'] # 3 task need to do (SingletonEffective.done(name, key))
    print SingletonEffective.is_ava(name, members)
    
    print '-' * 80
    SingletonEffective.done(name, 'aa')
    print SingletonEffective.counter(name) # 1
    print SingletonEffective.is_done(name) # False
    print SingletonEffective.is_ava(name, members) # True
    print '=' * 80
    SingletonEffective.done(name, 'bb')
    SingletonEffective.done(name, 'cc')
    print SingletonEffective.counter(name) # 2
    print SingletonEffective.is_done(name) # False
    print SingletonEffective.is_ava(name, members) # True

    print '+' * 80
    print SingletonEffective.members
