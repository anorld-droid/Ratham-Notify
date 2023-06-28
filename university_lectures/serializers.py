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


class DeanSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Dean
        fields = ['id', 'owner',  'name']


class StudentSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Dean
        fields = ['id', 'owner',  'name']


class SessionSerializer(serializers.HyperlinkedModelSerializer):
    dean = DeanSerializer(read_only=True)
    student = StudentSerializer(instance=Student())

    class Meta:
        model = Session
        fields = ['time', 'available', 'dean', 'student']

    def create(self, validated_data):
        dean = Dean.objects.get_or_create(
            **validated_data.pop('dean'))
        student = Student.objects.get_or_create(
            **validated_data.pop('student'))
        employee = Session.objects.create(
            **validated_data, dean=dean, student=student)
        return employee

    def update(self, instance, validated_data):
        instance.id = validated_data.get('id', instance.id)
        instance.time = validated_data.get(
            'time', instance.time)
        instance.available = validated_data.get(
            'available', instance.available)

        if 'dean' in validated_data:
            dean_data = validated_data.pop('dean')
            dean = instance.dean
            dean.id = dean_data.get('id', dean.id)
            dean.owner = dean_data.get('owner', dean.owner)
            dean.name = dean_data.get('name', dean.name)
            dean.save()

        if 'student' in validated_data:
            student_data = validated_data.pop('student')
            print(student_data.get('id'))
            student = Student.objects.get(id=student_data.get('id'))
            student.id = student_data.get('id', student.id)
            student.owner = User.objects.get(
                is_superuser=True)
            student.name = student_data.get('name', student.name)
            student.save()
            instance.student = student

        instance.save()

        return instance
