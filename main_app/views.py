from django.shortcuts import render
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import action
# Create your views here.
from main_app.models import Client, Message, Mailing
from main_app.serializers import ClientSerializer, MailingSerializer, MessageSerializer


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class MailingViewSet(viewsets.ModelViewSet):
    queryset = Mailing.objects.all()
    serializer_class = MailingSerializer

    @action(detail=True, methods=['GET'])
    def get_id(self,request, pk=None):
        queryset_mailing = Mailing.objects.all()
        get_object_or_404(queryset_mailing, pk=pk)
        queryset = Message.objects.filter(mailing = pk).all()
        serializer = MessageSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['GET'])
    def get_mails(self,request):
        total_count = Mailing.objects.count()
        mailing = Mailing.objects.values('id')
        content = {'Total number of mailings': total_count,
                   'The number of messages sent': ''}
        result = {}
        for row in mailing:
            res = {'Total messages': 0, 'Sent':0,'No sent':0}
            mail = Message.objects.filter(mailing = row['id']).all()
            group_sent = mail.filter(status=Message.Status_Message.SENT).count()
            group_not_sent = mail.filter(status=Message.Status_Message.NOT_SENT).count()
            res['Total messages']=len(mail)
            res['Sent']=group_sent
            res['No sent']=group_not_sent
            result[row['id']]= res
        content['The number of messages sent'] = result
        return Response(content)