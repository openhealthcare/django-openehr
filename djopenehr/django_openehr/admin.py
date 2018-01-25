from django.contrib import admin
from .models import AddressDetails, TelecomDetails, Demographics, SymptomSign

admin.site.register(AddressDetails)
admin.site.register(TelecomDetails)
admin.site.register(Demographics)
admin.site.register(SymptomSign)
