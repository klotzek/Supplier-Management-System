import pdb
from django.core.management.base import BaseCommand, CommandError
from django.core.mail import send_mail
from datetime import datetime, timedelta
from django.utils import timezone, http
from SMS.models import Task, UserProfile


class Command(BaseCommand):
    args = ''
    help = 'Nightly tasks'

    def handle(self, *args, **options):
        # do something here
        subject=''
        mail_text=''
        i=0
        pilots = []
        
        tasks = Task.objects.filter(closed=False, type = 'TASK' ) #gehe ueber alle aktiven Tasks und sammle die Piloten
        for task in tasks:
            if 'Overdue' in task.timely_status:
                pilot= task.pilot
                if not pilot in pilots:
                    pilots.append(pilot)    

        for pilot in pilots:
            receiver = Task.objects.filter(closed=False, pilot=pilot, type = 'TASK').first()
#             pdb.set_trace()
            mail_text ='Dear ' + receiver.pilot.firstname + ' '+ receiver.pilot.lastname + ','        
            mail_text += '\r\n'
            mail_text += '\r\n'
            tasks = Task.objects.filter(closed=False, pilot=pilot, type = 'TASK')
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
#             pdb.set_trace()
            subject = 'There are delayed tasks (' + str(Task.objects.filter(closed=False, pilot=pilot, type='TASK').count()) + ' pcs.)'
            send_mail(subject, mail_text, 'juergen.klotzek@nmb-minebea.com', [task.pilot.email, 'juergen.klotzek@nmb-minebea.com'])
#             send_mail(subject, mail_text, 'juergen.klotzek@nmb-minebea.com', [ 'juergen.klotzek@nmb-minebea.com', 'juergen.klotzek@nmb-minebea.com'])

