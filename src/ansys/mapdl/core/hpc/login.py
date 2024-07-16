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
from typing import Optional

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


def get_stored_credentials(identifier: str):
    """
    Retrieve stored credentials, timestamp and expiration time from the keyring.

    Parameters
    ----------
    identifier: str
        Identifier for the credentials

    Returns
    -------
    tuple
        (user, password, timestamp) or (None, None, None) if not found
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


def credentials_expired(timestamp: float, expiration_time: float = EXPIRATION_TIME):
    """
    Check if the stored credentials have expired.

    Parameters
    ----------
    timestamp, float
        Timestamp of when the credentials were stored

    expiration_time float
        Amount of time before the credentials expires.

    Returns
    -------
    bool
        True if credentials have expired, False otherwise
    """
    return time.time() - timestamp > expiration_time * 60


def delete_credentials(identifier: Optional[str] = None):
    """
    Delete stored credentials.

    Parameters
    ----------
    identifier: str, Optional
        Identifier for the credentials. If it is ``None``, the
        default credentials are deleted.

    Returns
    -------
    None
    """
    if not identifier:
        identifier = DEFAULT_IDENTIFIER

    logger.debug(f"Deleting credentials for identifier: {identifier}")

    keyring.delete_password(SERVICE_NAME, f"{identifier}_url")
    keyring.delete_password(SERVICE_NAME, f"{identifier}_user")
    keyring.delete_password(SERVICE_NAME, f"{identifier}_password")
    keyring.delete_password(SERVICE_NAME, f"{identifier}_timestamp")
    keyring.delete_password(SERVICE_NAME, f"{identifier}_expiration_time")


def token_is_valid(url, token):
    """Check if a token is valid.

    The validation is performed by requesting the number of users to the HPS cluster.

    Parameters
    ----------
    url : str
        HPS cluster URL.
    token : str
        Authentication token.

    Returns
    -------
    bool
        Whether the token is valid or not.
    """
    client = Client(url=url, access_token=token, verify=False)
    auth_api = AuthApi(client)

    try:
        auth_api.get_users()
        return True
    except ConnectionError:
        return False
    except Exception as e:
        raise e


def get_token_access(url: str = None, user: str = None, password: str = None):
    """
    Access an HPS cluster by logging in with the provided or stored credentials.

    This function attempts to log in to a cluster using the provided URL, username,
    and password.
    If any of these parameters are not provided, it attempts to retrieve stored
    credentials associated with the given URL.
    If no URL is provided, then it retrieves the default credentials.

    If the credentials are expired or not found, appropriate errors are raised.

    Parameters
    ----------
    url : str, optional
        The URL of the cluster to log in to. If not provided, a stored URL
        associated with the default or given identifier is used.
    user : str, optional
        The username for logging in. If not provided, a stored username associated
        with the default or given identifier is used.
    password : str, optional
        The password for logging in. If not provided, a stored password associated
        with the default or given identifier is used.

    Returns
    -------
    str
        It returns the authentication token for the session.

    Raises
    ------
    ConnectionError
        If there are no stored credentials for the given identifier, or if the stored credentials
        are expired.
    ValueError
        If a URL, username, or password is not provided and cannot be found in the stored
        credentials.

    Notes
    -----
    - If credentials are expired, they are deleted from storage.
    - The credentials can be stored using ``pymapdl login`` CLI.
      Alternatively you can use ``store_credentials`` as:

      .. code:: py

         from ansys.mapdl.core.hpc.login import store_credentials

         user = "myuser"
         password = "mypass"
         url = "https://cluster.example.com"
         store_credentials(user, password, url)


    Examples
    --------
    Using url, user and password:

    >>> get_token_access(url='https://cluster.example.com', user='admin', password='securepass')
    'eyJhbGciOiJSUzI1NiIsI...'

    Using the stored credential for that URL. If those credentials do not exists,
    the default credentials are used.

    >>> get_token_access(url='https://cluster.example.com')
    'bGciOiJSeyJhUzI1NiIsI...'

    Login using the default stored credentials:
    >>> get_token_access()
    'iJSeyJhUzI1bGciONiIsI...'
    """
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
    """Return the default credentials URL"""
    return get_password(SERVICE_NAME, f"{DEFAULT_IDENTIFIER}_url")
