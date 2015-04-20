import time
try:
    from bcbio.provenance import do
except ImportError:
    None


def fake_fn(n, args):
    print 'inside function with %s' % n
    time.sleep(n * 2)


def fake_cmd_fn(n, args):
    do.run("ls *", "testing cmds")
    print 'inside cmd function with %s' % n
    time.sleep(n * 2)
