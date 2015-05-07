import logbook
import logbook.queues
from bcbio import log
from bcbio.provenance.do import run as bcbio_run

LOG_NAME = "cluster-helper"
logger = logbook.Logger(LOG_NAME)
logger_cl = logbook.Logger(LOG_NAME + "-commands")
logger_stdout = logbook.Logger(LOG_NAME + "-stdout")


run = bcbio_run


def setup_log(config, parallel):
    parallel = log.create_base_logger(config, parallel)
    log.setup_local_logging(config, parallel)
