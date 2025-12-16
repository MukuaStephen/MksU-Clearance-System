"""
Audit mixin for DRF ModelViewSets to record create/update/delete actions
"""
from typing import Any

from django.conf import settings
from rest_framework.request import Request

from apps.audit_logs.models import AuditLog


class AuditViewSetMixin:
    """Mixin to log CRUD actions for DRF viewsets via AuditLog"""

    def _entity_name(self) -> str:
        try:
            return self.get_queryset().model.__name__
        except Exception:
            try:
                return self.get_serializer_class().Meta.model.__name__  # type: ignore[attr-defined]
            except Exception:
                return self.__class__.__name__

    def _ip(self, request: Request) -> str | None:
        return request.META.get('REMOTE_ADDR') or request.META.get('HTTP_X_FORWARDED_FOR')

    def perform_create(self, serializer):  # type: ignore[override]
        instance = serializer.save()
        try:
            AuditLog.log_action(
                actor=getattr(self.request, 'user', None),
                action='create',
                entity=self._entity_name(),
                entity_id=getattr(instance, 'id', getattr(instance, 'pk', '-')),
                description=f'Created {self._entity_name()} via API',
                changes={'data': getattr(serializer, 'data', {})},
                ip_address=self._ip(self.request),
            )
        except Exception:
            pass

    def perform_update(self, serializer):  # type: ignore[override]
        # Capture target id before save
        try:
            obj = self.get_object()
            obj_id: Any = getattr(obj, 'id', getattr(obj, 'pk', '-'))
        except Exception:
            obj_id = '-'
        instance = serializer.save()
        try:
            AuditLog.log_action(
                actor=getattr(self.request, 'user', None),
                action='update',
                entity=self._entity_name(),
                entity_id=obj_id if obj_id != '-' else getattr(instance, 'id', getattr(instance, 'pk', '-')),
                description=f'Updated {self._entity_name()} via API',
                changes={'data': getattr(serializer, 'data', {})},
                ip_address=self._ip(self.request),
            )
        except Exception:
            pass

    def perform_destroy(self, instance):  # type: ignore[override]
        try:
            AuditLog.log_action(
                actor=getattr(self.request, 'user', None),
                action='delete',
                entity=self._entity_name(),
                entity_id=getattr(instance, 'id', getattr(instance, 'pk', '-')),
                description=f'Deleted {self._entity_name()} via API',
                changes={},
                ip_address=self._ip(self.request),
            )
        except Exception:
            pass