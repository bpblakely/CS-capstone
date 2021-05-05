from django.contrib import admin
from .models import researchint, publications, grants

# Register your models here to be used on admin site
#admin.site.register(ContactInfo)
admin.site.register(researchint)
admin.site.register(publications)
admin.site.register(grants)
