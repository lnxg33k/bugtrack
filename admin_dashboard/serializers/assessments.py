from rest_framework import serializers, viewsets
from app.models import Assessment, Stakeholder


class StakeholderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Stakeholder
        fields = ('username', 'id')


class StakeholderViewSet(viewsets.ModelViewSet):
    queryset = Stakeholder.objects.all()
    serializer_class = StakeholderSerializer


class AssessmentSerializer(serializers.ModelSerializer):
    stakeholders = StakeholderSerializer(many=True, read_only=True)

    class Meta:
        model = Assessment
        fields = (
            'name', 'slug', 'stakeholders', 'introduction',
            'summary', 'is_published'
        )


class AssessmentViewSet(viewsets.ModelViewSet):
    queryset = Assessment.objects.all()
    serializer_class = AssessmentSerializer
