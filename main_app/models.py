from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone
from django.core.exceptions import ValidationError
import pytz

# Create your models here.


def check_timezone(tz):
    if tz not in pytz.all_timezones:
        raise ValidationError(f"{tz} the time zone is not correct", params={"tz": tz})


def check_phone_number(number):
    return RegexValidator(
        regex=r"^7\d{10}$",
        message="Incorrect phone number, please provide phone number in format 7XXXXXXXXXX (X - its number 0-9)",
    )


def check_code_operator(code):
    return RegexValidator(regex=r"^\d{3}$", message="The code must be 3 digits")


class Message(models.Model):
    class Status_Message(models.TextChoices):
        SENT = ("SENT", "SENT")
        NOT_SENT = ("NOT SENT", "NOT SENT")

    date_sent = models.DateTimeField(verbose_name="Time of send", auto_now=True)
    status = models.CharField(
        max_length=8,
        choices=Status_Message.choices,
        verbose_name="Status of message",
        default=Status_Message.NOT_SENT,
    )
    client = models.ForeignKey("Client", on_delete=models.SET_NULL, null=True)
    mailing = models.ForeignKey("Mailing", on_delete=models.CASCADE, null=True)

    def __str__(self) -> str:
        return f"Message: {self.id} \nSent Time: {self.date_sent} \nStatus: {self.status} \nClient: {self.client} \nMailing: {self.mailing}"

    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Messages"


class Mailing(models.Model):
    start_date = models.DateTimeField(verbose_name="Mailing start date")
    end_date = models.DateTimeField(verbose_name="Mailing end date")
    text = models.TextField(verbose_name="Text mailing", max_length=1000)
    tag = models.CharField(verbose_name="Search Tag", max_length=30, blank=True)
    operator_code = models.CharField(
        verbose_name="Operator Code",
        max_length=3,
        validators=[check_code_operator],
        blank=True,
    )

    @property
    def send(self):
        now = timezone.now()
        if self.start_date <= now <= self.end_date:
            return True
        return False

    def __str__(self) -> str:
        return f"Mailing: {self.id} \nStart: {self.start_date} \nEnd: {self.end_date} \nText: {self.text} \nTag: {self.tag} \nOperator code: {self.operator_code}"

    class Meta:
        verbose_name = "Mailing"
        verbose_name_plural = "Mailings"


class Client(models.Model):
    TIMEZONES = [(tz,tz) for tz in pytz.all_timezones]
    phone_number = models.CharField(
        verbose_name="Phone Number",
        max_length=11,
        unique=True,
        validators=[check_phone_number],
    )
    timezone = models.CharField(
        verbose_name="Time zone",
        max_length=50,
        choices=TIMEZONES,
        default="UTC",
        validators=[check_timezone],
    )
    operator_code = models.CharField(verbose_name="Operator Code", max_length=3)
    tag = models.CharField(verbose_name="Search Tag", max_length=30)

    def save(self, *args, **kwargs):
        self.operator_code = str(self.phone_number)[1:4]
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"Client: {self.id} \nPhone Number: {self.phone_number} \nTimezone: {self.timezone} \nOperator Code: {self.operator_code} \nTag: {self.tag}"

    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"
