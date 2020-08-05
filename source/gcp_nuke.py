"""
Main file to nuke everything in GCP
"""

from libs.arg import get_arguments
from libs.gcp_cleaner import GCPCleaner
from libs.logs import init_logs

if __name__ == '__main__':
    # Get the arguments
    args = get_arguments()
    # Init the logger
    init_logs(args.log_level)
    # Create the cleaner object
    gcp_cleaner = GCPCleaner(args.project_id, args.dry_run, args.yes)
    # Clean everything
    gcp_cleaner.delete_all()
