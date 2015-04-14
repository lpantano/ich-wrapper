import os

from bcbio import utils
from bcbio.log import logger
from cluster_helper import cluster as ipc

config_default = {'name': 'std', 'mem': 8, 'cores': 1}


def get_cluster_view(args):
    if not os.path.exists("ipython"):
        os.mkdir("ipython")
        os.mkdir("checkpoint")
    return ipc.cluster_view(args.scheduler, args.queue,
                          args.num_jobs, args.cores_per_job,
                          start_wait=args.timeout,
                          profile="ipython",
                          extra_params={"resources": args.resources,
                                        "mem": args.memory_per_job,
                                        "tag": "ichwrapper",
                                        "run_local": args.local})


def wait_until_complete(jobs):
    return [j.get() for j in jobs]


def is_done(step):
    if os.path.exists(os.path.join("checkpoint", step)):
        return True
    return False


def flag_done(step):
    with open(os.path.join("checkpoint", step), "w") as handle:
        handle.write("done")


def send_job(fn, data, args, resources=None):
    """decide if send jobs with ipython or run locally"""
    utils.safe_makedir("checkpoint")
    res = []
    if not resources:
        resources = config_default
    step = resources['name']
    logger.debug("doing %s" % step)
    if 'mem' not in resources or 'cores' not in resources:
        raise ValueError("resources without mem or cores keys: %s" % resources)
    else:
        args.memory_per_job = resources['mem']
        args.cores_per_job = resources['cores']
    if args.parallel == "ipython":
        if not is_done(step):
            with get_cluster_view(args) as view:
                for sample in data:
                    res.append(view.apply_async(fn, sample, args))
                res = wait_until_complete(res)
            flag_done(step)
            return res
    for sample in data:
        res.append(fn(sample, args))
    return res
