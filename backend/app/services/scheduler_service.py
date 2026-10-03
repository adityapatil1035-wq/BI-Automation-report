import os
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from app.services.pdf_report_generator import generate_pdf_report
from app.services.excel_report_generator import generate_excel_report
from app.services.email_service import send_report_email

scheduler = BackgroundScheduler()

def run_scheduled_report_job(
    schedule_id: int,
    title: str,
    file_path: str,
    recipients_str: str,
    format_type: str = "PDF"
):
    print(f"[SCHEDULER JOB] Executing scheduled report #{schedule_id}: '{title}' at {datetime.now()}")
    recipients = [r.strip() for r in recipients_str.split(",") if r.strip()]
    
    timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    export_dir = os.path.abspath("./exports")
    os.makedirs(export_dir, exist_ok=True)
    
    attachments = []
    
    if format_type in ["PDF", "Both"]:
        pdf_path = os.path.join(export_dir, f"report_{schedule_id}_{timestamp_str}.pdf")
        generate_pdf_report(file_path, pdf_path, report_title=title)
        attachments.append(pdf_path)
        
    if format_type in ["Excel", "Both"]:
        excel_path = os.path.join(export_dir, f"report_{schedule_id}_{timestamp_str}.xlsx")
        generate_excel_report(file_path, excel_path)
        attachments.append(excel_path)

    body_html = f"""
    <div style="font-family: Arial, sans-serif; max-width: 600px; padding: 20px; border: 1px solid #E2E8F0; border-radius: 8px;">
        <h2 style="color: #1E293B;">Automated Business Intelligence Report</h2>
        <p style="color: #475569;">Hello,</p>
        <p style="color: #475569;">Your scheduled report <strong>{title}</strong> has been generated successfully.</p>
        <div style="background-color: #F8FAFC; padding: 15px; border-left: 4px solid #2563EB; margin: 15px 0;">
            <p style="margin: 0; font-weight: bold; color: #1E293B;">Report Overview:</p>
            <p style="margin: 5px 0 0 0; color: #64748B;">Generated: {datetime.now().strftime('%d %B %Y, %I:%M %p')}</p>
            <p style="margin: 5px 0 0 0; color: #64748B;">Format: {format_type}</p>
        </div>
        <p style="color: #475569;">Please find your executive report attached to this email.</p>
        <p style="color: #94A3B8; font-size: 12px; margin-top: 20px;">Sent automatically by AI BI Reporting Platform.</p>
    </div>
    """

    send_report_email(
        recipients=recipients,
        subject=f"{title} — {datetime.now().strftime('%d %B %Y')}",
        body_html=body_html,
        attachment_paths=attachments
    )

def start_scheduler():
    if not scheduler.running:
        scheduler.start()
        print("[SCHEDULER] Background Report Scheduler started.")

def shutdown_scheduler():
    if scheduler.running:
        scheduler.shutdown()
        print("[SCHEDULER] Background Report Scheduler stopped.")
