from rest_framework import serializers

class APIResponseSerializer(serializers.Serializer):
    success = serializers.BooleanField()
    status = serializers.CharField(required=False)
    count = serializers.IntegerField(required=False)
    next = serializers.URLField(required=False)
    previous = serializers.URLField(required=False)
    data = serializers.JSONField(required=False)
    error = serializers.CharField(required=False)
