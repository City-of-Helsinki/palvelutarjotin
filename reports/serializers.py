from reports.models import EnrolmentReport
from rest_framework import serializers


class EnrolmentReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnrolmentReport
        fields = "__all__"
