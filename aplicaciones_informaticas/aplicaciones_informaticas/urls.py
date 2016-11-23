"""aplicaciones_informaticas URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from rest_framework import routers
from django.contrib import admin
from backend import views

admin.autodiscover()


router = routers.DefaultRouter()
router.register(r'healthcenters', views.HealthCenterViewSet)
router.register(r'queues', views.AtentionQueueViewSet)

#/hospitals/{idHospital}/queue/{idQueue}/patients
#/hospitals/{idHospital}/queues/{idQueue}/patients/{idPatient}:
urlpatterns = [
    url(r'^api/v1/', include(router.urls)),
    url(r'^admin/', admin.site.urls),
    url(r'^api/v1/hospitals/(?P<hc_id>[-\w]+)/queues/(?P<queue_id>\d+)$', views.AtentionQueueViewSet.as_view({'get': 'get_one_for_hc'})),
    url(r'^api/v1/hospitals/(?P<hc_id>[-\w]+)/queues/?$', views.AtentionQueueViewSet.as_view({'get': 'get_all_for_hc'})),
    url(r'^api/v1/hospitals/(?P<hc_id>[-\w]+)/queue/(?P<queue_id>\d+)/patients?$',views.AtentionQueueViewSet.as_view({'post': 'add_patient'})),
    url(r'^api/v1/hospitals/(?P<hc_id>[-\w]+)/queue/(?P<queue_id>\d+)/patients?/(?P<patient_id>\d+)$',
                        views.AtentionQueueViewSet.as_view({'get': 'get_patient'})),
#    url(r'^api/v1/', include('rest_framework.urls', namespace='rest_framework'))
]
