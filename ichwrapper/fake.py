import time


def fake_fn(n, args):
    print 'inside function with %s' % n
    time.sleep(n * 2)
