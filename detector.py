import pyinotify
import getpass
import threading


class MyEventHandler(pyinotify.ProcessEvent):

    def my_init(self, socketio=None):
        self.socketio = socketio

    def process_IN_DELETE(self, event):
        """
        This method processes a specific type of event: IN_DELETE. event
        is an instance of Event.
        """
        print 'deleting: {}\n'.format(event.pathname)
        self.socketio.emit('ssd', 'deleting: {}\n'.format(event.pathname), namespace='/vehicle')

    def process_IN_CREATE(self, event):
        """
        This method is called on these events: IN_CLOSE_WRITE and
        IN_CLOSE_NOWRITE.
        """
        print 'creating: {}\n'.format(event.pathname)
        self.socketio.emit('ssd', 'creating: {}\n'.format(event.pathname), namespace='/vehicle')

    def process_default(self, event):
        """
        Eventually, this method is called for all others types of events.
        This method can be useful when an action fits all events.
        """
        print 'default processing\n'


class myThread(threading.Thread):

    def __init__(self, socketio):
        self.socketio = socketio
        super(self.__class__, self).__init__()

    def run(self):
        # A way to instantiate this class could be:
        p = MyEventHandler(socketio=self.socketio)

        # Instanciate a new WatchManager (will be used to store watches).
        wm = pyinotify.WatchManager()
        # Associate this WatchManager with a Notifier (will be used to report and
        # process events).
        notifier = pyinotify.Notifier(wm, p)
        # Add a new watch on /tmp for ALL_EVENTS.
        wm.add_watch('/media/{}'.format(getpass.getuser()), pyinotify.ALL_EVENTS)
        # Loop forever and handle events.
        notifier.loop()