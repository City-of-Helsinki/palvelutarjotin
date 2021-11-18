from datetime import datetime

from reports.models import EnrolmentReport


def sync_enrolment_reports(hydrate_linkedevents_event=True, sync_from: datetime = None):
    """
    Synchronize the enrolemnts report table with enrolments table:
    1. Update the unsynced enrolment report instances.
    2. Create the missing enrolment report instances.
    NOTE: This function fetches data
    for each event of the enrolments from LinkedEvents API
    """
    sync_from = sync_from or EnrolmentReport.objects.latest_sync()
    if EnrolmentReport.objects.exists():
        EnrolmentReport.objects.update_unsynced(
            sync_from=sync_from, hydrate_linkedevents_event=hydrate_linkedevents_event
        )
    EnrolmentReport.objects.create_missing(sync_from=sync_from)
