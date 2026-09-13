"""
python manage.py sync_endpoints

Auto-registers every URL pattern under /api/ into the Endpoint table.
Existing rows are preserved (access_type, permission not overwritten);
new rows are created with sensible defaults.
"""
from django.core.management.base import BaseCommand
from django.urls import get_resolver, URLPattern, URLResolver

from apps.permissions.models.permissions import Endpoint


HTTP_METHODS = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']


def _extract_paths(url_patterns, prefix=''):
    routes = []
    for pattern in url_patterns:
        if isinstance(pattern, URLResolver):
            new_prefix = prefix + str(pattern.pattern)
            routes.extend(_extract_paths(pattern.url_patterns, new_prefix))
        elif isinstance(pattern, URLPattern):
            import re
            route = prefix + str(pattern.pattern)
            # Django path converters (<int:member_id>, <str:x>, <uuid:x>, <pk>, <name>)
            # → hammasi {id} bo'ladi (middleware'ning normalize_path'i bilan mos)
            route = re.sub(r'<(?:int:|str:|uuid:|slug:|path:)?[a-zA-Z_][a-zA-Z0-9_]*>', '{id}', route)
            route = '/' + route.lstrip('/')
            if not route.endswith('/') and '.' not in route.split('/')[-1]:
                route = route + '/'
            routes.append((route, pattern.callback))
    return routes


class Command(BaseCommand):
    help = 'Sync all API endpoints into the Endpoint table'

    def add_arguments(self, parser):
        parser.add_argument('--prefix', default='/api/', help='Only endpoints under this prefix')
        parser.add_argument('--dry-run', action='store_true')

    def handle(self, *args, **opts):
        resolver = get_resolver()
        prefix = opts['prefix']
        dry = opts['dry_run']

        routes = _extract_paths(resolver.url_patterns)
        created, skipped = 0, 0

        for path, callback in routes:
            if not path.startswith(prefix):
                continue

            view_class = getattr(callback, 'view_class', None)
            methods = HTTP_METHODS
            if view_class:
                methods = [m.upper() for m in view_class.http_method_names if m.upper() in HTTP_METHODS]

            for method in methods:
                exists = Endpoint.objects.filter(path=path, method=method).exists()
                if exists:
                    skipped += 1
                    continue
                self.stdout.write(f"  + {method:6s} {path}")
                if not dry:
                    Endpoint.objects.create(
                        path=path,
                        method=method,
                        name=f"{method} {path}",
                        access_type='authenticated',
                        is_active=True,
                    )
                created += 1

        self.stdout.write(self.style.SUCCESS(
            f"Done. Created: {created}, existing skipped: {skipped}"
        ))
