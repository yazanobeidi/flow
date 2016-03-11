__author__ = 'yazan'

class FlowException(Exception):
    """
    Base exception class for Flow. Can subclass to create custom error messages.
    """
    def __init__(self, message=None):
        self.message = message
        Exception.__init__(self)

    def __str__(self):
        return self.message or 'Unrecoverable exception in Flow runtime'

class Bankruptcy(FlowException):
    """
    Exception to be raised when bankroll passes zero.
    """
    def __str__(self):
        return 'Out of funds.'