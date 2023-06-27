from functools import partial
from rest_framework import permissions
from .models import Session, Dean, Student
from .serializers import SessionSerializer, StudentSerializer, DeanSerializer
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
# Create your views here.


class AvailableSessions(generics.ListCreateAPIView):
    """
    List all available sessions, or book a new session.
    """
    authentication_classes = (SessionAuthentication,
                              BasicAuthentication, TokenAuthentication)
    queryset = Session.objects.all().order_by('time')
    serializer_class = SessionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def patch(self, request, id=None):
        session = Session.objects.get(available=True)
        serializer = SessionSerializer(
            session, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "Success", "data": serializer.data})
        else:
            return Response({"status": "Error", "data": serializer.errors})


class Students(generics.ListCreateAPIView):
    """
    List all available sessions, or book a new session.
    """
    authentication_classes = (SessionAuthentication,
                              BasicAuthentication, TokenAuthentication)
    queryset = Student.objects.all().order_by('id')
    serializer_class = StudentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def patch(self, request, id=None):
        session = Session.objects.get(id=id)
        serializer = SessionSerializer(
            session, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "Success", "data": serializer.data})
        else:
            return Response({"status": "Error", "data": serializer.errors})


class Dean(generics.ListCreateAPIView):
    """
    List all available deans.
    """
    authentication_classes = (SessionAuthentication,
                              BasicAuthentication, TokenAuthentication)
    queryset = Dean.objects.all().order_by('id')
    serializer_class = DeanSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def patch(self, request, id=None):
        session = Session.objects.get(id=id)
        serializer = SessionSerializer(
            session, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "Success", "data": serializer.data})
        else:
            return Response({"status": "Error", "data": serializer.errors})


class SessionDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a session record.
    """
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = (SessionAuthentication,
                              BasicAuthentication, TokenAuthentication)
    queryset = Session.objects.all()
    serializer_class = SessionSerializer


class DeanSessions(generics.ListAPIView):
    """
    List all available sessions, or book a new session.
    """
    authentication_classes = (SessionAuthentication,
                              BasicAuthentication, TokenAuthentication)
    queryset = Session.objects.all().order_by('time')
    serializer_class = SessionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Return a list of all the sessions
        for the currently authenticated user.
        """
        user = self.request.user
        return Session.objects.filter(dean=user)


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })
