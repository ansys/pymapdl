.. _ref_tls_guide:

========================================
Securing connections with mTLS
========================================

Mutual TLS (mTLS) is the recommended transport mode when connecting to MAPDL over
a network, particularly in remote.
Unlike plain TLS, mTLS requires **both** the server and the client to present a
valid certificate signed by a shared Certificate Authority (CA). This mutual
authentication guarantees that:

* PyMAPDL only connects to a trusted MAPDL server.
* MAPDL only accepts connections from trusted clients.
* All gRPC traffic is encrypted in transit.


Certificate files
=================

An mTLS setup requires three pairs of files: one for the CA, one for the server,
and one for the client. All files use PEM encoding.

.. list-table::
   :header-rows: 1
   :widths: 20 20 60

   * - Party
     - Files
     - Purpose
   * - Certificate Authority
     - ``ca.key``, ``ca.crt``
     - Root of trust. The CA signs both the server and client certificates.
       ``ca.key`` must be kept secret; ``ca.crt`` is distributed to all parties.
   * - Server (MAPDL)
     - ``server.key``, ``server.crt``
     - Presented by MAPDL to prove its identity. The certificate carries
       ``SERVER_AUTH`` extended key usage and Subject Alternative Names (SANs)
       matching the hostname or IP address that clients use to connect.
   * - Client (PyMAPDL)
     - ``client.key``, ``client.crt``
     - Presented by PyMAPDL to prove its identity. The certificate carries
       ``CLIENT_AUTH`` extended key usage.

.. note::

   The server and client certificates must be signed by the same CA so that each
   party can verify the other.


Generating certificates
=======================

The following Python script generates a complete set of self-signed certificates
using the ``cryptography`` package (RSA 4096-bit keys, SHA-256 signing). It
produces the full CA → server → client chain and writes all files to a ``certs/``
output directory.

First, install the required dependency:

.. code-block:: console

    pip install cryptography

Then run the script below, adjusting ``SERVER_HOSTS`` and ``CLIENT_NAME`` as
needed:

.. code-block:: python

    """Generate mTLS certificates for MAPDL gRPC connections."""

    import os
    from datetime import datetime, timedelta, timezone
    from pathlib import Path

    from cryptography import x509
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.asymmetric import rsa
    from cryptography.x509.oid import ExtendedKeyUsageOID, NameOID

    # ── Configuration ────────────────────────────────────────────────────────────
    # Each entry is (primary_hostname, [extra_SANs]). For a remote server add its
    # hostname and IP, e.g. ("my-mapdl-host", ["192.168.1.10"]).
    # For HPC deployments add one entry per compute node.
    SERVER_HOSTS = [("localhost", ["127.0.0.1"])]
    CLIENT_NAME = "PyMAPDL Client"
    VALIDITY_DAYS = 365  # 1 year
    OUTPUT_DIR = Path("certs")
    # ─────────────────────────────────────────────────────────────────────────────


    def _new_key() -> rsa.RSAPrivateKey:
        return rsa.generate_private_key(public_exponent=65537, key_size=4096)


    def _save_key(key: rsa.RSAPrivateKey, path: Path) -> None:
        path.write_bytes(
            key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption(),
            )
        )


    def _save_cert(cert: x509.Certificate, path: Path) -> None:
        path.write_bytes(cert.public_bytes(serialization.Encoding.PEM))


    def _validity(days: int):
        now = datetime.now(timezone.utc)
        return now, now + timedelta(days=days)


    def make_ca(key: rsa.RSAPrivateKey, days: int) -> x509.Certificate:
        """Create a self-signed CA certificate."""
        name = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, "My CA")])
        nb, na = _validity(days)
        return (
            x509.CertificateBuilder()
            .subject_name(name)
            .issuer_name(name)
            .public_key(key.public_key())
            .serial_number(x509.random_serial_number())
            .not_valid_before(nb)
            .not_valid_after(na)
            .add_extension(x509.BasicConstraints(ca=True, path_length=None), critical=True)
            .add_extension(
                x509.KeyUsage(
                    digital_signature=True,
                    key_cert_sign=True,
                    crl_sign=True,
                    key_encipherment=False,
                    data_encipherment=False,
                    key_agreement=False,
                    content_commitment=False,
                    encipher_only=False,
                    decipher_only=False,
                ),
                critical=True,
            )
            .sign(key, hashes.SHA256())
        )


    def make_server_cert(
        key: rsa.RSAPrivateKey,
        ca_cert: x509.Certificate,
        ca_key: rsa.RSAPrivateKey,
        common_name: str,
        sans: list[str],
        days: int,
    ) -> x509.Certificate:
        """Create a server certificate signed by the CA."""
        san_list = [x509.DNSName(common_name)]
        for s in sans:
            if s != common_name:
                try:
                    import ipaddress

                    san_list.append(x509.IPAddress(ipaddress.ip_address(s)))
                except ValueError:
                    san_list.append(x509.DNSName(s))

        nb, na = _validity(days)
        return (
            x509.CertificateBuilder()
            .subject_name(x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, common_name)]))
            .issuer_name(ca_cert.subject)
            .public_key(key.public_key())
            .serial_number(x509.random_serial_number())
            .not_valid_before(nb)
            .not_valid_after(na)
            .add_extension(x509.SubjectAlternativeName(san_list), critical=False)
            .add_extension(
                x509.KeyUsage(
                    digital_signature=True,
                    key_encipherment=True,
                    key_cert_sign=False,
                    crl_sign=False,
                    data_encipherment=False,
                    key_agreement=False,
                    content_commitment=False,
                    encipher_only=False,
                    decipher_only=False,
                ),
                critical=True,
            )
            .add_extension(
                x509.ExtendedKeyUsage([ExtendedKeyUsageOID.SERVER_AUTH]), critical=False
            )
            .sign(ca_key, hashes.SHA256())
        )


    def make_client_cert(
        key: rsa.RSAPrivateKey,
        ca_cert: x509.Certificate,
        ca_key: rsa.RSAPrivateKey,
        common_name: str,
        days: int,
    ) -> x509.Certificate:
        """Create a client certificate signed by the CA."""
        nb, na = _validity(days)
        return (
            x509.CertificateBuilder()
            .subject_name(x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, common_name)]))
            .issuer_name(ca_cert.subject)
            .public_key(key.public_key())
            .serial_number(x509.random_serial_number())
            .not_valid_before(nb)
            .not_valid_after(na)
            .add_extension(
                x509.SubjectAlternativeName([x509.DNSName(common_name)]), critical=False
            )
            .add_extension(
                x509.KeyUsage(
                    digital_signature=True,
                    key_encipherment=True,
                    key_cert_sign=False,
                    crl_sign=False,
                    data_encipherment=False,
                    key_agreement=False,
                    content_commitment=False,
                    encipher_only=False,
                    decipher_only=False,
                ),
                critical=True,
            )
            .add_extension(
                x509.ExtendedKeyUsage([ExtendedKeyUsageOID.CLIENT_AUTH]), critical=False
            )
            .sign(ca_key, hashes.SHA256())
        )


    OUTPUT_DIR.mkdir(exist_ok=True)

    # CA
    ca_key = _new_key()
    ca_cert = make_ca(ca_key, VALIDITY_DAYS)
    _save_key(ca_key, OUTPUT_DIR / "ca.key")
    _save_cert(ca_cert, OUTPUT_DIR / "ca.crt")
    print("Generated CA")

    # Server certificate(s)
    for hostname, extra_sans in SERVER_HOSTS:
        stem = "server" if len(SERVER_HOSTS) == 1 else hostname
        srv_key = _new_key()
        srv_cert = make_server_cert(
            srv_key, ca_cert, ca_key, hostname, extra_sans, VALIDITY_DAYS
        )
        _save_key(srv_key, OUTPUT_DIR / f"{stem}.key")
        _save_cert(srv_cert, OUTPUT_DIR / f"{stem}.crt")
        print(f"Generated server certificate for {hostname}")

    # Client certificate
    cli_key = _new_key()
    cli_cert = make_client_cert(cli_key, ca_cert, ca_key, CLIENT_NAME, VALIDITY_DAYS)
    _save_key(cli_key, OUTPUT_DIR / "client.key")
    _save_cert(cli_cert, OUTPUT_DIR / "client.crt")
    print("Generated client certificate")

    print(f"\nAll certificates written to '{OUTPUT_DIR}/'")

After running the script, the output directory contains:

.. code-block:: text

    certs/
    ├── ca.key
    ├── ca.crt
    ├── server.key
    ├── server.crt
    ├── client.key
    └── client.crt

For multiple servers (HPC), each node gets its own ``<hostname>.key`` /
``<hostname>.crt`` pair alongside the shared ``ca.crt``.

.. warning::

   Self-signed certificates are suitable for testing and private deployments but
   should not be used in production without a proper PKI review. Keep all
   ``.key`` files private and never commit them to a repository.


Launching MAPDL with mTLS
==========================

MAPDL reads its server certificate and key from the directory pointed to by the
``ANSYS_MAPDL_CERTS_PATH`` environment variable. The directory must contain
``server.crt``, ``server.key``, and ``ca.crt``.

Set this variable before starting MAPDL, or pass it through ``add_env_vars`` when
using :func:`launch_mapdl() <ansys.mapdl.core.launcher.launch_mapdl>`.

**Option 1: Shell environment (manual MAPDL launch):**

.. code-block:: console

    export ANSYS_MAPDL_CERTS_PATH=/path/to/certs
    /ansys_inc/v252/ansys/bin/mapdl -grpc -port 50052 -transport mtls

**Option 2: Pass via PyMAPDL** (let PyMAPDL start the MAPDL process):

.. code-block:: python

    from ansys.mapdl.core import launch_mapdl

    mapdl = launch_mapdl(
        transport_mode="mtls",
        certs_dir="/path/to/certs",
        add_env_vars={"ANSYS_MAPDL_CERTS_PATH": "/path/to/certs"},
    )

.. note::

   The ``add_env_vars`` dictionary is merged on top of the current shell
   environment, so existing variables (license server, MPI settings, etc.) are
   preserved.


Connecting PyMAPDL to an existing mTLS-enabled MAPDL instance
==============================================================

When connecting to an already-running MAPDL instance, set the transport mode and
certificate directory either in code or via environment variables.

**Using** :func:`launch_mapdl() <ansys.mapdl.core.launcher.launch_mapdl>` **(connect only):**

.. code-block:: python

    from ansys.mapdl.core import launch_mapdl

    mapdl = launch_mapdl(
        start_instance=False,
        ip="192.168.1.10",
        port=50052,
        transport_mode="mtls",
        certs_dir="/path/to/certs",
    )

**Using environment variables** (no code changes required):

.. code-block:: console

    export PYMAPDL_GRPC_TRANSPORT=mtls
    export ANSYS_GRPC_CERTIFICATES=/path/to/certs

.. code-block:: python

    from ansys.mapdl.core import launch_mapdl

    # Transport mode and certs directory are read from the environment
    mapdl = launch_mapdl(start_instance=False, ip="192.168.1.10", port=50052)

The relevant environment variables are summarised below.

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Environment variable
     - Description
   * - ``PYMAPDL_GRPC_TRANSPORT`` or ``ANSYS_MAPDL_GRPC_TRANSPORT``
     - Sets the gRPC transport mode for PyMAPDL. Set to ``mtls`` to enable
       mutual TLS. ``PYMAPDL_GRPC_TRANSPORT`` takes precedence if both are
       set.
   * - ``ANSYS_GRPC_CERTIFICATES``
     - Path to the directory containing the **client** certificates
       (``ca.crt``, ``client.crt``, ``client.key``) used by PyMAPDL.
   * - ``ANSYS_MAPDL_CERTS_PATH``
     - Path to the directory containing the **server** certificates
       (``ca.crt``, ``server.crt``, ``server.key``) read by the MAPDL process.


End-to-end example
==================

The following example shows a complete workflow on a single machine.

**Step 1: Generate certificates**

Run the script from the `Generating certificates`_ section with the default
``SERVER_HOSTS = [("localhost", ["127.0.0.1"])]`` setting. This creates the
``certs/`` directory in the current working directory.

**Step 2: Launch MAPDL with mTLS**

.. code-block:: python

    import os
    from ansys.mapdl.core import launch_mapdl

    certs_path = os.path.abspath("certs")

    mapdl = launch_mapdl(
        transport_mode="mtls",
        certs_dir=certs_path,
        add_env_vars={"ANSYS_MAPDL_CERTS_PATH": certs_path},
    )

**Step 3: Verify the connection and run commands**

.. code-block:: pycon

    >>> print(mapdl)
    Product:             Ansys Mechanical Enterprise
    MAPDL Version:       25.2
    ansys.mapdl version: ...

    >>> mapdl.prep7()
    >>> mapdl.k(1, 0, 0, 0)
    >>> mapdl.exit()
