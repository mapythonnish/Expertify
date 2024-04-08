from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Expert
from .utils import send_notification_to_owner
import logging

@receiver(post_save, sender=Expert)
def send_notification_on_expert_signup(sender, instance, created, **kwargs):
    if created:
        message = f"New expert profile created: {instance.first_name} {instance.last_name}"
        owner = instance.owner
        if owner and owner.user:
            send_notification_to_owner(owner.user, message)
        else:
            # Log an error if owner or owner.user is None
            logging.error("Owner or owner user is None for Expert instance: %s", instance.id)

