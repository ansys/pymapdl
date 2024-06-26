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
from typing import Optional

import click

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger()


@click.command(
    name="login",
    short_help="Login into an HPS cluster.",
    help="""Login into an HPS cluster.

It does store credentials (cluster url, password and username) in the OS credential manager.
If you want to change any credential, just issue the command again with the new values.

Examples
--------

Prompt the values for user, password and HPC cluster URL:

$ pymapdl login
Username: myuser
Password: mypassword
HPS cluster URL: https://123.456.789.1:3000/hps
Stored credentials:
  User        : 'user'
  Cluster URL : 'https://123.456.789.1:3000/hps'

Use the CLI arguments to supply the values

$ pymapdl login --user myuser --password mypassword --url "https://123.456.789.1:3000/hps"
Stored credentials:
  User        : 'user'
  Cluster URL : 'https://123.456.789.1:3000/hps'

Set the defaults user, password and URL. They will be used when one of them is
missing.

$ pymapdl login --default --user myuser --password mypassword --url "https://123.456.789.1:3000/hps"
Stored default credentials.

It is possible to input some arguments using the CLI arguments, and other using
the prompt:

$ pymapdl login --user myuser --url "https://123.456.789.1:3000/hps"
Password: mypassword
Stored credentials:
  User        : 'user'
  Cluster URL : 'https://123.456.789.1:3000/hps'

""",
)
@click.option("--user", default=None, type=str, help="The username to login.")
@click.option("--password", default=None, type=str, help="The password to login.")
@click.option(
    "--url",
    default=None,
    type=str,
    help="The HPS cluster URL. For instance 'https://123.456.789.1:3000/hps'.",
)
@click.option(
    "--default",
    default=False,
    type=bool,
    is_flag=False,
    flag_value=True,
    help="""Set the default user, password and URL. These credentials are not tested against any HPC.""",
)
@click.option(
    "--test_token",
    default=False,
    type=bool,
    is_flag=False,
    flag_value=True,
    help="""Test if the token is valid. This argument is ignored if '--default' argument is ``True``.""",
)
@click.option(
    "--quiet",
    default=False,
    type=bool,
    is_flag=False,
    flag_value=True,
    help="""Suppress all console printout.""",
)
@click.option(
    "--debug",
    default=False,
    type=bool,
    is_flag=False,
    flag_value=True,
    help="""Activate debugging printout. It might show the input password!""",
)
def login(
    user: Optional[str] = None,
    password: Optional[str] = None,
    url: Optional[str] = None,
    default: bool = False,
    test_token: bool = False,
    quiet: bool = False,
    debug: bool = False,
):
    from ansys.mapdl.core.hpc.login import login_in_cluster, store_credentials

    if debug:
        logger.setLevel(logging.DEBUG)

    if quiet:
        import urllib3

        urllib3.disable_warnings()

    logger.debug("Storing non-default credentials.")
    if not user:
        user = click.prompt("Username")

        if not user:
            raise ValueError("No user was provided.")

    if not password:
        password = getpass("Password: ")
        if not password:
            raise ValueError("No password was provided.")

    if not default and not url:
        url = click.prompt("HPS cluster URL")
        if not url:
            raise ValueError("No password was provided.")

    token = login_in_cluster(user, password, url)
    logger.debug(f"Login successful")

    if test_token:
        logger.debug("Testing token")
        from requests import ConnectionError

        from ansys.mapdl.core.hpc.login import token_is_valid

        if not token_is_valid(url, token):
            raise ConnectionError("The retrieved token is not valid.")
        else:
            if not quiet:
                click.echo("Token has been verified with the HPC cluster.")

    logger.info(f"Stored credentials: {user}, {password}, {url}")
    store_credentials(user, password, url, default=default)

    if not quiet:
        if default:
            click.echo("Stored default credentials.")
        else:
            click.echo(
                f"Stored credentials:\n  User        : '{user}'\n  Cluster URL : '{url}'"
            )


@click.command(
    short_help="Logout from an HPS cluster.",
    help="""Logout from an HPS cluster.

It deletes credentials stored on the system.

Examples
--------

Delete the credentials associated to an specific URL

$ pymapdl logout --url "https://123.456.789.1:3000/hps"
The HPS cluster 'https://123.456.789.1:3000/hps' credentials have been deleted.

Delete the default credentials.

$ pymapdl logout --default
The default credentials have been deleted.

Notes
-----
- If the credentials do not exist, the CLI notifies and exits cleanly.
  No exception is raised. If you want to raise an exception (exit 1), then pass
  the argument ``--strict``.
""",
)
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
    help="""Deletes the default login configuration.""",
)
@click.option(
    "--quiet",
    default=False,
    type=bool,
    is_flag=False,
    flag_value=True,
    help="""Suppress all console printout.""",
)
@click.option(
    "--debug",
    default=False,
    type=bool,
    is_flag=False,
    flag_value=True,
    help="""Activate debugging printout.""",
)
@click.option(
    "--strict",
    default=False,
    type=bool,
    is_flag=False,
    flag_value=True,
    help="""Raise an issue if the credentials do not exist.""",
)
def logout(url, default, quiet, debug, strict):

    # TODO: keyrings library seems to not being able to list the credentials
    # under a service name. We might need to keep track of those in a file or
    # something.

    import keyring

    from ansys.mapdl.core.hpc.login import delete_credentials

    if debug:
        logger.setLevel(logging.DEBUG)

    if not url and not default:
        raise ValueError("An URL needs to be used.")

    if url and default:
        raise ValueError("The argument '--default' cannot be used with an URL.")

    if default:
        logger.debug("Deleting credentials for the default profile.")
        url = None

    try:
        delete_credentials(url)
        success_message = "The {0} credentials have been deleted.".format(
            "default" if default else f"HPS cluster '{url}'"
        )
    except keyring.errors.PasswordDeleteError:
        success_message = "The {0} credentials do not exist.".format(
            "default" if default else f"HPS cluster '{url}'"
        )
        if strict:
            raise keyring.errors.PasswordDeleteError(success_message)

    if not quiet:
        click.echo(success_message)
