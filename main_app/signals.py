from django.db.models.signals import post_save
from django.db.models import Q
from django.dispatch import receiver

from main_app.models import Mailing, Message, Client
from main_app.tasks import send_message

@receiver(post_save, sender = Mailing, dispatch_uid = 'builder_task_on_mailing')
def builder_tasks_on_mailing(sender , instance , created , *args, **kwargs):
    if created:
        mail = Mailing.objects.get(pk=instance.id)
        clients = Client.objects.filter(Q(tag=mail.tag) | Q(operator_code=mail.operator_code))
        for client in clients:
            message=Message.objects.create(client= client.id, mailing = mail.id)
            if mail.send:
                send_message.apply_async((message.id, client.id, mail.id),expires = mail.end_date )
            else:
                 send_message.apply_async((message.id, client.id, mail.id),
                                         eta=mail.start_date, expires=mail.end_date)
                