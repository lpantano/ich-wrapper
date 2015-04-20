import time
from argparse import ArgumentParser

from ichwrapper import arguments, cluster, fake
from ichwrapper.log import logger

if __name__ == "__main__":
        start = time.time()
        parser = ArgumentParser(description="Test cluster")
        parser = arguments.myargs(parser)
        parser.add_argument("--cmd", default=False, action='store_true')
        args = parser.parse_args()
        # args = parser.parse_args(["--parallel", "ipython", "--local"])
        logger.info(args)
        resources = {'name': 'step1', 'mem': 1, 'cores': 1}
        cluster.send_job(fake.fake_fn, [1, 2], args, resources)
        if args.cmd:
            cluster.send_job(fake.fake_cmd_fn, [1, 2], args, resources)
        logger.info('It took %.3f minutes with ipython' % ((time.time()-start)/60))
