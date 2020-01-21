from django.db import models
import uuid

class Sms(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content = models.CharField(max_length=256)
    date_composed = models.DateTimeField('Date Composed',auto_now=True, auto_now_add=False)
    date_sent = models.DateTimeField('Date Sent',auto_now=False, auto_now_add=False)
    sent_to = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'SMS'
        verbose_name_plural = 'SMS'
    
    def __str__(self):
        return str(self.uuid)
    
    # def get_absolute_url(self):
    #     return reverse("model_detail", kwargs={"pk": self.pk})
    
