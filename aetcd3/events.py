class Event(object):
    """Base event type.

    :param event: Raw gRPC event
    """

    def __init__(self, event):
        self.key = event.kv.key

        self._event = event

    def __getattr__(self, name):
        if name.startswith('prev_'):
            return getattr(self._event.prev_kv, name[5:])
        return getattr(self._event.kv, name)

    def __str__(self):
        return f'{self.__class__} key={self.key} value={self.value}'


class PutEvent(Event):
    """Put event type."""


class DeleteEvent(Event):
    """Delete event type."""


def new_event(event):
    """Wrap a raw gRPC event in a friendlier containing class.

    This picks the appropriate class from one of :class:`PutEvent` or
    :class:`DeleteEvent` and returns a new instance.

    If wrong raw gRPC event was provided `Exception` is raised.

    :param event: Raw gRPC event

    :rtype: One of :class:`PutEvent` or :class:`DeleteEvent`

    :raises: :class:`Exception`
    """
    op_name = event.EventType.DESCRIPTOR.values_by_number[event.type].name
    if op_name == 'PUT':
        cls = PutEvent
    elif op_name == 'DELETE':
        cls = DeleteEvent
    else:
        raise Exception('Invalid gRPC event type name')

    return cls(event)
