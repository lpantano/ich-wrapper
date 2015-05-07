import time
try:
    from bcbio.provenance import do
except ImportError:
    None


def fake_fn(data, args):
    print 'inside function with %s' % data
    time.sleep(data['num'] * 2)


def fake_cmd_fn(data, args):
    do.run("ls *", "testing cmds")
    print 'inside function with %s' % data
    time.sleep(data['num'] * 2)
