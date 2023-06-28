from django.contrib import admin

# Register your models here.
# Register your models here.
from .models import Student
from .models import Dean
from .models import Session


admin.site.register(Dean)
admin.site.register(Student)
admin.site.register(Session)
