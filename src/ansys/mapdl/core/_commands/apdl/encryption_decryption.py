# Copyright (C) 2016 - 2025 ANSYS, Inc. and/or its affiliates.
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

from ansys.mapdl.core._commands import CommandsBase


class EncryptionDecryption(CommandsBase):

    def dbdecrypt(
        self,
        keya: str = "",
        keyb: str = "",
        datatype: str = "",
        num1: str = "",
        num2: str = "",
        inc: str = "",
        **kwargs,
    ):
        r"""Controls decryption of material data in the database file.

        Mechanical APDL Command: `/DBDECRYPT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_DBDECRYPT.html>`_

        Parameters
        ----------
        keya : str
            Decryption key A (32-character maximum). This key is used to decrypt the data in a one-level
            encryption or to control access to the data in a two-level encryption. Leave this field blank if
            you do not have key A.

        keyb : str
            Decryption key B (32-character maximum). This key is used to decrypt the data in a two-level
            encryption. Leave this field blank if the database file is encrypted with one-level encryption.

        datatype : str
            Type of data to decrypt. Must be set to MAT for material data.

        num1 : str
            Decrypt materials from material number ``NUM1`` to ``NUM2`` (defaults to ``NUM1`` ) in steps of
            ``INC`` (defaults to 1). If ``NUM1`` = ALL (default), ``NUM2`` and ``INC`` are ignored.

        num2 : str
            Decrypt materials from material number ``NUM1`` to ``NUM2`` (defaults to ``NUM1`` ) in steps of
            ``INC`` (defaults to 1). If ``NUM1`` = ALL (default), ``NUM2`` and ``INC`` are ignored.

        inc : str
            Decrypt materials from material number ``NUM1`` to ``NUM2`` (defaults to ``NUM1`` ) in steps of
            ``INC`` (defaults to 1). If ``NUM1`` = ALL (default), ``NUM2`` and ``INC`` are ignored.

        Notes
        -----

        .. _s-DBDECRYPT_notes:

        This command decrypts data in the database file. It must be issued before resuming the database file
        ( :ref:`resume` command). Only ``KeyA`` is required for a one-level encryption. For a `two-level
        encryption
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_apdl/apdl_encryptmat.html#partial_access>`_,
        inputting ``KeyB`` gives you partial access to the data. Inputting both ``KeyA`` and ``KeyB`` gives
        you full access.

        For more information about using :ref:`dbdecrypt` in the encryption/decryption procedure, see
        `Encrypting Material Data
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_apdl/apdl_encryptmat.html#apdl_encryptsteps_mat>`_
        :ref:`dbencrypt` command.

        This command is valid in any processor.
        """
        command = f"/DBDECRYPT,{keya},{keyb},{datatype},{num1},{num2},{inc}"
        return self.run(command, **kwargs)

    def dbencrypt(
        self,
        keya: str = "",
        keyb: str = "",
        datatype: str = "",
        num1: str = "",
        num2: str = "",
        inc: str = "",
        **kwargs,
    ):
        r"""Controls encryption of material data in the database file.

        Mechanical APDL Command: `/DBENCRYPT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_DBENCRYPT.html>`_

        Parameters
        ----------
        keya : str
            Encryption key A (32-character maximum). This key is used to encrypt the data in a one-level
            encryption or to control access to the data in a two-level encryption.

        keyb : str
            Encryption key B (32-character maximum). This key is used to encrypt the data in a two-level
            encryption. If ``KeyB`` is not specified, a one-level encryption is used to encrypt the data.

        datatype : str
            Type of data to encrypt. Must be set to MAT for material data.

        num1 : str
            Encrypt materials from material number ``NUM1`` to ``NUM2`` (defaults to ``NUM1`` ) in steps of
            ``INC`` (defaults to 1). If ``NUM1`` = ALL (default), ``NUM2`` and ``INC`` are ignored.

        num2 : str
            Encrypt materials from material number ``NUM1`` to ``NUM2`` (defaults to ``NUM1`` ) in steps of
            ``INC`` (defaults to 1). If ``NUM1`` = ALL (default), ``NUM2`` and ``INC`` are ignored.

        inc : str
            Encrypt materials from material number ``NUM1`` to ``NUM2`` (defaults to ``NUM1`` ) in steps of
            ``INC`` (defaults to 1). If ``NUM1`` = ALL (default), ``NUM2`` and ``INC`` are ignored.

        Notes
        -----

        .. _s-DBENCRYPT_notes:

        This command encrypts data in the database file. It must be issued before saving the database file (
        :ref:`save` command).

        For a one-level encryption, specify only ``KeyA`` and set ``NUM1`` to ALL. ( ``NUM2`` and ``INC``
        are not used.)

        For a `two-level encryption
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_apdl/apdl_encryptmat.html#partial_access>`_,
        specify both ``KeyA`` and ``KeyB``. Also specify ``NUM1``, ``NUM2``, and ``INC`` as needed.

        For more information about using :ref:`dbencrypt` in the encryption/decryption procedure, see
        `Encrypting Material Data
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_apdl/apdl_encryptmat.html#apdl_encryptsteps_mat>`_
        :ref:`dbdecrypt` command.

        This command is valid in any processor.
        """
        command = f"/DBENCRYPT,{keya},{keyb},{datatype},{num1},{num2},{inc}"
        return self.run(command, **kwargs)

    def decrypt(self, key1: str = "", key2: str = "", **kwargs):
        r"""Controls decryption of command input.

        Mechanical APDL Command: `/DECRYPT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_DECRYPT.html>`_

        Parameters
        ----------
        key1 : str
            Key to decrypt the encrypted input created by :ref:`encrypt`. The only valid label is PASSWORD.

        key2 : str
            Key to decrypt the encrypted input or to set the global encryption key. The following are valid
            inputs:

            * If ``Key2`` = OPENSSL or is blank, then decryption commences and the previously set global
              encryption key is used for decryption.

            * If ``Key2`` has a value, then that value is set as the global encryption key.

            * If ``Key2`` = OFF, then the global encryption password previously set by the command
              :ref:`decrypt`,PASSWORD, ``Key2`` is reset.

        Notes
        -----

        .. _s-DECRYPT_notes:

        When decrypting an encrypted input, ``/DECRYPT,PASSWORD,OPENSSL`` must appear as the first line of
        the encrypted file. The line is inserted automatically when you issue :ref:`encrypt` to create the
        encrypted file.

        To read an encrypted file, enter :ref:`decrypt`,PASSWORD, ``Key2`` anywhere in the standard input
        file to set the global encryption key. The encryption key must be set before reading in the
        encrypted input.

        :ref:`decrypt` is also valid when entered in the Command Input Window of the Mechanical APDL user
        interface.

        See `Encrypting Command Input and Other Data
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_apdl/apdl_encryptmat.html>`_
        :ref:`decrypt` and performing encryption and decryption.
        """
        command = f"/DECRYPT,{key1},{key2}"
        return self.run(command, **kwargs)

    def encrypt(self, key: str = "", fname: str = "", ext: str = "", **kwargs):
        r"""Controls encryption of command input.

        Mechanical APDL Command: `/ENCRYPT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_ENCRYPT.html>`_

        Parameters
        ----------
        key : str
            Encryption key used to encrypt the data (32-character maximum). A character parameter may be
            used. If the key is unspecified, encryption is turned off.

        fname : str
            Name of file (including directory path) where the encrypted commands are written (248-character
            maximum for both file name and directory). An unspecified directory path defaults to the working
            directory; in this case, you can use all 248 characters for the file name.

        ext : str
            File name extension (eight-character maximum).

        Notes
        -----

        .. _s-ENCRYPT_notes:

        This command opens the encrypted file specified by ``Fname`` and ``Ext`` for writing encrypted input
        commands.

        Issuing this command results in a new file that overwrites any data in an existing file by the same
        name. When the encrypted file is written, the first line in the file is
        ``/DECRYPT``,PASSWORD,OPENSSL and the last line is ``/DECRYPT``.

        See `Encrypting Command Input and Other Data
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_apdl/apdl_encryptmat.html>`_
        :ref:`encrypt` and performing encryption and decryption.
        """
        command = f"/ENCRYPT,{key},{fname},{ext}"
        return self.run(command, **kwargs)
