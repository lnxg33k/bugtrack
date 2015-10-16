from django.conf.urls import include, url
from serializers.assessments import AssessmentViewSet, StakeholderViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'assessments', AssessmentViewSet)
router.register(r'stakeholders', StakeholderViewSet)

urlpatterns = [
    url(r'^api/', include(router.urls)),
]
