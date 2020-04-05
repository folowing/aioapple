import datetime
import jwt
import asyncio
import json

from .exception import (
    AioAppleTimeoutError,
    AioAppleAuthError,
)


class AioAppleAuth:

    def __get_client_secret(self):
        headers = {
            'kid': self.key_id,
        }

        now = datetime.datetime.now(datetime.timezone.utc)
        payload = {
            'iss': self.team_id,
            'iat': now,
            'exp': now + datetime.timedelta(days=180),
            'aud': 'https://appleid.apple.com',
            'sub': self.bundle_id,
        }

        client_secret = jwt.encode(
            payload,
            self.key_content,
            algorithm='ES256',
            headers=headers
        ).decode("utf-8")
        return client_secret

    async def get_user_info(self, access_token, redirect_uri=None):
        """
        :param access_token:
        :param redirect_uri:
        :return: { 'uid': 'xxxx', 'email'?: 'yyyy'}
        """
        client_secret = self.__get_client_secret()
        params = {
            'client_id': self.bundle_id,
            'client_secret': client_secret,
            'grant_type': 'authorization_code',
            'code': access_token,
            'redirect_uri': '',
        }

        access_token_url = 'https://appleid.apple.com/auth/token'

        try:
            async with self._session.post(access_token_url, params=params,
                                          timeout=self.timeout) as resp:
                resp_text = await resp.text()
                result = json.loads(resp_text)
                print(result)
                if 'error' in result:
                    raise AioAppleAuthError(result)
                id_token = result.get('id_token')
                if id_token:
                    decoded = jwt.decode(id_token, '', verify=False)
                    uid = decoded.get('sub')
                    if not uid:
                        raise AioAppleAuthError('uid not found')
                    email = decoded.get('email')
                    result = {
                        'uid': uid
                    }
                    if email:
                        result['email']: email
                    return result

        except asyncio.TimeoutError:
            raise AioAppleTimeoutError()

