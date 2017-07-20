from collections import defaultdict
import redis 

r = redis.Redis("localhost", 6379)

class Singleton(object):
    
    @classmethod
    def first_eff(cls, r, key, fields, ignore=1, ex=24 * 60 * 60):
        """
        r: redis handler
        key: user define the key (hash key)
        fields: user care about the field!
        """

        _join_key = key + '-'.join(fields)
        ignore_field = r.smembers(_join_key) or []
        ignore_field = set(ignore_field)
        fields = set(fields)
        care_fields = fields - ignore_field

        values = []
        for field in care_fields:
            v = r.hget(key, field)
            values.append(v)
            if str(v) == str(ignore):
                r.sadd(_join_key , field)
                break
        r.expire(_join_key, ex)
        return any(values)



if __name__ == '__main__':
    """
    If you have doing update like
    r.hset(the_keykey, 'aa', 1)
    the return value will be the true for one time~
    """
    print Singleton.first_eff(r, 'the_keykey', ['aa','bb','cc'])
    
