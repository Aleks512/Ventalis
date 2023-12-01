from django.db import models


class Message(models.Model):
    sender = models.ForeignKey('users.NewUser', on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey('users.NewUser', on_delete=models.CASCADE, related_name='received_messages')
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    def __str__(self):
        return f"Message from {self.sender} to {self.recipient} at {self.timestamp}"


from django.db import models

# Create your models here.
