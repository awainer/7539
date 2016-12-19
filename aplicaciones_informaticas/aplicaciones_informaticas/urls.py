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
from django.conf.urls import url, include
from rest_framework import routers
from django.contrib import admin
from backend import views

admin.autodiscover()


router = routers.DefaultRouter()
router.register(r'healthcenters', views.HealthCenterViewSet)
router.register(r'queues', views.AtentionQueueViewSet)
router.register(r'specialties', views.SpecialtyViewSet, base_name='Specialty')
router.register(r'triagescalelevel', views.TriageScaleLevelViewSet, base_name='TriageScaleLevel')


urlpatterns = [
    url(r'^api/v1/', include(router.urls)),
    url(r'^admin/', admin.site.urls),
    url(r'^api/v1/hospitals/(?P<hc_id>[-\w]+)/queues/(?P<queue_id>\d+)$',
                views.AtentionQueueViewSet.as_view({'get': 'get_one_for_hc'})),
    url(r'^api/v1/hospitals/(?P<hc_id>[-\w]+)/queues/?$',
                views.AtentionQueueViewSet.as_view({'get': 'get_all_for_hc'})),
    url(r'^api/v1/hospitals/(?P<hc_id>[-\w]+)/queue/(?P<queue_id>\d+)/patients?$',
                views.AtentionQueueViewSet.as_view({'post': 'add_patient', 'get': 'get_all_patients'})),
    url(r'^api/v1/hospitals/(?P<hc_id>[-\w]+)/queue/(?P<queue_id>\d+)/patients?/(?P<patient_id>\d+)$',
                views.AtentionQueueViewSet.as_view({'get': 'get_patient', 'delete':'delete_patient'})),
    url(r'^api/v1/hospitals/recommendation$',
                views.RecommendationEngineViewSet.as_view({'post':'get_recommendation'})),
    url(r'^api/v1/hospitals/recommendation/select/(?P<hc_id>[-\w]+)/queue/(?P<queue_id>\d+)/',
                views.RecommendationEngineViewSet.as_view({'post':'select_recommendation'})),
    url(r'^api/v1/hospitals/(?P<hc_id>[-\w]+)/rate',
                views.HealthCenterViewSet.as_view({'post':'rate'})),
    url(r'^api/v1/hospitals/avg',
                views.HealthCenterViewSet.as_view({'get':'get_average_wait'})),
    url(r'^api/v1/hospitals/stats/(?P<hc_id>[-\w]+)/count$',
                views.HealthCenterViewSet.as_view({'get':'patient_count_stats'})),
    url(r'^api/v1/hospitals/stats/(?P<hc_id>[-\w]+)/count/per_specialty',
                views.ReportsViewSet.as_view({'get':'patient_percentage_per_specialty'})),
    url(r'^api/v1/hospitals/(?P<hc_id>[-\w]+)/feed',
                views.ReportsViewSet.as_view({'get':'get_feed'})),
    url(r'^api/v1/hospitals/stats/(?P<hc_id>[-\w]+)/delete_reason$',
                views.ReportsViewSet.as_view({'get':'patient_delete_reason'})),
    url(r'^api/v1/hospitals/statistics/attention_per_hour',
                views.ReportsViewSet.as_view({'get':'get_attention_per_hour'}))

]

