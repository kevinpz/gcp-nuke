"""
Lib to clean GCP
"""
import logging
import os
import sys

from google.cloud import storage
import googleapiclient.discovery


class GCPCleaner:
    """
    GCP Cleaner class
    """

    def __init__(self, project_id, dry_run, assume_yes):
        """
        Init the GCP cleaner class

        :param project_id: GCP project id
        :param dry_run: dry run mode
        :param yes: dry run mode
        """
        self.dry_run = dry_run
        self.project_id = project_id
        self._check_auth()
        if not assume_yes:
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
            logging.critical(
                f"/!\ Everything will be deleted in the Project ID = {self.project_id}!\n"
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
        except:
            logging.error("Invalid auth provided")
            sys.exit(1)

        logging.info("Auth successfully validated")

    def delete_all(self):
        """
        Delete all the GCP resources
        """
        # Clean all ressources
        logging.info("Deleting all GCP resources")
        #self.delete_storage()
        #self.delete_compute_instance()
        self.delete_managed_instance_group()
        self.delete_unmanaged_instance_group()

    def delete_storage(self):
        """
        Delete all the buckets
        """
        logging.info("Deleting Google Storage buckets")
        # Init storage client
        storage_client = storage.Client()
        # Get the list of all buckets
        bucket_list = storage_client.list_buckets()
        # Delete each bucket
        for bucket in bucket_list:
            logging.info(f"[Storage] Deleting bucket {bucket.name}")
            if not self.dry_run:
                res = bucket.delete(force=True)
        logging.info("[Storage] All buckets are deleted")

    def delete_compute_instance(self):
        """
        Delete all the GCE instances
        """
        logging.info("Deleting Google Instances")
        # Init compute client
        compute = googleapiclient.discovery.build('compute', 'v1', cache_discovery=False)
        # Get the list of instances in all the zones
        instance_list = compute.instances().aggregatedList(project=self.project_id).execute()
        # For each zone
        for zone in instance_list['items']:
            # Check if we have instances
            if 'instances' in instance_list['items'][zone]:
                # For each instances
                # TODO: check instance status
                for instance in instance_list['items'][zone]['instances']:
                    # Get the zone name in the right format
                    zone_name = zone.split('/')[1]
                    logging.info(f"[Storage] Deleting instance {instance['name']} in zone {zone_name}")
                    if not self.dry_run:
                        compute.instances().delete(project=self.project_id, zone=zone_name,
                                                   instance=instance['name']).execute()

    def delete_unmanaged_instance_group(self):
        """
        Delete the unmanaged instance group
        """
        logging.info("Deleting Unmanaged Instance Group")
        # Init compute client
        compute = googleapiclient.discovery.build('compute', 'v1', cache_discovery=False)
        # Get the list of uig in all the zones
        uig_list = compute.instanceGroups().aggregatedList(project=self.project_id).execute()
        # For each zone
        for zone in uig_list['items']:
            # Check if we have UIG
            if 'instanceGroups' in uig_list['items'][zone]:
                # For each instances
                # TODO: check uig status
                for uig in uig_list['items'][zone]['instanceGroups']:
                    # Get the zone name in the right format
                    zone_name = zone.split('/')[1]
                    logging.info(f"[Storage] Deleting UIG {uig['name']} in zone {zone_name}")
                    if not self.dry_run:
                        compute.instanceGroups().delete(project=self.project_id, zone=zone_name,
                                                        instanceGroup=uig['name']).execute()

    def delete_managed_instance_group(self):
        """
        Delete the managed instance group
        """
        logging.info("Deleting Managed Instance Group")
        # Init compute client
        compute = googleapiclient.discovery.build('compute', 'v1', cache_discovery=False)
        # Get the list of uig in all the zones
        mig_list = compute.instanceGroupManagers().aggregatedList(project=self.project_id).execute()
        # For each zone
        for zone in mig_list['items']:
            # Check if we have UIG
            if 'instanceGroupManagers' in mig_list['items'][zone]:
                # For each instances
                for mig in mig_list['items'][zone]['instanceGroupManagers']:
                    # TODO: check instance status
                    # Get the zone name in the right format
                    zone_name = zone.split('/')[1]
                    logging.info(f"[Storage] Deleting MIG {mig['name']} in zone {zone_name}")
                    if not self.dry_run:
                        compute.instanceGroupManagers().delete(project=self.project_id, zone=zone_name,
                                                               instanceGroupManager=mig['name']).execute()


