.. _ref_tls_guide:

==============================
Securing connections with mTLS
==============================

Mutual TLS (mTLS) is the recommended transport mode when connecting to MAPDL over
a network, particularly for remote connections.
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

.. warning::

   The certificate generation utilities described here are intended **for testing and
   local development only**. They are provided without any warranty and must not be
   used in production environments. For production deployments, always obtain
   certificates from your organization's IT department or a trusted Certificate
   Authority (CA).

To generate self-signed certificates for testing, use the
``generate_test_certificates()`` function from the ``ansys-tools-common`` package.
Install it with the ``other`` optional dependency group:

.. code-block:: console

    pip install ansys-tools-common[other]

Then generate certificates with a single call:

.. code-block:: python

    from ansys.tools.common.utils import generate_test_certificates
    from pathlib import Path

    generate_test_certificates(output_dir=Path("certs"))

After running the function, the output directory contains:

.. code-block:: text

    certs/
    ├── ca.key
    ├── ca.crt
    ├── server.key
    ├── server.crt
    ├── client.key
    └── client.crt

.. note::

   By default, generated certificates are valid for only **24 hours**. This short
   validity period is intentional for testing environments to encourage certificate
   regeneration and avoid stale credentials. Pass ``validity_days`` to override:

   .. code-block:: python

       generate_test_certificates(output_dir=Path("certs"), validity_days=30)

For HPC multi-node deployments, see the `certificate_generation_utilities`_ reference page.

For more details on certificate generation and the full ``cyberchannel`` API, see
the `certificate_generation_utilities`_ and `secure_grpc_docs`_ reference pages.

.. warning::

   Self-signed certificates are suitable for testing and private deployments but
   should not be used in production without a proper PKI review. Keep all
   ``.key`` files private and never commit them to a repository.


Launching MAPDL with mTLS
==========================

MAPDL reads its server certificate and key from the directory pointed to by the
``ANSYS_GRPC_CERTIFICATES`` environment variable. The directory must contain
``server.crt``, ``server.key``, and ``ca.crt``.

Set this environment variable before starting MAPDL, or pass it through
``add_env_vars`` when using
:func:`launch_mapdl() <ansys.mapdl.core.launcher.launch_mapdl>`.

**Option 1: Shell environment (manual MAPDL launch):**

.. code-block:: console

    export ANSYS_GRPC_CERTIFICATES=/path/to/certs
    /ansys_inc/v252/ansys/bin/mapdl -grpc -port 50052 -transport mtls

**Option 2: Pass via PyMAPDL** (let PyMAPDL start the MAPDL process):

You can pass the certificate directory to
:func:`launch_mapdl() <ansys.mapdl.core.launcher.launch_mapdl>` using the
``certs_dir`` argument.

.. code-block:: python

    from ansys.mapdl.core import launch_mapdl

    mapdl = launch_mapdl(
        transport_mode="mtls",
        certs_dir="/path/to/certs",
    )

.. note:: Using `certs_dir` automatically sets the ``ANSYS_GRPC_CERTIFICATES``
   environment variable for the MAPDL process while additionally checking that
   the required certificate files exist in the directory.

Or using the ``add_env_vars`` argument is used to set the ``ANSYS_GRPC_CERTIFICATES``
environment variable.

.. code-block:: python

    from ansys.mapdl.core import launch_mapdl

    mapdl = launch_mapdl(
        transport_mode="mtls",
        add_env_vars={"ANSYS_GRPC_CERTIFICATES": "/path/to/certs"},
    )


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

A summary table of the relevant environment variables, including the transport related ones,
can be found in :ref:`ref_environment_variables`.


End-to-end example
==================

The following example shows a complete workflow on a single machine.

**Step 1: Generate certificates**

.. code-block:: python

    from ansys.tools.common.utils import generate_test_certificates
    from pathlib import Path

    generate_test_certificates(output_dir=Path("certs"))

This creates the ``certs/`` directory in the current working directory with a CA,
server, and client certificate pair, each valid for 24 hours.

**Step 2: Launch MAPDL with mTLS**

.. code-block:: python

    import os
    from ansys.mapdl.core import launch_mapdl

    certs_path = os.path.abspath("certs")

    mapdl = launch_mapdl(
        transport_mode="mtls",
        certs_dir=certs_path,
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
