"""
Serializers for Audit Logs
"""
from rest_framework import serializers
from apps.audit_logs.models import AuditLog


class AuditLogListSerializer(serializers.ModelSerializer):
    actor_name = serializers.CharField(source='actor.full_name', read_only=True)
    actor_email = serializers.CharField(source='actor.email', read_only=True)

    class Meta:
        model = AuditLog
        fields = [
            'id',
            'actor',
            'actor_name',
            'actor_email',
            'action',
            'entity',
            'entity_id',
            'description',
            'ip_address',
            'created_at'
        ]
        read_only_fields = fields


class AuditLogSerializer(serializers.ModelSerializer):
    actor_name = serializers.CharField(source='actor.full_name', read_only=True)
    actor_email = serializers.CharField(source='actor.email', read_only=True)

    class Meta:
        model = AuditLog
        fields = [
            'id',
            'actor',
            'actor_name',
            'actor_email',
            'action',
            'entity',
            'entity_id',
            'description',
            'changes',
            'ip_address',
            'created_at'
        ]
        read_only_fields = fields


class AuditLogStatisticsSerializer(serializers.Serializer):
    total_logs = serializers.IntegerField()
    by_action = serializers.DictField()
    top_entities = serializers.ListField(child=serializers.DictField())
    top_users = serializers.ListField(child=serializers.DictField())
    recent_logs = AuditLogListSerializer(many=True)
