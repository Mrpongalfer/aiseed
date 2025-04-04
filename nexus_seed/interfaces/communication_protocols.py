from enum import Enum

class CommunicationModes(Enum):
    TEXT = "TEXT"
    SYMBOLIC = "SYMBOLIC"
    ENCODED = "ENCODED"

class CommunicationProtocols(Enum):
    JSON = "JSON"
    XML = "XML"
    BINARY = "BINARY"
