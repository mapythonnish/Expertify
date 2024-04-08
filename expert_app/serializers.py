from rest_framework import serializers
from .models import Expert,Owner

class OwnerSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    confirm_password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = Owner
        fields = ('email', 'password', 'confirm_password', 'name', 'address', 'phone_number')

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')   
        password = validated_data.pop('password')

         
        user = User.objects.create_user(
            username=validated_data['email'],  
            email=validated_data['email'],
            password=password
        )

         
        owner = Owner.objects.create(user=user, **validated_data)
        return owner

class ExpertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expert
        fields = ('first_name','last_name','email','phone_number','expert_category','subcategory')
        read_only_fields = ['user']

class SendPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    
# serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_bytes, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework import serializers
from .utils import Util

class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

class SendPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)

    def validate(self, attrs):
        email = attrs.get("email")
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = PasswordResetTokenGenerator().make_token(user)
            link = f"http://localhost:/api/user/reset/{uid}/{token}"
            # Send Email
            body = f"Click the following link to reset your password: {link}"
            data = {"subject": "Reset Your Password", "body": body, "to_email": user.email}
            Util.send_email(data)  # You need to implement the Util class for sending emails
            return attrs
        else:
            raise serializers.ValidationError("You are not a registered user")

from rest_framework import serializers

class PasswordResetSerializer(serializers.Serializer):
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

 

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Expert, Certification, Owner
from .notifications import send_notification_to_owner

class ExpertSignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    certifications_upload = serializers.ListField(child=serializers.FileField(max_length=100000, allow_empty_file=False), write_only=True, required=False)
    
    class Meta:
        model = Expert
        fields = ['first_name', 'last_name', 'email', 'overview', 'phone_number', 'alternate_phone_number', 
                  'gender', 'city', 'languages_spoken', 
                  'class_location', 'full_address', 'time_slots_available', 
                  'expert_category', 'total_experience', 
                  'certifications', 'fees', 'certifications_upload',  
                  'insta_id', 'fb_id', 'pincode', 'password']

    def create(self, validated_data):
        # Remove 'password' from validated_data
        password = validated_data.pop('password')

        # Create user
        user = User.objects.create_user(
            username=validated_data['email'],  # Set username as email
            email=validated_data['email'],
            password=password  # Use the provided password
        )

        # Ensure the user has an associated owner
        owner = Owner.objects.filter(user=user).first()  # Retrieve the owner associated with the user

        # Handle certifications_upload
        certifications_upload = validated_data.pop('certifications_upload', [])
        expert = Expert.objects.create(user=user, owner=owner, **validated_data)
        
        # Message for notification
        message = f"New expert profile created: {expert.first_name} {expert.last_name}"

        # Send notification to owner if owner exists
        if owner:
            send_notification_to_owner(owner.user, message)

        for certification in certifications_upload:
            Certification.objects.create(expert=expert, file=certification)

        return expert





from rest_framework import serializers
from .models import Expert

class ExpertProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expert
        fields = ['first_name', 'last_name', 'overview', 'phone_number', 'alternate_phone_number', 'emergency_contact_name']


from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'  # Adjust fields as needed



from rest_framework import serializers

class ExpertPasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate(self, data):
        old_password = data.get('old_password')
        new_password = data.get('new_password')

        # Add custom validation logic here if needed
        # For example, you might want to enforce password complexity rules

        return data

class ExpertSendPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)

    def validate(self, attrs):
        email = attrs.get("email")
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = PasswordResetTokenGenerator().make_token(user)
            link = f"http://localhost:/api/user/reset/{uid}/{token}"
            # Send Email
            body = f"Click the following link to reset your password: {link}"
            data = {"subject": "Reset Your Password", "body": body, "to_email": user.email}
            Util.send_email(data)  # You need to implement the Util class for sending emails
            return attrs
        else:
            raise serializers.ValidationError("You are not a registered user")
        
from rest_framework import serializers

class ExpertPasswordResetSerializer(serializers.Serializer):
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)        
        