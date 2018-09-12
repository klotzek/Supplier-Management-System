from django.core.management.base import BaseCommand, CommandError
from django.core.mail import send_mail
from datetime import datetime, timedelta
from django.utils import timezone, http
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
        
        tasks = Task.objects.filter(closed=False ) #gehe ueber alle aktiven Tasks und sammle die Piloten
        for task in tasks:
            if 'Overdue' in task.timely_status:
                pilot= task.pilot
                if not pilot in pilots:
                    pilots.append(pilot)    

        for pilot in pilots:
            mail_text ='Dear ' + task.pilot.firstname + ' '+ task.pilot.lastname + ','        
            mail_text += '\r\n'
            mail_text += '\r\n'
            tasks = Task.objects.filter(closed=False, pilot=pilot)
            for task in tasks:
                if 'Overdue' in task.timely_status:
                    mail_text += 'Task "' + task.task + '" overdue. Due date was: ' + str(task.due_date)
                    mail_text += '\r\n'
                    mail_text += 'https://'
                    url = 'sms.pmdm.de/SMS/task_details/due_date/' + str(task.project) + '/' + str(task.subproject) + '/' + str(task.pk)
                    url = http.urlquote(url)
                    mail_text += url
                    mail_text += '\r\n'
                    mail_text += ''
                    mail_text += '\r\n'
            subject = 'There are delayed tasks (' + str(Task.objects.filter(closed=False, pilot=pilot).count()) + ' pcs.)'
            send_mail(subject, mail_text, 'juergen.klotzek@nmb-minebea.com', [task.pilot.email, 'juergen.klotzek@nmb-minebea.com'])

