from django.db import models, IntegrityError
from users.models import NewUser, Consultant, Customer


class ApiMessage(models.Model):
    sender = models.ForeignKey(Consultant, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ['-timestamp']

    def save(self, *args, **kwargs):
        # Assurez-vous que le destinataire est le client associé à la commande
        if self.receiver != self.order.customer:
            raise IntegrityError("Le client doit être le destinataire du message")

        # Assurez-vous que le destinataire est un client du consultant
        self.receiver = self.sender.customers.filter(pk=self.order.customer.pk).first()
        if not self.receiver:
            raise IntegrityError("Le destinataire doit être un client du consultant")

        super().save(*args, **kwargs)
