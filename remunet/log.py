"Logging functions for Remunet."

from mininet.log import *


class RemunetLogger(MininetLogger, object):

    def _log(self, level, msg, args, exc_info=None, extra=None, stack_info=False):
        super()._log(level, msg, args, exc_info, extra, stack_info)

        """
            #TODO THERE ARE YOU NEED TO WRITE OWN OUTPUT
        """


lg = RemunetLogger()


_loggers = lg.info, lg.output, lg.warning, lg.error, lg.debug
_loggers = tuple(makeListCompatible(logger)
                 for logger in _loggers)
lg.info, lg.output, lg.warning, lg.error, lg.debug = _loggers
info, output, warn, error, debug = _loggers

setLogLevel = lg.setLogLevel
