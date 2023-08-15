import re
import string
from typing import Protocol

from CreatorPipeline.constants import DEFAULTS


class Identifier(Protocol):
    """Identifies an episode"""
    value: str
    col: int

    def expression(self) -> re.Pattern:
        """Returns a regex pattern that matches the episode"""
        return re.compile(rf"({self.value})")


class NumericIdentifier:
    """Identifies an episode by its number"""
    def __init__(self, value):
        self.value = value
        self.col = DEFAULTS.id_col_numeric

    def expression(self) -> re.Pattern:
        """Returns a regex pattern that matches the episode number"""
        ...


class TitleIdentifier:
    """Identifies an episode by its title"""
    def __init__(self, value):
        self.value = value
        self.col = DEFAULTS.id_col_title

    def expression(self) -> re.Pattern:
        """Returns a regex pattern that matches the episode title"""
        return re.compile(rf"({self.value})")


class HashIdentifier:
    """Identifies an episode by its hash"""
    def __init__(self, value):
        self.value = value
        self.col = DEFAULTS.id_col_hash

    def expression(self) -> re.Pattern:
        """Returns a regex pattern that matches the episode hash"""
        return re.compile(rf"({self.value})")


class ShorthandIdentifier:
    """Identifies an episode by its shorthand"""
    def __init__(self, value):
        self.value = value
        self.col = DEFAULTS.id_col_shorthand

    def expression(self) -> re.Pattern:
        """Returns a regex pattern that matches the episode shorthand"""
        return re.compile(rf"({self.value})")


def identifier_factory(value: str) -> Identifier:
    """Returns an Identifier object based on the value provided"""
    value = str(value).strip()
    if any(x in value for x in string.whitespace):
        print("TitleIdentifier")
        print(value)
        return TitleIdentifier(value)
    if "_" in value:
        print("ShorthandIdentifier")
        return ShorthandIdentifier(value)
    if value.isnumeric() and len(str(value)) < 4:
        print("NumericIdentifier")
        return NumericIdentifier(value)
    if value.isalnum():
        print("HashIdentifier")
        return HashIdentifier(value)
    print(f"ISSUE EPISODE ID: {value}")
    raise EpisodeError


class EpisodeError(Exception):
    """Raised when an episode cannot be identified"""
    ...
