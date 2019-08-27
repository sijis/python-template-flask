
import uuid

from flask.views import MethodView
from structlog import get_logger


# pylint: disable=no-self-use
class BaseAPI(MethodView):

    endpoint = 'base'

    def __init__(self):
        logger = get_logger()
        self.uuid = str(uuid.uuid4())
        self.log = logger.new(request_id=self.uuid, endpoint=self.endpoint)
