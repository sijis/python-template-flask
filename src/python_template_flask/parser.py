import flask

from .base_api import BaseAPI
from .plugin_manager import get_plugin, get_plugins


# pylint: disable=no-self-use
class ParserAPI(BaseAPI):

    endpoint = 'parser'

    def post(self):
        """Handle post."""
        response = {
            'received': flask.request.json,
            'warning': None,
            'parsed': {},
        }
        body = response['received']

        if not body:
            msg = 'No data received.'
            self.log.debug(msg=msg)
            response['warning'] = msg
            return flask.make_response(flask.jsonify(response), 422)

        plugins = get_plugins(plugin_dir='parsers')
        for plugin in plugins:
            if plugin == 'common':
                continue

            manager = get_plugin('parsers', plugin)
            parser = manager.EventParser(uuid=self.uuid)
            if parser.match(data=body):
                parser.parse(body)
                parsed = parser.create()
                response['parsed'][plugin] = parsed

        return flask.jsonify(**response)
