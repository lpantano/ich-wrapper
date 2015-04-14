

def myargs(parser):
    parser.add_argument("-n", "--num-jobs", type=int,
                        default=1, help="Number of concurrent jobs to process.")
    parser.add_argument("--cores-per-job", type=int,
                        default=1, help="Number of cores to use.")
    parser.add_argument("--memory-per-job", default=2, help="Memory in GB to reserve per job.")
    parser.add_argument("--timeout", default=15, help="Time to wait before giving up starting.")
    parser.add_argument("-s", "--scheduler", default=None, help="Type of scheduler to use.",
                        choices=["lsf", "slurm", "torque", "sge"])
    parser.add_argument("-r", "--resources", default=None, help="Extra scheduler resource flags.")
    parser.add_argument("-q", "--queue", default=None, help="Queue to submit jobs to.")
    parser.add_argument("-t", "--parallel", choices=["local", "ipython"], default="local",
                        help="Run in parallel on a local machine.")
    parser.add_argument("--local", action="store_true",
                        default=False, help="Run parallel locally")
    return parser
