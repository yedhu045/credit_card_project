from django.contrib import admin
from .models import Register, Card, Transaction, FraudAlert

admin.site.register(Register)
admin.site.register(Card)
admin.site.register(Transaction)
admin.site.register(FraudAlert)


# Register your models here.
