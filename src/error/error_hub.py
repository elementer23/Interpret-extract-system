from error.error_hub_signals import ErrorHubSignals

class ErrorHub:
    _signals = ErrorHubSignals()

    @classmethod
    def error_msg(cls, msg: str, type: str = "warning"):
        """Give a message, along with the error type. (default: 'warning', options: 'critical', 'information')"""
        cls._signals.error_raised.emit(msg, type)
    
    @classmethod
    def get(cls):
        return cls._signals