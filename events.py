__author__ = 'ievans3024'


class EventSystem(object):

    def __init__(self):
        self._handlers = {}
        self._queue = []

    def __setitem__(self, name, callback):
        """
        Creates a new event type, assigns callback.
        Appends callback if event type already exists.
        """
        if hasattr(callback, '__call__'):
            if self._handlers.get(name):
                self._handlers.get(name).append(callback)
            else:
                self._handlers[name] = [callback]
        else:
            raise TypeError('Callback must be callable (e.g., function)')

    def __delitem__(self, name):
        """
        Erases an event type entirely, dissociating all callbacks.
        Use EventSystem.unbind(name, callback) to unbind a specific callback.
        """
        if self._handlers.get(name):
            del self._handlers[name]

    def __getitem__(self, name):
        """Gets a list of bound callbacks by event name"""
        if self._handlers.get(name):
            return self._handlers[name]

    def append(self, name):
        """Appends an event to the queue"""
        self._queue.append(name)

    def dispatch(self):
        for event in self._poll():
            for func in self.get(event):
                func()

    def _poll(self):
        """Current queue as generator. Events are removed from the queue as they are supplied."""
        while self._queue:
            yield self._queue.pop(0)

    get = __getitem__



