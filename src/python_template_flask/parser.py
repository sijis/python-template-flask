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
            'parsed': None,
        }
        body = response['received']

        if not body:
            msg = 'No data received.'
            self.log.debug(msg=msg)
            response['warning'] = msg
            return flask.make_response(flask.jsonify(response), 422)

        all_parsers = self._determine_parser(body)

        for parser in all_parsers:
            plugin_found = False
            try:
                manager = get_plugin('parsers', parser)
                plugin_found = True
            except ModuleNotFoundError as error:
                msg = 'Plugin {} not found.'.format(parser)
                self.log.error(msg=msg, error=error)
                response['warning'] = msg

            if plugin_found:
                parser = manager.EventParser(uuid=self.uuid)
                parser.parse(body)
                parsed = parser.create()
                response['parsed'] = parsed

        return flask.jsonify(**response)

    def _determine_parser(self, body):
        """Attempt to determine the correct parser."""
        parser_prefix = 'mirror'

        found_prefix = body.get('parser', None)
        if found_prefix:
            parser_prefix = found_prefix

        return get_plugins('parsers', parser_prefix)
