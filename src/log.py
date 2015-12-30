import gi
gi.require_version('Tracker', '1.0')
from gi.repository import Tracker
from itertools import chain
import logging
import time
logger = logging.getLogger(__name__)


def log(fn):

    def wrapped(*v, **k):
        if logger.getEffectiveLevel() > logging.DEBUG:
            return fn(*v, **k)

        global tabbing
        name = fn.__qualname__
        filename = fn.__code__.co_filename.split('/')[-1]
        lineno = fn.__code__.co_firstlineno
        params = ", ".join(map(repr, chain(v, k.values())))

        start = time.time()
        retval = fn(*v, **k)
        elapsed = time.time() - start
        logger.debug("%s%s(%s)->(%s)[%02f][%s:%s]",'|', name, params, repr(retval), elapsed, filename, lineno,)

        return retval

    return wrapped
