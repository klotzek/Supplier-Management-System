from django.core.management.base import BaseCommand, CommandError
from django.core.mail import send_mail
from datetime import datetime, timedelta
from django.utils import timezone
from SMS.models import Task


class Command(BaseCommand):
    args = ''
    help = 'Nightly tasks'

    def handle(self, *args, **options):
        # do something here
        subject=''
        mail_text=''
        i=0
        pilots = []
        tasks = Task.objects.filter(closed=False ) #gehe über alle aktiven Tasks und sammle die Piloten
        for task in tasks:
            if 'Overdue' in task.timely_status:
                pilot= task.pilot
                if not pilot in pilots:
                    pilots.append(pilot)    

        for pilot in pilots:
            mail_text =''        
            tasks = Task.objects.filter(closed=False, pilot=pilot)
            for task in tasks:
                if 'Overdue' in task.timely_status:
                    mail_text += 'Dear ' + task.pilot + ','
                    mail_text += '\r\n'
                    mail_text += 'Task "' + task.task + '" overdue. Due date was: ' + str(task.due_date)
                    mail_text += '\r\n'
                    mail_text += 'http://localhost:8000/SMS/task_details/due_date/' + str(task.project) + '/' + str(task.subproject) + '/' + str(task.pk)
                    mail_text += '\r\n'
                    mail_text += ''
                    mail_text += '\r\n'
            subject = 'There are delayed tasks (' + str(Task.objects.filter(closed=False, pilot=pilot).count()) + ' pcs.)'
            send_mail(subject, mail_text, 'juergen.klotzek@nmb-minebea.com', (pilot, 'juergen.klotzek@nmb-minebea.com'))

#         print (pilots)
#         subject = pilots
#         subject = task.project
#         mail_text = 'Overdue: ' + task.task + ' due date was: ' + str(task.due_date)
#         send_mail(subject, 'mail_text', 'juergen.klotzek@nmb-minebea.com', ('juergen.klotzek@nmb-minebea.com',))
