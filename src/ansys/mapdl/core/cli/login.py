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

"""Login into a PyHPS cluster"""
from getpass import getpass
import logging

import click

logger = logging.getLogger()


@click.command(
    name="login",
    short_help="Login into an HPS cluster.",
    help="""Login into an HPS cluster.

It does store credentials (cluster url, password and username) in the OS credential manager.
If you want to change any credential, just issue the command again with the new values.

""",
)
@click.option("--user", default=None, type=str, help="The username to login.")
@click.option("--password", default=None, type=str, help="The password to login.")
@click.option(
    "--url",
    default=None,
    type=str,
    help="The HPS cluster URL. For instance 'https://10.231.106.1:3000/hps'.",
)
@click.option(
    "--default",
    default=False,
    type=bool,
    is_flag=False,
    flag_value=True,
    help="""Set the default user, password and URL. These credentials are not tested.""",
)
@click.option(
    "--test_token",
    default=False,
    type=bool,
    is_flag=False,
    flag_value=True,
    help="""Test if the token is valid. This argument is ignored if '--default' argument is ``True``.""",
)
def login(user, password, url, default, test_token):
    """
    Command Line Interface for logging in and getting an access token.

    Parameters
    user (str): Username for login
    password (str): Password for login
    default (bool): If used, the input data is set as default and it will be used for any login which does not specify the url, user or password.
    """
    if not default:
        logger.debug("Storing non-default credentials.")
        if not user and not click.prompt("Username: "):
            raise ValueError("No user was provided.")

        if not password and not getpass("Password: "):
            raise ValueError("No password was provided.")

        if not url and not click.prompt("HPS cluster URL: "):
            raise ValueError("No password was provided.")

        try:
            token = login(user, password, url)
            click.echo(f"Login successful")
        except Exception as e:
            click.echo(f"Login failed: {str(e)}")

        if test_token:
            logger.debug("Testing token")
            from requests import ConnectionError

            from ansys.mapdl.core.hpc.login import token_is_valid

            if not token_is_valid(token):
                raise ConnectionError("The retrieved token is not valid.")

    logger.info(f"Stored credentials: {user}, {password}, {url}")
    store_credentials(user, password, url)


@click.command(
    short_help="Logout from an HPS cluster.",
    help="""Logout from an HPS cluster.

It deletes credentials stored on the system.

""",
)
@click.option(
    "--url",
    prompt="HPS cluster URL",
    help="The HPS cluster URL. For instance 'https://10.231.106.1:3000/hps'.",
    default=None,
    type=str,
)
@click.option(
    "--default",
    default=False,
    type=bool,
    is_flag=False,
    flag_value=True,
    help="""Whether PyMAPDL is to print debug logging to the console.""",
)
def logout(url, default):

    # TODO: keyrings library seems to not being able to list the credentials
    # under a service name. We might need to keep track of those in a file or
    # something.

    from ansys.mapdl.core.hpc.login import delete_credentials

    if not url and not default:
        raise ValueError("An URL needs to be used.")

    if url and default:
        raise ValueError("The argument '--default' cannot be used with an URL.")

    if default:
        url = "default"

    delete_credentials(url)
    click.echo(f"The credentials for '{url}' have been deleted.")
