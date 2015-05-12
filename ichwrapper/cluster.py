import os
import yaml

from bcbio import utils
from bcbio.install import _get_data_dir
from bcbio.distributed import clargs
from bcbio.provenance import system
import bcbio.distributed.resources as res
from bcbio.distributed.ipython import create
# from bcbio import log
import log
from cluster_helper import cluster as ipc

config_default = {'name': 'std', 'mem': 8, 'cores': 1}


def get_cluster_view(args):
    if not os.path.exists("ipython"):
        utils.safe_makedir("ipython")
        utils.safe_makedir("checkpoint")
    return ipc.cluster_view(args['scheduler'], args['queue'],
                            args['num_jobs'], args['cores_per_job'],
                            start_wait=args['timeout'],
                            profile="ipython",
                            extra_params={"resources": args['resources'],
                                          "mem": args['mem'],
                                          "tag": "ichwrapper",
                                          "run_local": args['run_local']})


def wait_until_complete(jobs):
    return [[j.get()] for j in jobs] 


def is_done(step):
    if os.path.exists(os.path.join("checkpoint", step)):
        return True
    return False


def flag_done(step):
    with open(os.path.join("checkpoint", step), "w") as handle:
        handle.write("done")


def _calculate_resources(data, args, resources):
    parallel = clargs.to_parallel(args)
    config = data[0][0]['config']
    config['resources'].update({resources['name']: {'memory': "%sg" % resources['mem'], 'cores': resources['cores']}})
    parallel.update({'progs': [resources['name']]})
    # parallel = log.create_base_logger(config, parallel)
    # log.setup_local_logging(config, parallel)
    log.setup_log(config, parallel)
    dirs = {'work': os.path.abspath(os.getcwd())}
    system.write_info(dirs, parallel, config)
    sysinfo = system.machine_info()[0]
    log.logger.info("Number of items %s" % len(data))
    parallel = res.calculate(parallel, data, sysinfo, config)
    log.logger.info(parallel)
    # print parallel
    # raise
    return parallel


def _check_items(data):
    """
    First check items are as expected
    """
    msg = ("\nYou can use ichwrapper.cluster.update_samples to add the config structure."
           "\nExample of list of samples to parallelize:"
           "\n[sample1, sample2, sample3]"
           "\nsample1=[{..., 'config':{'algorithm', ...}}]")
    assert isinstance(data,  list), "data needs to be a list"
    assert isinstance(data[0], list), "each item inside data needs to be like this [{}]"
    assert data[0][0]['config'], "each item inside data needs to have a config key with the info from galaxy/bcbio_system.yaml." + msg
    assert data[0][0]['config']['algorithm'], "config key inside item dict needs to have algorithm key." + msg


def send_job(fn, data, args, resources=None):
    """decide if send jobs with ipython or run locally"""
    utils.safe_makedir("checkpoint")
    _check_items(data)
    res = []
    dirs = {'work': os.path.abspath(os.getcwd())}
    config = data[0][0]['config']
    if not resources:
        resources = config_default
    step = resources['name']
    if 'mem' not in resources or 'cores' not in resources:
        raise ValueError("resources without mem or cores keys: %s" % resources)
    par = _calculate_resources(data, args, resources)
    # args.memory_per_job = resources['mem']
    # args.cores_per_job = resources['cores']
    # log.setup_log(args)
    log.logger.debug("doing %s" % step)
    if par['type'] == "ipython" and not is_done(step):
        with create(par, dirs, config) as view:
            for sample in data:
                res.append(view.apply_async(fn, sample[0], args))
            res = wait_until_complete(res)
        flag_done(step)
        return res
    for sample in data:
        res.append([fn(sample[0], args)])
    return res


def update_samples(data, resources, args):
    """
    Update algorithm dict with new cores set
    """
    if args.galaxy:
        system_config = args.galaxy
    else:
        system_config = os.path.join(_get_data_dir(), "galaxy", "bcbio_system.yaml")
    config = yaml.load(open(system_config))
    config['algorithm'] = {}

    new_data = []
    for sample in data:
        sample['config'] = config
        sample['config']['algorithm'] = resources
        new_data.append([sample])
    return new_data
