"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import builtins
import google.protobuf.descriptor
import google.protobuf.internal.extension_dict
import google.protobuf.message
import pyatv.protocols.mrp.protobuf.NowPlayingClient_pb2
import pyatv.protocols.mrp.protobuf.ProtocolMessage_pb2
import typing
import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor = ...

class UpdateClientMessage(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
    CLIENT_FIELD_NUMBER: builtins.int
    @property
    def client(self) -> pyatv.protocols.mrp.protobuf.NowPlayingClient_pb2.NowPlayingClient: ...
    def __init__(self,
        *,
        client : typing.Optional[pyatv.protocols.mrp.protobuf.NowPlayingClient_pb2.NowPlayingClient] = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal[u"client",b"client"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal[u"client",b"client"]) -> None: ...
global___UpdateClientMessage = UpdateClientMessage

updateClientMessage: google.protobuf.internal.extension_dict._ExtensionFieldDescriptor[pyatv.protocols.mrp.protobuf.ProtocolMessage_pb2.ProtocolMessage, global___UpdateClientMessage] = ...
