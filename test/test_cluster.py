from unittest import TestCase
# import os
import time

from argparse import ArgumentParser
from bcbio.log import logger
from ichwrapper import arguments, cluster


class TestCluster(TestCase):

    def test_cluster(self):

        def fake_fn(n, args):
            print 'inside function with %s' % n
            time.sleep(n * 2)

        start = time.time()
        parser = ArgumentParser(description="Test cluster")
        parser = arguments.myargs(parser)
        args = parser.parse_args()
        logger.info(args)
        resources = {'name': 'step1', 'mem': 1, 'cores': 1}
        cluster.send_job(fake_fn, [1, 2], args, resources)
        logger.info('It took %.3f minutes without ipython' % ((time.time()-start)/60))

