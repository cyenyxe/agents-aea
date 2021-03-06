# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: fipa.proto

import sys

_b = sys.version_info[0] < 3 and (lambda x: x) or (lambda x: x.encode("latin1"))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


DESCRIPTOR = _descriptor.FileDescriptor(
    name="fipa.proto",
    package="fetch.aea.fipa",
    syntax="proto3",
    serialized_options=None,
    serialized_pb=_b(
        '\n\nfipa.proto\x12\x0e\x66\x65tch.aea.fipa"\x8d\x07\n\x0b\x46IPAMessage\x12\x12\n\nmessage_id\x18\x01 \x01(\x05\x12"\n\x1a\x64ialogue_starter_reference\x18\x02 \x01(\t\x12$\n\x1c\x64ialogue_responder_reference\x18\x03 \x01(\t\x12\x0e\n\x06target\x18\x04 \x01(\x05\x12.\n\x03\x63\x66p\x18\x05 \x01(\x0b\x32\x1f.fetch.aea.fipa.FIPAMessage.CFPH\x00\x12\x36\n\x07propose\x18\x06 \x01(\x0b\x32#.fetch.aea.fipa.FIPAMessage.ProposeH\x00\x12\x34\n\x06\x61\x63\x63\x65pt\x18\x07 \x01(\x0b\x32".fetch.aea.fipa.FIPAMessage.AcceptH\x00\x12?\n\x0cmatch_accept\x18\x08 \x01(\x0b\x32\'.fetch.aea.fipa.FIPAMessage.MatchAcceptH\x00\x12\x36\n\x07\x64\x65\x63line\x18\t \x01(\x0b\x32#.fetch.aea.fipa.FIPAMessage.DeclineH\x00\x12\x34\n\x06inform\x18\n \x01(\x0b\x32".fetch.aea.fipa.FIPAMessage.InformH\x00\x12\x44\n\x0f\x61\x63\x63\x65pt_w_inform\x18\x0b \x01(\x0b\x32).fetch.aea.fipa.FIPAMessage.AcceptWInformH\x00\x12O\n\x15match_accept_w_inform\x18\x0c \x01(\x0b\x32..fetch.aea.fipa.FIPAMessage.MatchAcceptWInformH\x00\x1a}\n\x03\x43\x46P\x12\x0f\n\x05\x62ytes\x18\x01 \x01(\x0cH\x00\x12:\n\x07nothing\x18\x02 \x01(\x0b\x32\'.fetch.aea.fipa.FIPAMessage.CFP.NothingH\x00\x12\x15\n\x0bquery_bytes\x18\x03 \x01(\x0cH\x00\x1a\t\n\x07NothingB\x07\n\x05query\x1a\x1b\n\x07Propose\x12\x10\n\x08proposal\x18\x01 \x03(\x0c\x1a\x08\n\x06\x41\x63\x63\x65pt\x1a\r\n\x0bMatchAccept\x1a\t\n\x07\x44\x65\x63line\x1a\x17\n\x06Inform\x12\r\n\x05\x62ytes\x18\x01 \x01(\x0c\x1a\x1e\n\rAcceptWInform\x12\r\n\x05\x62ytes\x18\x01 \x01(\x0c\x1a#\n\x12MatchAcceptWInform\x12\r\n\x05\x62ytes\x18\x01 \x01(\x0c\x42\x0e\n\x0cperformativeb\x06proto3'
    ),
)


_FIPAMESSAGE_CFP_NOTHING = _descriptor.Descriptor(
    name="Nothing",
    full_name="fetch.aea.fipa.FIPAMessage.CFP.Nothing",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=747,
    serialized_end=756,
)

_FIPAMESSAGE_CFP = _descriptor.Descriptor(
    name="CFP",
    full_name="fetch.aea.fipa.FIPAMessage.CFP",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="bytes",
            full_name="fetch.aea.fipa.FIPAMessage.CFP.bytes",
            index=0,
            number=1,
            type=12,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b(""),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="nothing",
            full_name="fetch.aea.fipa.FIPAMessage.CFP.nothing",
            index=1,
            number=2,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="query_bytes",
            full_name="fetch.aea.fipa.FIPAMessage.CFP.query_bytes",
            index=2,
            number=3,
            type=12,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b(""),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
    ],
    extensions=[],
    nested_types=[_FIPAMESSAGE_CFP_NOTHING,],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[
        _descriptor.OneofDescriptor(
            name="query",
            full_name="fetch.aea.fipa.FIPAMessage.CFP.query",
            index=0,
            containing_type=None,
            fields=[],
        ),
    ],
    serialized_start=640,
    serialized_end=765,
)

_FIPAMESSAGE_PROPOSE = _descriptor.Descriptor(
    name="Propose",
    full_name="fetch.aea.fipa.FIPAMessage.Propose",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="proposal",
            full_name="fetch.aea.fipa.FIPAMessage.Propose.proposal",
            index=0,
            number=1,
            type=12,
            cpp_type=9,
            label=3,
            has_default_value=False,
            default_value=[],
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=767,
    serialized_end=794,
)

_FIPAMESSAGE_ACCEPT = _descriptor.Descriptor(
    name="Accept",
    full_name="fetch.aea.fipa.FIPAMessage.Accept",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=796,
    serialized_end=804,
)

_FIPAMESSAGE_MATCHACCEPT = _descriptor.Descriptor(
    name="MatchAccept",
    full_name="fetch.aea.fipa.FIPAMessage.MatchAccept",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=806,
    serialized_end=819,
)

_FIPAMESSAGE_DECLINE = _descriptor.Descriptor(
    name="Decline",
    full_name="fetch.aea.fipa.FIPAMessage.Decline",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=821,
    serialized_end=830,
)

_FIPAMESSAGE_INFORM = _descriptor.Descriptor(
    name="Inform",
    full_name="fetch.aea.fipa.FIPAMessage.Inform",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="bytes",
            full_name="fetch.aea.fipa.FIPAMessage.Inform.bytes",
            index=0,
            number=1,
            type=12,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b(""),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=832,
    serialized_end=855,
)

_FIPAMESSAGE_ACCEPTWINFORM = _descriptor.Descriptor(
    name="AcceptWInform",
    full_name="fetch.aea.fipa.FIPAMessage.AcceptWInform",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="bytes",
            full_name="fetch.aea.fipa.FIPAMessage.AcceptWInform.bytes",
            index=0,
            number=1,
            type=12,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b(""),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=857,
    serialized_end=887,
)

_FIPAMESSAGE_MATCHACCEPTWINFORM = _descriptor.Descriptor(
    name="MatchAcceptWInform",
    full_name="fetch.aea.fipa.FIPAMessage.MatchAcceptWInform",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="bytes",
            full_name="fetch.aea.fipa.FIPAMessage.MatchAcceptWInform.bytes",
            index=0,
            number=1,
            type=12,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b(""),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=889,
    serialized_end=924,
)

_FIPAMESSAGE = _descriptor.Descriptor(
    name="FIPAMessage",
    full_name="fetch.aea.fipa.FIPAMessage",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="message_id",
            full_name="fetch.aea.fipa.FIPAMessage.message_id",
            index=0,
            number=1,
            type=5,
            cpp_type=1,
            label=1,
            has_default_value=False,
            default_value=0,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="dialogue_starter_reference",
            full_name="fetch.aea.fipa.FIPAMessage.dialogue_starter_reference",
            index=1,
            number=2,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b("").decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="dialogue_responder_reference",
            full_name="fetch.aea.fipa.FIPAMessage.dialogue_responder_reference",
            index=2,
            number=3,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b("").decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="target",
            full_name="fetch.aea.fipa.FIPAMessage.target",
            index=3,
            number=4,
            type=5,
            cpp_type=1,
            label=1,
            has_default_value=False,
            default_value=0,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="cfp",
            full_name="fetch.aea.fipa.FIPAMessage.cfp",
            index=4,
            number=5,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="propose",
            full_name="fetch.aea.fipa.FIPAMessage.propose",
            index=5,
            number=6,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="accept",
            full_name="fetch.aea.fipa.FIPAMessage.accept",
            index=6,
            number=7,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="match_accept",
            full_name="fetch.aea.fipa.FIPAMessage.match_accept",
            index=7,
            number=8,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="decline",
            full_name="fetch.aea.fipa.FIPAMessage.decline",
            index=8,
            number=9,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="inform",
            full_name="fetch.aea.fipa.FIPAMessage.inform",
            index=9,
            number=10,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="accept_w_inform",
            full_name="fetch.aea.fipa.FIPAMessage.accept_w_inform",
            index=10,
            number=11,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="match_accept_w_inform",
            full_name="fetch.aea.fipa.FIPAMessage.match_accept_w_inform",
            index=11,
            number=12,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
    ],
    extensions=[],
    nested_types=[
        _FIPAMESSAGE_CFP,
        _FIPAMESSAGE_PROPOSE,
        _FIPAMESSAGE_ACCEPT,
        _FIPAMESSAGE_MATCHACCEPT,
        _FIPAMESSAGE_DECLINE,
        _FIPAMESSAGE_INFORM,
        _FIPAMESSAGE_ACCEPTWINFORM,
        _FIPAMESSAGE_MATCHACCEPTWINFORM,
    ],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[
        _descriptor.OneofDescriptor(
            name="performative",
            full_name="fetch.aea.fipa.FIPAMessage.performative",
            index=0,
            containing_type=None,
            fields=[],
        ),
    ],
    serialized_start=31,
    serialized_end=940,
)

_FIPAMESSAGE_CFP_NOTHING.containing_type = _FIPAMESSAGE_CFP
_FIPAMESSAGE_CFP.fields_by_name["nothing"].message_type = _FIPAMESSAGE_CFP_NOTHING
_FIPAMESSAGE_CFP.containing_type = _FIPAMESSAGE
_FIPAMESSAGE_CFP.oneofs_by_name["query"].fields.append(
    _FIPAMESSAGE_CFP.fields_by_name["bytes"]
)
_FIPAMESSAGE_CFP.fields_by_name[
    "bytes"
].containing_oneof = _FIPAMESSAGE_CFP.oneofs_by_name["query"]
_FIPAMESSAGE_CFP.oneofs_by_name["query"].fields.append(
    _FIPAMESSAGE_CFP.fields_by_name["nothing"]
)
_FIPAMESSAGE_CFP.fields_by_name[
    "nothing"
].containing_oneof = _FIPAMESSAGE_CFP.oneofs_by_name["query"]
_FIPAMESSAGE_CFP.oneofs_by_name["query"].fields.append(
    _FIPAMESSAGE_CFP.fields_by_name["query_bytes"]
)
_FIPAMESSAGE_CFP.fields_by_name[
    "query_bytes"
].containing_oneof = _FIPAMESSAGE_CFP.oneofs_by_name["query"]
_FIPAMESSAGE_PROPOSE.containing_type = _FIPAMESSAGE
_FIPAMESSAGE_ACCEPT.containing_type = _FIPAMESSAGE
_FIPAMESSAGE_MATCHACCEPT.containing_type = _FIPAMESSAGE
_FIPAMESSAGE_DECLINE.containing_type = _FIPAMESSAGE
_FIPAMESSAGE_INFORM.containing_type = _FIPAMESSAGE
_FIPAMESSAGE_ACCEPTWINFORM.containing_type = _FIPAMESSAGE
_FIPAMESSAGE_MATCHACCEPTWINFORM.containing_type = _FIPAMESSAGE
_FIPAMESSAGE.fields_by_name["cfp"].message_type = _FIPAMESSAGE_CFP
_FIPAMESSAGE.fields_by_name["propose"].message_type = _FIPAMESSAGE_PROPOSE
_FIPAMESSAGE.fields_by_name["accept"].message_type = _FIPAMESSAGE_ACCEPT
_FIPAMESSAGE.fields_by_name["match_accept"].message_type = _FIPAMESSAGE_MATCHACCEPT
_FIPAMESSAGE.fields_by_name["decline"].message_type = _FIPAMESSAGE_DECLINE
_FIPAMESSAGE.fields_by_name["inform"].message_type = _FIPAMESSAGE_INFORM
_FIPAMESSAGE.fields_by_name["accept_w_inform"].message_type = _FIPAMESSAGE_ACCEPTWINFORM
_FIPAMESSAGE.fields_by_name[
    "match_accept_w_inform"
].message_type = _FIPAMESSAGE_MATCHACCEPTWINFORM
_FIPAMESSAGE.oneofs_by_name["performative"].fields.append(
    _FIPAMESSAGE.fields_by_name["cfp"]
)
_FIPAMESSAGE.fields_by_name["cfp"].containing_oneof = _FIPAMESSAGE.oneofs_by_name[
    "performative"
]
_FIPAMESSAGE.oneofs_by_name["performative"].fields.append(
    _FIPAMESSAGE.fields_by_name["propose"]
)
_FIPAMESSAGE.fields_by_name["propose"].containing_oneof = _FIPAMESSAGE.oneofs_by_name[
    "performative"
]
_FIPAMESSAGE.oneofs_by_name["performative"].fields.append(
    _FIPAMESSAGE.fields_by_name["accept"]
)
_FIPAMESSAGE.fields_by_name["accept"].containing_oneof = _FIPAMESSAGE.oneofs_by_name[
    "performative"
]
_FIPAMESSAGE.oneofs_by_name["performative"].fields.append(
    _FIPAMESSAGE.fields_by_name["match_accept"]
)
_FIPAMESSAGE.fields_by_name[
    "match_accept"
].containing_oneof = _FIPAMESSAGE.oneofs_by_name["performative"]
_FIPAMESSAGE.oneofs_by_name["performative"].fields.append(
    _FIPAMESSAGE.fields_by_name["decline"]
)
_FIPAMESSAGE.fields_by_name["decline"].containing_oneof = _FIPAMESSAGE.oneofs_by_name[
    "performative"
]
_FIPAMESSAGE.oneofs_by_name["performative"].fields.append(
    _FIPAMESSAGE.fields_by_name["inform"]
)
_FIPAMESSAGE.fields_by_name["inform"].containing_oneof = _FIPAMESSAGE.oneofs_by_name[
    "performative"
]
_FIPAMESSAGE.oneofs_by_name["performative"].fields.append(
    _FIPAMESSAGE.fields_by_name["accept_w_inform"]
)
_FIPAMESSAGE.fields_by_name[
    "accept_w_inform"
].containing_oneof = _FIPAMESSAGE.oneofs_by_name["performative"]
_FIPAMESSAGE.oneofs_by_name["performative"].fields.append(
    _FIPAMESSAGE.fields_by_name["match_accept_w_inform"]
)
_FIPAMESSAGE.fields_by_name[
    "match_accept_w_inform"
].containing_oneof = _FIPAMESSAGE.oneofs_by_name["performative"]
DESCRIPTOR.message_types_by_name["FIPAMessage"] = _FIPAMESSAGE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

FIPAMessage = _reflection.GeneratedProtocolMessageType(
    "FIPAMessage",
    (_message.Message,),
    dict(
        CFP=_reflection.GeneratedProtocolMessageType(
            "CFP",
            (_message.Message,),
            dict(
                Nothing=_reflection.GeneratedProtocolMessageType(
                    "Nothing",
                    (_message.Message,),
                    dict(
                        DESCRIPTOR=_FIPAMESSAGE_CFP_NOTHING,
                        __module__="fipa_pb2"
                        # @@protoc_insertion_point(class_scope:fetch.aea.fipa.FIPAMessage.CFP.Nothing)
                    ),
                ),
                DESCRIPTOR=_FIPAMESSAGE_CFP,
                __module__="fipa_pb2"
                # @@protoc_insertion_point(class_scope:fetch.aea.fipa.FIPAMessage.CFP)
            ),
        ),
        Propose=_reflection.GeneratedProtocolMessageType(
            "Propose",
            (_message.Message,),
            dict(
                DESCRIPTOR=_FIPAMESSAGE_PROPOSE,
                __module__="fipa_pb2"
                # @@protoc_insertion_point(class_scope:fetch.aea.fipa.FIPAMessage.Propose)
            ),
        ),
        Accept=_reflection.GeneratedProtocolMessageType(
            "Accept",
            (_message.Message,),
            dict(
                DESCRIPTOR=_FIPAMESSAGE_ACCEPT,
                __module__="fipa_pb2"
                # @@protoc_insertion_point(class_scope:fetch.aea.fipa.FIPAMessage.Accept)
            ),
        ),
        MatchAccept=_reflection.GeneratedProtocolMessageType(
            "MatchAccept",
            (_message.Message,),
            dict(
                DESCRIPTOR=_FIPAMESSAGE_MATCHACCEPT,
                __module__="fipa_pb2"
                # @@protoc_insertion_point(class_scope:fetch.aea.fipa.FIPAMessage.MatchAccept)
            ),
        ),
        Decline=_reflection.GeneratedProtocolMessageType(
            "Decline",
            (_message.Message,),
            dict(
                DESCRIPTOR=_FIPAMESSAGE_DECLINE,
                __module__="fipa_pb2"
                # @@protoc_insertion_point(class_scope:fetch.aea.fipa.FIPAMessage.Decline)
            ),
        ),
        Inform=_reflection.GeneratedProtocolMessageType(
            "Inform",
            (_message.Message,),
            dict(
                DESCRIPTOR=_FIPAMESSAGE_INFORM,
                __module__="fipa_pb2"
                # @@protoc_insertion_point(class_scope:fetch.aea.fipa.FIPAMessage.Inform)
            ),
        ),
        AcceptWInform=_reflection.GeneratedProtocolMessageType(
            "AcceptWInform",
            (_message.Message,),
            dict(
                DESCRIPTOR=_FIPAMESSAGE_ACCEPTWINFORM,
                __module__="fipa_pb2"
                # @@protoc_insertion_point(class_scope:fetch.aea.fipa.FIPAMessage.AcceptWInform)
            ),
        ),
        MatchAcceptWInform=_reflection.GeneratedProtocolMessageType(
            "MatchAcceptWInform",
            (_message.Message,),
            dict(
                DESCRIPTOR=_FIPAMESSAGE_MATCHACCEPTWINFORM,
                __module__="fipa_pb2"
                # @@protoc_insertion_point(class_scope:fetch.aea.fipa.FIPAMessage.MatchAcceptWInform)
            ),
        ),
        DESCRIPTOR=_FIPAMESSAGE,
        __module__="fipa_pb2"
        # @@protoc_insertion_point(class_scope:fetch.aea.fipa.FIPAMessage)
    ),
)
_sym_db.RegisterMessage(FIPAMessage)
_sym_db.RegisterMessage(FIPAMessage.CFP)
_sym_db.RegisterMessage(FIPAMessage.CFP.Nothing)
_sym_db.RegisterMessage(FIPAMessage.Propose)
_sym_db.RegisterMessage(FIPAMessage.Accept)
_sym_db.RegisterMessage(FIPAMessage.MatchAccept)
_sym_db.RegisterMessage(FIPAMessage.Decline)
_sym_db.RegisterMessage(FIPAMessage.Inform)
_sym_db.RegisterMessage(FIPAMessage.AcceptWInform)
_sym_db.RegisterMessage(FIPAMessage.MatchAcceptWInform)


# @@protoc_insertion_point(module_scope)
