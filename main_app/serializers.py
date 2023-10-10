from rest_framework import serializers
from main_app.models import Client, Message, Mailing

class MailingSerializer(serializers.ModelSerializer):
    class Meta:
        model=Mailing
        fields="__all__"

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model=Client
        fields="__all__"


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model=Message
        fields="__all__"