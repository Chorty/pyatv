"""Pick authentication type based on device support."""
import logging
from typing import Tuple

from pyatv import exceptions
from pyatv.auth.hap_pairing import (
    NO_CREDENTIALS,
    TRANSIENT_CREDENTIALS,
    AuthenticationType,
    HapCredentials,
    PairSetupProcedure,
    PairVerifyProcedure,
    parse_credentials,
)
from pyatv.auth.hap_session import HAPSession
from pyatv.auth.hap_srp import SRPAuthHandler
from pyatv.interface import BaseService
from pyatv.protocols.airplay import features as ft
from pyatv.protocols.airplay.auth.hap import (
    AirPlayHapPairSetupProcedure,
    AirPlayHapPairVerifyProcedure,
)
from pyatv.protocols.airplay.auth.hap_transient import (
    AirPlayHapTransientPairVerifyProcedure,
)
from pyatv.protocols.airplay.auth.legacy import (
    AirPlayLegacyPairSetupProcedure,
    AirPlayLegacyPairVerifyProcedure,
)
from pyatv.protocols.airplay.srp import LegacySRPAuthHandler, new_credentials
from pyatv.support.http import HttpConnection

_LOGGER = logging.getLogger(__name__)

CONTROL_SALT = "Control-Salt"
CONTROL_OUTPUT_INFO = "Control-Write-Encryption-Key"
CONTROL_INPUT_INFO = "Control-Read-Encryption-Key"


class NullPairVerifyProcedure:
    """Null implementation for Pair-Verify when no verification is needed."""

    async def verify_credentials(self) -> bool:
        """Verify if credentials are valid."""
        _LOGGER.debug("Performing null Pair-Verify")
        return False

    @staticmethod
    def encryption_keys(salt: str, output_info: str, input_key: str) -> Tuple[str, str]:
        """Return derived encryption keys."""
        raise exceptions.NotSupportedError(
            "encryption keys not supported by null implementation"
        )


def pair_setup(
    auth_type: AuthenticationType, connection: HttpConnection
) -> PairSetupProcedure:
    """Return procedure object used for Pair-Setup."""
    _LOGGER.debug("Setting up new AirPlay Pair-Setup procedure with type %s", auth_type)

    if auth_type == AuthenticationType.Legacy:
        srp = LegacySRPAuthHandler(new_credentials())
        srp.initialize()
        return AirPlayLegacyPairSetupProcedure(connection, srp)
    if auth_type == AuthenticationType.HAP:
        srp = SRPAuthHandler()
        srp.initialize()
        return AirPlayHapPairSetupProcedure(connection, srp)

    raise exceptions.NotSupportedError(
        f"authentication type {auth_type} does not support Pair-Setup"
    )


def pair_verify(
    credentials: HapCredentials, connection: HttpConnection
) -> PairVerifyProcedure:
    """Return procedure object used for Pair-Verify."""
    _LOGGER.debug(
        "Setting up new AirPlay Pair-Verify procedure with type %s", credentials.type
    )

    if credentials.type == AuthenticationType.Null:
        return NullPairVerifyProcedure()
    if credentials.type == AuthenticationType.Legacy:
        srp = LegacySRPAuthHandler(credentials)
        srp.initialize()
        return AirPlayLegacyPairVerifyProcedure(connection, srp)

    srp = SRPAuthHandler()
    srp.initialize()
    if credentials.type == AuthenticationType.HAP:
        return AirPlayHapPairVerifyProcedure(connection, srp, credentials)
    return AirPlayHapTransientPairVerifyProcedure(connection, srp)


async def verify_connection(
    credentials: HapCredentials, connection: HttpConnection
) -> None:
    """Perform Pair-Verify on a connection and enable encryption."""
    verifier = pair_verify(credentials, connection)
    has_encryption_keys = await verifier.verify_credentials()

    if has_encryption_keys:
        output_key, input_key = verifier.encryption_keys(
            CONTROL_SALT, CONTROL_OUTPUT_INFO, CONTROL_INPUT_INFO
        )

        session = HAPSession()
        session.enable(output_key, input_key)
        connection.receive_processor = session.decrypt
        connection.send_processor = session.encrypt

    return verifier


def extract_credentials(service: BaseService) -> HapCredentials:
    """Extract credentials from service based on what's supported."""
    if service.credentials is not None:
        return parse_credentials(service.credentials)

    features = ft.parse(service.properties.get("features", "0x0"))
    if (
        ft.AirPlayFlags.SupportsSystemPairing in features
        or ft.AirPlayFlags.SupportsCoreUtilsPairingAndEncryption in features
    ):
        return TRANSIENT_CREDENTIALS

    return NO_CREDENTIALS
