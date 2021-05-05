from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('results', views.resultspage),
    path('home', views.index, name='home'),
    path('update', views.updatepage, name='update'),
    path('uploadPDF', views.uploadpdf, name='uploadPDF'),
    path('upload_submit_button',views.upload_submit_button,name='upload_submit_button'),
    path('login',views.loginButton, name='login'),
    #path('actionUrl', views.resultspage),
]

# should remember that this is set only for when debug = True.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
