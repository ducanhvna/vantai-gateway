from apscheduler.schedulers.background import BackgroundScheduler
from .report_update import export_report

def start():
    scheduler = BackgroundScheduler(daemon=False)
    # scheduler.add_job(post_inspection, 'interval', seconds=36000)
    # scheduler.add_job(update_report, 'interval', seconds=600)
    scheduler.add_job(export_report, 'interval', seconds=20)
    # scheduler.add_job(export_report_only, 'interval', seconds=369)
    # scheduler.add_job(export_report_al_cl_next_month, 'interval', seconds=600)
    # scheduler.add_job(export_report_ho, 'interval', seconds=427)
    # scheduler.add_job(export_report_department, 'interval', seconds=220)
    # scheduler.add_job(export_report_next_month, 'interval', seconds=1000)
    # scheduler.add_job(collect_attendance, 'interval', seconds=12000)
    scheduler.start()
