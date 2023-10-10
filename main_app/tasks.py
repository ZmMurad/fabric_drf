import os
import requests
from celery.utils.log import get_task_logger

from main_app.models import Message, Client, Mailing
from mailing_service.celery import app

logger= get_task_logger(__name__)

URL=os.getenv("URL")
TOKEN = os.getenv("TOKEN")

@app.task(bind=True, retry_backoff = True)
def send_message(self,mesasge_id, cliend_id, mailing_id, url=URL, token=TOKEN):
    mail = Mailing.objects.get(pk=mailing_id)
    cliend= Client.objects.get(pk=cliend_id)
    if mail and cliend:
        if mail.send:
            data = {'id':mesasge_id, 'phone':cliend.phone_number, 'text':mail.text}
            header = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            }
            try:
                response = requests.post(url, data,headers=header)
                if response.ok:
                    logger.info(f"Message {mesasge_id} send successfully")
                    Message.objects.filter(pk=mesasge_id).update(status=Message.Status_Message.SENT)
            except Exception as exc:
                logger.error(f"Message {mesasge_id} ocured by error")
                raise self.retry(exc=exc)
        else:
            logger.info(f'Mailig time has been expired {mesasge_id}')
            return self.retry(eta=mail.start_date, expires=mail.end_date)
    else:
        logger.info('Mailing or Client is empty')
