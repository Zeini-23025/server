from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from django.contrib.auth import get_user_model, logout
from .serializers import UserSerializer, RegisterSerializer, LoginSerializer
from .permissions import IsAdmin, IsUser, IsAuthenticatedUser
from django.utils.crypto import get_random_string
from django.utils import timezone
from datetime import timedelta
from .models import OTP
from getionEmploi.utils import envoyer_email

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = []  

class LoginView(APIView):
    permission_classes = []
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': UserSerializer(user).data,
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh),
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class LogoutView(APIView):
    permission_classes = [IsAuthenticatedUser]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh_token")
            if not refresh_token:
                return Response({"error": "Refresh token requis"}, status=status.HTTP_400_BAD_REQUEST)

            token = RefreshToken(refresh_token)
            token.blacklist()

            logout(request) 

            return Response({"message": "Déconnecté avec succès"}, status=status.HTTP_200_OK)

        except Exception:
            return Response({"error": "Token invalide ou déjà expiré"}, status=status.HTTP_400_BAD_REQUEST)


class CheckAuthView(APIView):
    def post(self, request):
        access_token = request.data.get("access_token")
        refresh_token = request.data.get("refresh_token")

        if not access_token or not refresh_token:
            return Response({"error": "Tokens requis"}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            access = AccessToken(access_token)
            user = User.objects.get(id=access["user_id"])
            
            return Response({"message": "Utilisateur authentifié", "user": {"email": user.email, "role": user.role}}, status=status.HTTP_200_OK)
        
        except Exception:
            try:
                refresh = RefreshToken(refresh_token)
                new_access_token = str(refresh.access_token)
                return Response({"message": "Token rafraîchi", "access_token": new_access_token ,"refresh_token": str(refresh) }, status=status.HTTP_200_OK)
            except Exception:
                return Response({"error": "Refresh token invalide"}, status=status.HTTP_401_UNAUTHORIZED)

class RequestUpdatePasswordView(APIView):
    def post(self, request):
        email = request.data.get("email")
        if not email:
            return Response({"error": "Email requis"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
            otp_code = get_random_string(6, allowed_chars="0123456789")
            OTP.objects.create(email=email, code=otp_code)
            envoyer_email(email, "Votre code OTP", f"Votre code OTP est : {otp_code}")
            return Response({"message": "OTP envoyé par email","email":email}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "Utilisateur non trouvé"}, status=status.HTTP_404_NOT_FOUND)

class VerifyOTPUpdatePasswordView(APIView):
    def post(self, request):
        otp_code = request.data.get("otp_code")
        new_password = request.data.get("new_password")

        if not otp_code or not new_password:
            return Response({"error": "Code OTP et nouveau mot de passe requis"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            otp = OTP.objects.get(code=otp_code, is_used=False)
            if timezone.now() > otp.created_at + timedelta(minutes=5):
                return Response({"error": "OTP expiré"}, status=status.HTTP_400_BAD_REQUEST)

            user = User.objects.get(email=otp.email)
            user.set_password(new_password)
            user.save()
            otp.is_used = True
            otp.save()

            return Response({"message": "Mot de passe mis à jour"}, status=status.HTTP_200_OK)

        except OTP.DoesNotExist:
            return Response({"error": "Code OTP invalide"}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"error": "Utilisateur introuvable"}, status=status.HTTP_404_NOT_FOUND)


class UpdateEmailRequestView(APIView):
    permission_classes = [IsAuthenticatedUser]

    def post(self, request):
        old_email = request.user.email
        new_email = request.data.get("new_email")

        if not new_email:
            return Response({"error": "Le nouvel email est requis"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=new_email).exists():
            return Response({"error": "Cet email est déjà utilisé"}, status=status.HTTP_400_BAD_REQUEST)

        otp_code = get_random_string(6, allowed_chars="0123456789")
        OTP.objects.create(email=old_email, code=otp_code)
        
        envoyer_email(old_email, "Code de vérification", f"Votre code OTP pour changer d'email est : {otp_code}")

        return Response({"message": "OTP envoyé à l'ancien email","old_email": old_email,"new_email":new_email,}, status=status.HTTP_200_OK)

class VerifyOTPUpdateEmailView(APIView):
    permission_classes = [IsAuthenticatedUser]

    def post(self, request):
        old_email = request.user.email
        otp_code = request.data.get("otp_code")
        new_email = request.data.get("new_email")

        if not otp_code or not new_email:
            return Response({"error": "Code OTP et nouvel email requis"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            otp = OTP.objects.get(email=old_email, code=otp_code, is_used=False)

            if timezone.now() > otp.created_at + timedelta(minutes=5):
                return Response({"error": "OTP expiré"}, status=status.HTTP_400_BAD_REQUEST)

            if User.objects.filter(email=new_email).exists():
                return Response({"error": "Cet email est déjà utilisé"}, status=status.HTTP_400_BAD_REQUEST)

            user = request.user
            user.email = new_email
            user.save()

            otp.is_used = True
            otp.save()

            return Response({"message": "Email mis à jour avec succès"}, status=status.HTTP_200_OK)

        except OTP.DoesNotExist:
            return Response({"error": "Code OTP invalide"}, status=status.HTTP_400_BAD_REQUEST)

class AdminOnlyView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        return Response({"message": "Bienvenue, Admin!"}, status=status.HTTP_200_OK)

class UserOnlyView(APIView):
    permission_classes = [IsUser]

    def get(self, request):
        return Response({"message": "Bienvenue, Utilisateur!"}, status=status.HTTP_200_OK)
