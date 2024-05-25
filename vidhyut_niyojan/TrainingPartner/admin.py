from django.contrib import admin
from .models import CountryMaster, StateMaster, CityMaster
# Register your models here.
admin.site.register(CountryMaster)
admin.site.register(StateMaster)
admin.site.register(CityMaster)
