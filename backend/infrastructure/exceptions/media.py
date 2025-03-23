from backend.infrastructure.exceptions.base import BaseInfastructureError


class InvalidMediaContentTypeError(BaseInfastructureError):
    def __init__(self):
        super().__init__('Invalid media content type')
