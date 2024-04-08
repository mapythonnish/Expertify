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
