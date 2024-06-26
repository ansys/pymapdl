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

logger = logging.getLogger()

# logging.basicConfig(
#     level=logging.DEBUG,
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#     # handlers=[
#     #     logging.FileHandler("pymapdl.log"),
#     #     logging.StreamHandler()
#     # ]
# )


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
@click.option(
    "--quiet",
    default=False,
    type=bool,
    is_flag=False,
    flag_value=True,
    help="""Suppress al console printout.""",
)
def login(
    user: Optional[str] = None,
    password: Optional[str] = None,
    url: Optional[str] = None,
    default: bool = False,
    test_token: bool = False,
    quiet: bool = False,
):
    """
    Command Line Interface for logging in and getting an access token.

    Parameters
    user (str): Username for login
    password (str): Password for login
    default (bool): If used, the input data is set as default and it will be used for any login which does not specify the url, user or password.
    """
    from ansys.mapdl.core.hpc.login import login_in_cluster, store_credentials

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
def logout(url, default):

    # TODO: keyrings library seems to not being able to list the credentials
    # under a service name. We might need to keep track of those in a file or
    # something.

    import keyring

    from ansys.mapdl.core.hpc.login import delete_credentials

    if not url and not default:
        raise ValueError("An URL needs to be used.")

    if url and default:
        raise ValueError("The argument '--default' cannot be used with an URL.")

    if default:
        logger.debug("Deleting credentials for the default profile.")
        url = None

    try:
        delete_credentials(url)
    except keyring.errors.PasswordDeleteError:
        click.echo("The default credentials do not exist.")
        return

    if default:
        click.echo(f"The default credentials have been deleted.")
    else:
        click.echo(f"The credentials for the HPS cluster '{url}' have been deleted.")


if __name__ == "__main__":
    # login(default=True)
    # user, password, url, default, test_token, quiet
    login(
        user="repuser",
        password="repuser",
        url="https://10.231.106.32:3000/hps",
        default=False,
        test_token=True,
        quiet=True,
    )
