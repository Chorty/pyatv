"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import builtins
import google.protobuf.descriptor
import google.protobuf.internal.extension_dict
import google.protobuf.message
import pyatv.protocols.mrp.protobuf.ProtocolMessage_pb2
import typing
import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor = ...

class AudioFadeResponseMessage(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
    FADEDURATION_FIELD_NUMBER: builtins.int
    fadeDuration: builtins.int = ...
    def __init__(self,
        *,
        fadeDuration : typing.Optional[builtins.int] = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal[u"fadeDuration",b"fadeDuration"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal[u"fadeDuration",b"fadeDuration"]) -> None: ...
global___AudioFadeResponseMessage = AudioFadeResponseMessage

audioFadeResponseMessage: google.protobuf.internal.extension_dict._ExtensionFieldDescriptor[pyatv.protocols.mrp.protobuf.ProtocolMessage_pb2.ProtocolMessage, global___AudioFadeResponseMessage] = ...
