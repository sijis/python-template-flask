"""Base Plugin class."""
from abc import ABC, abstractmethod, abstractproperty
from uuid import uuid4

from structlog import get_logger


class BasePlugin(ABC):
    """All Plugins should inherit from this base class."""

    def __init__(self, uuid=None):
        logger = get_logger()
        self.uuid = uuid or str(uuid4())
        self.log = logger.new(request_id=self.uuid, parser=self.name)
        self.data = None

    @abstractproperty
    def resource(self):
        """Implement the resource property."""

    @abstractproperty
    def name(self):
        """Implement the provider property."""

    @abstractmethod
    def match(self, data):
        """Implement the Resource match operation."""

    @abstractmethod
    def parse(self, data):
        """Implement the Resource parse operation."""

    @abstractmethod
    def create(self):
        """Implement the Resource create operation."""
