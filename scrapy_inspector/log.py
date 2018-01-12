import logging
import sys
from logging import StreamHandler


def rootlogger_monkeypatch(handler):
    rootloger = logging.getLogger()
    rootloger.handlers = []
    rootloger.handlers.append(handler)
