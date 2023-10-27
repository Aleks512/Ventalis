from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import NewUser, Consultant, Customer

class ConsultantAdmin(admin.ModelAdmin):
    model = Consultant
    verbose_name = "Consultant"
    verbose_name_plural = "Consultants"

admin.site.register(Consultant, ConsultantAdmin)
admin.site.register(Customer)
admin.site.register(NewUser)
