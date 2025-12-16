"""
Audit Log Middleware: logs requests and responses as 'other' actions
"""
import json
import re
import time
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from django.utils.timezone import now
from django.http import HttpRequest, HttpResponse

from apps.audit_logs.models import AuditLog


SENSITIVE_KEYS = getattr(settings, 'AUDIT_LOG_SENSITIVE_KEYS', [
    'password', 'token', 'authorization', 'secret', 'pass', 'pwd'
])
MAX_BODY_LEN = getattr(settings, 'AUDIT_LOG_MAX_BODY_LEN', 2048)


def _redact(data):
    if data is None:
        return None
    try:
        if isinstance(data, (str, bytes)):
            s = data.decode('utf-8', errors='ignore') if isinstance(data, bytes) else data
            # Attempt JSON decode, otherwise truncate
            try:
                obj = json.loads(s)
                return _redact(obj)
            except Exception:
                return s[:MAX_BODY_LEN]
        elif isinstance(data, dict):
            redacted = {}
            for k, v in data.items():
                if any(sk.lower() in k.lower() for sk in SENSITIVE_KEYS):
                    redacted[k] = '***'
                else:
                    redacted[k] = _redact(v)
            return redacted
        elif isinstance(data, list):
            return [_redact(x) for x in data]
        else:
            return str(data)[:MAX_BODY_LEN]
    except Exception:
        return None


class AuditLogMiddleware(MiddlewareMixin):
    def process_request(self, request: HttpRequest):
        request._audit_start = time.perf_counter()
        return None

    def process_response(self, request: HttpRequest, response: HttpResponse):
        try:
            duration_ms = None
            if hasattr(request, '_audit_start'):
                duration_ms = int((time.perf_counter() - request._audit_start) * 1000)

            user = getattr(request, 'user', None)
            actor = user if getattr(user, 'is_authenticated', False) else None

            # Only log API endpoints under /api/
            path = request.path
            if not path.startswith('/api/'):
                return response

            method = request.method
            status_code = getattr(response, 'status_code', None)
            ip = request.META.get('REMOTE_ADDR') or request.META.get('HTTP_X_FORWARDED_FOR')
            user_agent = request.META.get('HTTP_USER_AGENT')

            # Request body
            req_body = None
            try:
                if method in ['POST', 'PUT', 'PATCH']:
                    req_body = _redact(getattr(request, 'body', None))
            except Exception:
                req_body = None

            # Response body (may be streaming)
            resp_body = None
            try:
                if hasattr(response, 'data'):
                    resp_body = _redact(response.data)
                elif hasattr(response, 'content'):
                    resp_body = _redact(response.content)
            except Exception:
                resp_body = None

            changes = {
                'request': {
                    'method': method,
                    'path': path,
                    'body': req_body,
                    'headers': {k: v for k, v in request.META.items() if k.startswith('HTTP_')}
                },
                'response': {
                    'status_code': status_code,
                    'body': resp_body,
                },
                'meta': {
                    'ip': ip,
                    'user_agent': user_agent,
                    'duration_ms': duration_ms,
                }
            }

            # Map HTTP method to action type
            if method == 'POST':
                action_type = 'create'
            elif method in ['PUT', 'PATCH']:
                action_type = 'update'
            elif method == 'DELETE':
                action_type = 'delete'
            else:
                action_type = 'other'

            # Prefer entity_id from response payload if present
            entity_id = status_code or '-'
            try:
                if hasattr(response, 'data') and isinstance(response.data, dict):
                    entity_id = str(response.data.get('id', entity_id))
            except Exception:
                pass

            AuditLog.log_action(
                actor=actor,
                action=action_type,
                entity=path,
                entity_id=entity_id,
                description=f'{method} {path}',
                changes=changes,
                ip_address=ip,
            )
        except Exception:
            # Avoid breaking request flow due to audit issues
            pass

        return response
