# utils.py

from django.core.mail import EmailMessage

class Util:
    @staticmethod
    def send_email(data):
        try:
            email = EmailMessage(
                subject=data['subject'],
                body=data['body'],
                to=[data['to_email']]
            )
            email.send()
            return True
        except Exception as e:
            print(str(e))
            return False
        
        
 
from fcm_django.models import FCMDevice
import logging

def send_notification_to_owner(owner_user, message):
    # Fetch the FCM device associated with the owner
    owner_fcm_device = FCMDevice.objects.filter(user=owner_user).first()

    if owner_fcm_device:
        # Send a push notification to the owner's device
        owner_fcm_device.send_message(title="New Expert Signup", body=message)
    else:
        # Handle the case when the owner's FCM device is not found
        logging.warning("Owner's FCM device not found. Notification not sent.")

 
# expert_app/utils.py

from django.contrib.auth.models import User
from .models import Owner

def find_owner(email):
    try:
        user = User.objects.get(email=email)
        owner = Owner.objects.get(user=user)
        return owner
    except User.DoesNotExist:
        return None
    except Owner.DoesNotExist:
        return None

 