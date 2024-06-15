import threading

class StoppableThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, *, daemon=None):
        super(StoppableThread, self).__init__(group=group, target=target, name=name, args=args, kwargs=kwargs, daemon=daemon)
        self._stop_event = threading.Event()

    def stop(self):
        print("Stopping Thread")
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()
    