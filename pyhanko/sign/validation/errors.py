from typing import Optional

from ..ades.report import AdESIndeterminate, AdESStatus, AdESSubIndic

__all__ = [
    'SignatureValidationError', 'WeakHashAlgorithmError',
    'ValidationInfoReadingError', 'NoDSSFoundError',
    'SigSeedValueValidationError',
    'CMSStructuralError', 'CMSAlgorithmProtectionError',
    'ValueErrorWithMessage'
]


class ValueErrorWithMessage(ValueError):
    """
    Value error with a failure message attribute that can be conveniently
    extracted, instead of having to rely on extracting exception args
    generically.
    """
    def __init__(self, failure_message):
        self.failure_message = str(failure_message)


class ValidationInfoReadingError(ValueErrorWithMessage):
    """Error reading validation info."""
    pass


class NoDSSFoundError(ValidationInfoReadingError):
    def __init__(self):
        super().__init__("No DSS found")


class CMSStructuralError(ValueErrorWithMessage):
    """Structural error in a CMS object."""


class CMSAlgorithmProtectionError(ValueErrorWithMessage):
    """Error related to CMS algorithm protection checks."""


class SignatureValidationError(ValueErrorWithMessage):
    """Error validating a signature."""
    def __init__(self, failure_message,
                 ades_subindication: Optional[AdESSubIndic] = None):
        self.ades_subindication = ades_subindication
        super().__init__(failure_message)

    @property
    def ades_status(self) -> Optional[AdESStatus]:
        if self.ades_subindication is not None:
            return self.ades_subindication.status


class WeakHashAlgorithmError(SignatureValidationError):
    def __init__(self, *args, **kwargs):
        super().__init__(
            *args, **kwargs,
            ades_subindication=AdESIndeterminate.CRYPTO_CONSTRAINTS_FAILURE
        )


class SigSeedValueValidationError(SignatureValidationError):
    """Error validating a signature's seed value constraints."""

    # TODO perhaps we can encode some more metadata here, such as the
    #  seed value that tripped the failure.
    pass
