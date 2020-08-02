"""
Main file to nuke everything in GCP
"""
import logging
import os
import sys

from google.cloud import storage

from libs.arg import get_arguments
from libs.logs import init_logs


class GCPCleaner:
    """
    GCP Cleaner class
    """
    def __init__(self, project_id, dry_run):
        """
        Init the GCP cleaner class

        :param project_id: GCP project id
        :param dry_run: dry run mode
        """
        self.dry_run = dry_run
        self.project_id = project_id
        self._check_auth()
        self._validate_deletion()

    def _validate_deletion(self):
        """
        Just to be sure we want to delete everything
        """
        # Check if we're in dry run mode
        if self.dry_run:
            logging.info("Dry run mode, nothing will be deleted")
        else:
            # Otherwise be sure the user want to delete everything in the project
            logging.critical(f"/!\ Everything will be deleted in the Project ID = {self.project_id}!\n"  # pylint: disable=anomalous-backslash-in-string
                             f"Are you sure? (yes/no)")
            answer = input()
            valid_answer = ["yes", "y"]
            # If the user answer is not in the valid_answer list, just exit
            if answer.lower() not in valid_answer:
                logging.info(f"Exiting because of user input {answer}")
                sys.exit(0)

    def _check_auth(self):
        """
        Check if the auth is working
        """
        logging.info(f"Checking auth for Project ID = {self.project_id}")
        # Put the project id as env variable, so all python call can use it
        os.environ['GCLOUD_PROJECT'] = self.project_id

        # Check if we can list the bucket, so we have access to the project
        try:
            storage_client = storage.Client()
            list(storage_client.list_buckets())
        except:  # pylint: disable=bare-except
            logging.error("Invalid auth provided")
            sys.exit(1)

        logging.info("Auth successfully validated")

    def delete_all(self):
        """
        Delete all the GCP resources
        """
        # Clean all ressources
        logging.info("Deleting all GCP resources")
        self.delete_storage()

    def delete_storage(self):
        """
        Delete all the buckets
        """
        logging.info("Deleting Google Storage buckets")
        storage_client = storage.Client()
        bucket_list = storage_client.list_buckets()
        for bucket in bucket_list:
            logging.info(f"[Storage] Deleting bucket {bucket.name}")
            if not self.dry_run:
                bucket.delete(force=True)
        logging.info("[Storage] All buckets are deleted")


if __name__ == '__main__':
    # Get the arguments
    args = get_arguments()
    # Init the logger
    init_logs(args.log_level)
    # Create the cleaner object
    gcp_cleaner = GCPCleaner(args.project_id, args.dry_run)
    # Clean everything
    gcp_cleaner.delete_all()
