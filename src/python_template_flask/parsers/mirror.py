"""Event Parser."""
from .common import BasePlugin


# pylint: disable=abstract-method
class EventParser(BasePlugin):
    """Event Parser for events."""

    resource = 'parser'
    name = 'mirror'

    def match(self, data):
        return True

    def parse(self, data):
        self.log.info(data)
        self.data = data
        return self.data

    def create(self):
        return self.data
