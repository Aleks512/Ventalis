from django.db import models, IntegrityError
from users.models import NewUser, Consultant, Customer


class ApiMessage(models.Model):
    sender = models.ForeignKey(Consultant, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"De {self.sender} - de chez Ventalis à {self.receiver}"


class ApiMessageWrittenByCustomer(models.Model):
    sender = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(Consultant, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"De {self.sender} - au consultant {self.receiver} de chez Ventalis"
