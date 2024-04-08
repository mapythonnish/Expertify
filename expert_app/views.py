from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Owner
from .serializers import OwnerSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

class MasterAdminLoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        master_admin_user = authenticate(username=username, password=password)

        if master_admin_user is not None:
            try:
                refresh = RefreshToken.for_user(master_admin_user)
                response_data = {
                    "username": username,
                    "tokens": {
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                    },
                }
                return Response(response_data, status=status.HTTP_200_OK)
            except Exception as e:
                return Response(
                    {"error": "Token generation failed"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
        else:
            return Response(
                {"error": "Authentication failed"}, status=status.HTTP_401_UNAUTHORIZED
            )

class OwnerCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Check if the user is a MasterAdmin
        if request.user.is_superuser:
            serializer = OwnerSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Owner account created successfully"}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)











from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from fcm_django.models import FCMDevice
from .serializers import OwnerSerializer 



class OwnerLoginAPIView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response(
                {"error": "Both email and password are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Check if the user with the given email exists
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"error": "Invalid email"}, status=status.HTTP_401_UNAUTHORIZED
            )

        # Check if the user is active and the password is correct
        if user.is_active and check_password(password, user.password):
            # Assuming your store owner model has a 'store_name' field
            owner = Owner.objects.get(user=user)
            store_name = owner.name

            refresh = RefreshToken.for_user(user)
            response_data = {
                "username": email,
                "owner": store_name,
                "tokens": {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
            }
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )





from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .serializers import SendPasswordResetEmailSerializer, PasswordChangeSerializer,PasswordResetSerializer
from rest_framework.permissions import IsAuthenticated


class PasswordChangeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PasswordChangeSerializer(data=request.data)
        if serializer.is_valid():
            old_password = serializer.validated_data['old_password']
            new_password = serializer.validated_data['new_password']
            user = request.user
            if user.check_password(old_password):
                user.set_password(new_password)
                user.save()
                return Response({'message': 'Password changed successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Old password is incorrect'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    

class SendPasswordResetEmailView(APIView):

    def post(self, request, format=None):
        serializer = SendPasswordResetEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Retrieve the encoded UID and reset token if available
        encoded_uid = serializer.validated_data.get('encoded_uid')
        reset_token = serializer.validated_data.get('reset_token')

        # Construct the response
        response_data = {"result": "Password Reset link sent. Please check your Email"}
        
        # Include encoded UID and reset token in the response if available
        if encoded_uid and reset_token:
            response_data["encoded_uid"] = encoded_uid
            response_data["reset_token"] = reset_token

        return Response(response_data, status=status.HTTP_200_OK)



class PasswordResetAPIView(APIView):
    def post(self, request, uidb64, token):
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.filter(pk=uid).first()
        if user and default_token_generator.check_token(user, token):
            serializer = PasswordResetSerializer(data=request.data)
            if serializer.is_valid():
                new_password = serializer.validated_data.get('new_password')
                confirm_password = serializer.validated_data.get('confirm_password')

                if new_password != confirm_password:
                    return Response({'error': 'New password and confirm password do not match.'}, status=status.HTTP_400_BAD_REQUEST)

                user.set_password(new_password)
                user.save()
                return Response({'message': 'Password reset successfully'}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'Invalid reset link'}, status=status.HTTP_400_BAD_REQUEST)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ExpertSignUpSerializer
from .models import Expert, Notification
from .notifications import send_notification_to_owner
from .models import Owner

class ExpertSignUpAPIView(APIView):
    def post(self, request):
        serializer = ExpertSignUpSerializer(data=request.data)
        if serializer.is_valid():
            expert = serializer.save()

            # Retrieve the owner with the primary key of 1
            try:
                owner = Owner.objects.get(pk=1)
            except Owner.DoesNotExist:
                return Response({"error": "Owner with the specified ID does not exist."}, status=status.HTTP_404_NOT_FOUND)

            # Create the notification message
            message = f"New expert profile created: {expert.first_name} {expert.last_name}"

            # Create a notification object
            notification = Notification.objects.create(owner=owner, message=message)

            # Send the notification to the owner
            send_notification_to_owner(owner.user, message)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)











            
   



# views.py
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
 


class ExpertLoginAPIView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        # Authenticate expert using email and password
        user = authenticate(request, username=email, password=password)

        if user is not None:
            # Generate tokens
            refresh = RefreshToken.for_user(user)
            response_data = {
                "email": email,
                "tokens": {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
            }
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            # Authentication failed
            return Response({"error": "Invalid email or password."}, status=status.HTTP_401_UNAUTHORIZED)







from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import ExpertProfileSerializer
from .models import Expert

class ExpertProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        expert = request.user.expert  # Assuming the authenticated user is an expert
        serializer = ExpertProfileSerializer(expert)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        expert = request.user.expert  # Assuming the authenticated user is an expert
        serializer = ExpertProfileSerializer(expert, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Notification
from .serializers import NotificationSerializer,ExpertPasswordChangeSerializer,ExpertSendPasswordResetEmailSerializer,ExpertPasswordResetSerializer

class OwnerNotificationAPIView(APIView):
    def get(self, request):
        notifications = Notification.objects.all()  # Fetch all notifications
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


class ExpertPasswordChangeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ExpertPasswordChangeSerializer(data=request.data)
        if serializer.is_valid():
            old_password = serializer.validated_data['old_password']
            new_password = serializer.validated_data['new_password']
            user = request.user
            if user.check_password(old_password):
                user.set_password(new_password)
                user.save()
                return Response({'message': 'Password changed successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Old password is incorrect'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    

class ExpertSendPasswordResetEmailView(APIView):

    def post(self, request, format=None):
        serializer = ExpertSendPasswordResetEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Retrieve the encoded UID and reset token if available
        encoded_uid = serializer.validated_data.get('encoded_uid')
        reset_token = serializer.validated_data.get('reset_token')

        # Construct the response
        response_data = {"result": "Password Reset link sent. Please check your Email"}
        
        # Include encoded UID and reset token in the response if available
        if encoded_uid and reset_token:
            response_data["encoded_uid"] = encoded_uid
            response_data["reset_token"] = reset_token

        return Response(response_data, status=status.HTTP_200_OK)



class ExpertPasswordResetAPIView(APIView):
    def post(self, request, uidb64, token):
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.filter(pk=uid).first()
        if user and default_token_generator.check_token(user, token):
            serializer = ExpertPasswordResetSerializer(data=request.data)
            if serializer.is_valid():
                new_password = serializer.validated_data.get('new_password')
                confirm_password = serializer.validated_data.get('confirm_password')

                if new_password != confirm_password:
                    return Response({'error': 'New password and confirm password do not match.'}, status=status.HTTP_400_BAD_REQUEST)

                user.set_password(new_password)
                user.save()
                return Response({'message': 'Password reset successfully'}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'Invalid reset link'}, status=status.HTTP_400_BAD_REQUEST)
    
    
# views.py

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Notification

class NotificationDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, notification_id):
        notification = get_object_or_404(Notification, pk=notification_id)
        
        # Check if the logged-in user is the owner of the notification
        if notification.owner == request.user:
            notification.delete()  # Delete the notification
            return Response({"message": "Notification deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"error": "You do not have permission to delete this notification."}, status=status.HTTP_403_FORBIDDEN)

