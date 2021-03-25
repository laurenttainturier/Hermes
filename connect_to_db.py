from functools import wraps

import psycopg2


def connect_to_db(db_config):
    def decorator(old_func):
        @wraps(old_func)
        def new_fun(*args, **kwargs):
            con = psycopg2.connect(
                database=db_config['database'],
                host=db_config['host'],
                port=db_config['port'],
                user=db_config['user'],
                password=db_config['pwd']
            )

            result = old_func(con, *args, **kwargs)

            con.close()
            return result

        return new_fun

    return decorator
