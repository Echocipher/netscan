import copy
from .postgresql import PostgreSQL
from utils.output import Output
from utils.utils import AuthFailure

def bruteforce_worker(target, timeout):
    for password in target['b_password_list']:
        username = target['b_username']

        postgresql = PostgreSQL(target['hostname'], target['port'], timeout)

        success = False
        stop = False

        success, _ = postgresql.auth(target['b_username'], password)
        if success:
            Output.write({'target': postgresql.url(), 'message': 'Authentication success with credentials %s and password %s' % (username, password)})
            stop = True

        try:
            postgresql.disconnect()
        except:
            pass

        if stop:
            break

def bruteforce_generator(target, username_file, password_file, simple_bruteforce=False):
    password_list = []
    if password_file != None:
        password_f = open(password_file)
        for f in password_f:
            f = f.strip()
            password_list.append(f)
        password_f.close()

    username_f = open(username_file)
    for u in username_f:
        u = u.strip()
        if len(u) == 0:
            continue

        if not simple_bruteforce:
            if ':' in u:
                p = [u.split(':', 1)[-1]]
                u = u.split(':', 1)[0]
            else:
                p = password_list
        else:
            if ':' in u:
                u = u.split(':', 1)[0]
            p = [u]

        t = copy.copy(target)
        t['b_username'] = u
        t['b_password_list'] = p

        yield t
    username_f.close()

def bruteforce_generator_count(target, username_file, password_file):
    count = 0

    username_f = open(username_file)
    for u in username_f:
        u = u.strip()
        if len(u) == 0:
            continue

        count += 1
    username_f.close()

    return count
