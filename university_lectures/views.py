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
from datetime import date, timedelta
# Create your views here.


class AvailableSessions(generics.ListCreateAPIView):
    """
    List all available sessions, or book a new session.
    """
    authentication_classes = (SessionAuthentication,
                              BasicAuthentication, TokenAuthentication)
    queryset = Session.objects.filter(available=True)
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


class StudentDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a student record.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    authentication_classes = (SessionAuthentication,
                              BasicAuthentication, TokenAuthentication)
    queryset = Student.objects.all().order_by('id')
    serializer_class = StudentSerializer


class DeanList(generics.ListCreateAPIView):
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


class DeanDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a dean record.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    authentication_classes = (SessionAuthentication,
                              BasicAuthentication, TokenAuthentication)
    queryset = Dean.objects.all()
    serializer_class = DeanSerializer


class SessionDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a session record.
    """
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = (SessionAuthentication,
                              BasicAuthentication, TokenAuthentication)
    queryset = Session.objects.all()
    serializer_class = SessionSerializer


class DeanSessions(generics.ListCreateAPIView):
    """
    List all available sessions, or book a new session.
    """
    authentication_classes = (SessionAuthentication,
                              BasicAuthentication, TokenAuthentication)
    permission_classes = [permissions.IsAuthenticated]
    queryset = Session.objects.all()
    serializer_class = SessionSerializer

    def list(self, request):
        """
        Return a list of all the sessions
        for the currently authenticated user.
        """
        try:
            user = self.request.user
            dean = Dean.objects.get(id=user)
            startdate = date.today()
            enddate = startdate + timedelta(days=7)
            queryset = Session.objects.filter(
                time__range=[startdate, enddate], dean=dean, available=False)
            serializer = SessionSerializer(queryset, many=True)
            return Response(serializer.data)
        except:
            return Response({"message": "User doesn't have permission"})

    # def get_queryset(self):
    #     """
    #     Return a list of all the sessions
    #     for the currently authenticated user.
    #     """
    #
    #


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'db_identifier': user.pk,
        })
