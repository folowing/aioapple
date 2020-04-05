
class AioAppleError(Exception):
    pass


class AioAppleTimeoutError(AioAppleError):
    pass


class AioAppleAuthError(AioAppleError):
    pass
