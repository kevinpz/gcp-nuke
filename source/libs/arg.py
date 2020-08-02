"""
Manage arguments
"""

import argparse


def get_arguments():
    """
    Get the args used with the script


    :return: the args object
    """
    # Init argument parsing
    parser = argparse.ArgumentParser()

    parser.add_argument('-l', '--log-level',
                        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
                        default='INFO',
                        help='select log level'
                        )

    parser.add_argument('--project-id',
                        required=True,
                        help='GCP project ID'
                        )

    parser.add_argument('--dry-run',
                        action='store_true',
                        required=False,
                        help='Dry run mode'
                        )

    args = parser.parse_args()

    return args
