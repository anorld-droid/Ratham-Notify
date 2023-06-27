from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Student, Dean, Session


class UserSerializer(serializers.ModelSerializer):
    students = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Student.objects.all())
    deans = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Dean.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'students', 'deans']


class DeanSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Dean
        fields = ['id', 'owner',  'name']


class StudentSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Student
        fields = ['id', 'owner',  'name']


class SessionSerializer(serializers.HyperlinkedModelSerializer):
    dean = DeanSerializer()
    student = StudentSerializer()

    class Meta:
        model = Session
        fields = ['time', 'available', 'dean', 'student']

    def create(self, validated_data):
        deans_data = validated_data.pop('dean')
        dean = Dean.objects.get(id=dean_data.get('id'))
        student_data = validated_data.pop('dean')
        student = Dean.objects.get(id=student_data.get('id'))
        employee = Session.objects.create(
            **validated_data, dean=dean, student=student)
        return employee
