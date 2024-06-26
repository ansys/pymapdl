# Copyright (C) 2024 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import logging
import time

try:
    from ansys.hps.client import AuthApi, Client
    from ansys.hps.client.authenticate import authenticate
    import keyring
    from requests import ConnectionError
except ModuleNotFoundError:
    raise ModuleNotFoundError(
        """Some of the dependencies required for login into an HPS cluster are not installed.
Please install them using "pip install 'ansys-mapdl-core[hps]"."""
    )

DEFAULT_IDENTIFIER = "defaultconfig"
SERVICE_NAME = "pymapdl-pyhps"
EXPIRATION_TIME = 4 * 24 * 60  # 2 days in minutes

logger = logging.getLogger()
# logging.basicConfig(
#     level=logging.DEBUG,
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#     # handlers=[
#     #     logging.FileHandler("pymapdl.log"),
#     #     logging.StreamHandler()
#     # ]
# )


def get_password(*args, **kwargs):
    logger.debug(f"Getting password from service '{args[0]}' and key '{args[1]}'")
    return keyring.get_password(*args, **kwargs)


def set_password(*args, **kwargs):
    logger.debug(f"Setting password from service '{args[0]}' and key '{args[1]}'")
    return keyring.set_password(*args, **kwargs)


def login_in_cluster(user, password, url):
    """
    Authenticate with the server and return the access token.

    Parameters
    ----------
    user : str
        Username.
    password : str
        Password.
    url : str
        URL.

    Returns
    -------
    str
        Access token.
    """
    logger.debug(f"Authenticating on cluster '{url}' using user '{user}'.")
    access_token = authenticate(
        url=url, username=user, password=password, scope="openid", verify=False
    )["access_token"]
    return access_token


def store_credentials(
    user: str = None,
    password: str = None,
    url: str = None,
    default=False,
    expiration_time: float = EXPIRATION_TIME,
):
    """
    Store user credentials and the current timestamp in the keyring.

    If ``default`` argument is ``True``, you can store a default password,
    default user, or/and default URL.

    Parameters
    ----------
    user : str, optional
        Username.
    password : str, optional
        Password
    url : str, optional
        URL of the HPS cluster

    """
    if default:
        identifier = DEFAULT_IDENTIFIER
    else:
        identifier = url
    logger.debug(f"Using identifier: '{identifier}'")

    if not default and (not url or not user or not password):
        raise ValueError(
            "To store non-default credentials, an URL, an user and a password are needed."
        )

    if url:
        set_password(SERVICE_NAME, f"{identifier}_url", url)
    if user:
        set_password(SERVICE_NAME, f"{identifier}_user", user)
    if password:
        set_password(SERVICE_NAME, f"{identifier}_password", password)
    if expiration_time:
        set_password(
            SERVICE_NAME, f"{identifier}_expiration_time", str(expiration_time)
        )

    set_password(SERVICE_NAME, f"{identifier}_timestamp", str(time.time()))


def get_stored_credentials(identifier):
    """
    Retrieve stored credentials and timestamp from the keyring.

    Returns:
    tuple: (user, password, timestamp) or (None, None, None) if not found
    """
    logger.debug(f"Retrieving info for '{identifier}'")
    url = get_password(SERVICE_NAME, f"{identifier}_url")
    user = get_password(SERVICE_NAME, f"{identifier}_user")
    password = get_password(SERVICE_NAME, f"{identifier}_password")
    timestamp = get_password(SERVICE_NAME, f"{identifier}_timestamp")
    expiration_time = get_password(SERVICE_NAME, f"{identifier}_expiration_time")

    if timestamp:
        timestamp = float(timestamp)
    if expiration_time:
        expiration_time = float(expiration_time)

    logger.debug(
        f"Retrieved info for '{identifier}': {url}, {user}, {password}, {timestamp}, {expiration_time} "
    )
    return url, user, password, timestamp, expiration_time


def credentials_expired(timestamp, expiration_time: float = EXPIRATION_TIME):
    """
    Check if the stored credentials have expired.

    Parameters:
    timestamp (float): Timestamp of when the credentials were stored

    Returns:
    bool: True if credentials have expired, False otherwise
    """
    return time.time() - timestamp > expiration_time * 60


def delete_credentials(identifier=None):
    if not identifier:
        identifier = DEFAULT_IDENTIFIER

    logger.debug(f"Deleting credentials for identifier: {identifier}")

    keyring.delete_password(SERVICE_NAME, f"{identifier}_url")
    keyring.delete_password(SERVICE_NAME, f"{identifier}_user")
    keyring.delete_password(SERVICE_NAME, f"{identifier}_password")
    keyring.delete_password(SERVICE_NAME, f"{identifier}_timestamp")
    keyring.delete_password(SERVICE_NAME, f"{identifier}_expiration_time")


def token_is_valid(url, token):
    client = Client(url=url, access_token=token, verify=False)
    auth_api = AuthApi(client)

    try:
        auth_api.get_users()
        return True
    except ConnectionError:
        return False
    except Exception as e:
        raise e


def access(url: str = None, user: str = None, password: str = None):

    if not url or not user or not password:
        if not url:
            identifier = DEFAULT_IDENTIFIER
        else:
            identifier = url

        (
            url_default,
            user_default,
            password_default,
            timestamp_default,
            expiration_default,
        ) = get_stored_credentials(identifier=identifier)

        if not url_default or not user_default or not password_default:
            raise ConnectionError(
                f"There are no credentials stored for '{identifier}'."
            )

        if credentials_expired(timestamp_default, expiration_time=expiration_default):
            delete_credentials(identifier)

            raise ConnectionError(f"The stored '{identifier}' credentials are expired.")

    if not url:
        if url_default:
            url = url_default
        else:
            raise ValueError(
                f"No 'URL' is given nor stored for '{identifier}'. You must input one."
            )

    if not user:
        if user_default:
            user = user_default
        else:
            raise ValueError(
                f"No 'user' is given nor stored for '{identifier}'. You must input one."
            )

    if not password:
        if password_default:
            password = password_default
        else:
            raise ValueError(
                f"No 'password' is given nor stored for '{identifier}'. You must input one."
            )

    return login_in_cluster(user=user, password=password, url=url)


def get_default_url():
    """Return the default URL"""
    return get_password(SERVICE_NAME, f"{DEFAULT_IDENTIFIER}_url")


def get_token(url: str = None, user: str = None, password: str = None):
    """Wrapper around `access`` function"""
    return access(url=url, user=user, password=password)
