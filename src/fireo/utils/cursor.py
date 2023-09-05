import base64
import json
from datetime import datetime
from typing import Optional, TYPE_CHECKING

from google.cloud.firestore_v1 import Query

from fireo.fields import DateTime
from fireo.utils.utils import get_nested_field_by_dotted_name

if TYPE_CHECKING:
    from fireo.queries.query_set import QuerySet
    from fireo.queries.filter_query import FilterQuery


class Cursor(dict):
    @classmethod
    def from_string(cls, cursor_string: str):
        return cls(**json.loads(base64.b64decode(cursor_string)))

    def to_string(self) -> str:
        return base64.b64encode(json.dumps(self).encode()).decode()

    @classmethod
    def extract(cls, query: 'FilterQuery') -> 'Cursor':
        cursor = {}
        if query.parent:
            cursor['parent'] = query.parent

        for name, op, val in query._select_query:
            # ISSUE # 77
            # if filter value type is datetime then it need to first
            # convert into string then JSON serialize
            if isinstance(val, datetime):
                val = val.isoformat()

            cursor.setdefault('filters', []).append((name, op, val))

        cursor['limit'] = query._limit

        if query._order:
            cursor['order'] = ','.join(
                ('-' if direction == Query.DESCENDING else '') + name
                for name, direction in query._order
            )

        return cls(**cursor)

    def apply(self, parent: Optional[str], queryset: 'QuerySet') -> 'FilterQuery':
        if 'parent' in self:
            parent = self['parent']

        query = queryset.filter(parent)

        if 'filters' in self:
            for name, op, val in self['filters']:
                # ISSUE # 77
                # if field is datetime and type is str (which is usually come from cursor)
                # then convert this string into datetime format
                field = get_nested_field_by_dotted_name(queryset.model_cls, name)
                if isinstance(field, DateTime):
                    val = datetime.fromisoformat(val)

                query = query.filter(name, op, val)

        if 'order' in self:
            for order in self['order'].split(','):
                query = query.order(order)

        if 'limit' in self:
            query = query.limit(self['limit'])

        # check if last doc key is available or not
        if 'last_doc_key' in self:
            query = query.start_after(key=self['last_doc_key'])

        else:
            query = query.offset(self['offset'])

        return query
