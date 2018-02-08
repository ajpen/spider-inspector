import json
import logging
import pkg_resources
import webbrowser

import autobahn.twisted as autobahn
from autobahn.twisted.resource import WebSocketResource

from twisted.web.server import Site
from twisted.web.static import File

from scrapy.utils.python import to_unicode
from scrapy.utils.reactor import listen_tcp
from scrapy.utils.reqser import request_to_dict
from scrapy.exceptions import NotConfigured
from scrapy import signals

STATIC_FILES = pkg_resources.resource_filename(__name__, 'client/')


class InspectorServer(autobahn.WebSocketServerFactory):

    def __init__(self, crawler, *args, **kwargs):
        if not crawler.settings.getbool('INSPECTOR_ENABLED'):
            raise NotConfigured
        super(InspectorServer, self).__init__()
        self.host = crawler.settings.get('INSPECTOR_HOST', '127.0.0.1')
        ports = crawler.settings.get('INSPECTOR_PORT', None)
        if ports:
            self.portrange = [int(x) for x in ports if len(x) > 2]
        else:
            self.portrange = [7024, 7074]
        self.crawler = crawler
        self.protocol = websocket_protocol_factory(self)
        self.logger = logging.getLogger(__name__)
        self.crawler.signals.connect(self.start_listening, signals.engine_started)
        self.crawler.signals.connect(self.stop_listening, signals.engine_stopped)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def start_listening(self):
        resource = WebSocketResource(self)

        # serve files from ./client
        root = File(STATIC_FILES)
        root.putChild(b"ws", resource)
        site = Site(root)
        self.port = listen_tcp(self.portrange, self.host, site)
        h = self.port.getHost()
        self.logger.debug("Inspector available on %(host)s:%(port)d",
                     {'host': h.host, 'port': h.port},
                     extra={'crawler': self.crawler})
        if self.crawler.settings.get('INSPECTOR_BROWSER', None):
            webbrowser.open('http://{}:{}'.format(h.host, h.port))

    def stop_listening(self):
        self.port.stopListening()


def websocket_protocol_factory(server_instance):

    class WebSocketProtocol(autobahn.WebSocketServerProtocol):

        def __init__(self, server=server_instance):
            super(WebSocketProtocol, self).__init__()
            self.server = server

        def onMessage(self, payload, is_binary):
            print payload

        def onOpen(self):
            self.setup_signals()

        @staticmethod
        def response_to_dict(response):
            d = {
                'url': to_unicode(response.url),
                'status': int(response.status),
                'headers': dict(response.headers),
                'body': response.body,
                'flags': list(response.flags),
                'request': request_to_dict(response.request)
            }
            return d

        @staticmethod
        def build_and_encode_payload(event, **kwargs):
            payload = {
                'event': event
            }
            request = kwargs.get('request', None)
            if request:
                request = request_to_dict(request, kwargs.get('spider', None))
                payload['request'] = request

            response = kwargs.get('response', None)
            if response:
                response = WebSocketProtocol.response_to_dict(response)
                payload['response'] = response

            return json.dumps(payload, ensure_ascii=True, indent=2)

        def setup_signals(self):
            supported_signals = {
                'request_scheduled': signals.request_scheduled,
                'request_dropped': signals.request_dropped,
                'response_received': signals.response_received
            }

            for name, signal in supported_signals.items():
                func = self._event_callback_factory(name)
                self.server.crawler.signals.connect(func, signal=signal, weak=False)

        def _event_callback_factory(self, event_type):
            server = self

            def push_request_event(**kwargs):
                payload = server.build_and_encode_payload(event_type, **kwargs)
                server.sendMessage(payload, isBinary=False)

            return push_request_event

    return WebSocketProtocol
