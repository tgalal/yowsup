from .identitykeystore import IdentityKeyStore
from .prekeystore import PreKeyStore
from .sessionstore import SessionStore
from .signedprekeystore import SignedPreKeyStore
import abc
class AxolotlStore(IdentityKeyStore, PreKeyStore, SignedPreKeyStore, SessionStore):
    __metaclass__ = abc.ABCMeta