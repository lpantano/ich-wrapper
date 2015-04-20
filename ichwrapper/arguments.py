

def myargs(parser):
    parser.add_argument("-n", "--numcores", type=int,
                        default=1, help="Number of concurrent jobs to process.")
    parser.add_argument("-c", "--cores-per-job", type=int,
                        default=1, help="Number of cores to use.")
    parser.add_argument("-m", "--memory-per-job", default=2, help="Memory in GB to reserve per job.")
    parser.add_argument("--timeout", default=15, help="Time to wait before giving up starting.")
    parser.add_argument("--retries", default=0, type=int,
                        help=("Number of retries of failed tasks during "
                              "distributed processing. Default 0 "
                              "(no retries)"))
    parser.add_argument("-s", "--scheduler", help="Type of scheduler to use.",
                        choices=["lsf", "slurm", "torque", "sge", "pbspro"])
    parser.add_argument("-r", "--resources", help="Extra scheduler resource flags.", default=[], action="append")
    parser.add_argument("-q", "--queue", help="Queue to submit jobs to.")
    parser.add_argument("-p", "--tag", help="Tag name to label jobs on the cluster", default="bcb-prep")
    parser.add_argument("-t", "--paralleltype",
                        choices=["local", "ipython"],
                        default="local", help="Run with iptyhon")
    parser.add_argument("--local", default=False, action='store_true', help="Run cluster locally")

    return parser
