import logbook
import logbook.queues
from bcbio.distributed import clargs
from bcbio import log

LOG_NAME = "cluster-helper"
logger = logbook.Logger(LOG_NAME)
logger_cl = logbook.Logger(LOG_NAME + "-commands")
logger_stdout = logbook.Logger(LOG_NAME + "-stdout")


def setup_log(args):
    parallel = clargs.to_parallel(args)
    parallel = log.create_base_logger({}, parallel)
    log.setup_local_logging({}, parallel)
