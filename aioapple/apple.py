import aiohttp

from .auth import AioAppleAuth


class AioApple(AioAppleAuth):

    def __init__(self, key_id, key_content, team_id, bundle_id,
                 timeout=5):
        """
        :param key_id: Private Key ID, for sign check
        :param key_content: Private Key Content, load from file which is downloaded from apple
        :param team_id: Team ID
        :param bundle_id: Bundle ID
        """
        conn = aiohttp.TCPConnector(limit=1024)
        self._session = aiohttp.ClientSession(
            connector=conn,
            skip_auto_headers={'Content-Type'},
        )
        self.key_id = key_id
        self.key_content = key_content
        self.team_id = team_id
        self.bundle_id = bundle_id
        self.timeout = timeout

    def __del__(self):
        if not self._session.closed:
            if self._session._connector is not None \
                    and self._session._connector_owner:
                self._session._connector.close()
            self._session._connector = None
