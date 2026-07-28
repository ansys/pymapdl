# PR #4617 — Comments Summary

This file details all comments found on PR #4617 (ansys/pymapdl). Each entry contains author, timestamp, file/path (if applicable), URL, and the full comment body.

---

1) Author: codecov[bot]
   Created: 2026-05-27T16:11:33Z
   URL: https://github.com/ansys/pymapdl/pull/4617#issuecomment-4556367798
   Type: Automated coverage report (issue comment)

   Body:

   ## [Codecov](https://app.codecov.io/gh/ansys/pymapdl/pull/4617?dropdown=coverage&src=pr&el=h1&utm_medium=referral&utm_source=github&utm_content=comment&utm_campaign=pr+comments&utm_term=ansys) Report
   :white_check_mark: All modified and coverable lines are covered by tests.
   :white_check_mark: Project coverage is 90.26%. Comparing base ([`1268f20`](https://app.codecov.io/gh/ansys/pymapdl/commit/1268f20eaad0953e656b06090667d0ccf91514d0?dropdown=coverage&el=desc&utm_medium=referral&utm_source=github&utm_content=comment&utm_campaign=pr+comments&utm_term=ansys)) to head ([`63009e8`](https://app.codecov.io/gh/ansys/pymapdl/commit/63009e8271ebdee24445850a2c0551f95384726f?dropdown=coverage&el=desc&utm_medium=referral&utm_source=github&utm_content=comment&utm_campaign=pr+comments&utm_term=ansys)).
   :warning: Report is 4 commits behind head on main.

   Additional diff summary (excerpt):

   - Coverage   90.27%   90.26%   -0.02%
   - Files         209      209
   - Lines       17187    17187
   - Hits        15516    15513       -3
   - Misses       1671     1674       +3

---

2) Author: Copilot
   Created: 2026-05-27T15:56:58Z
   Path: doc/source/user_guide/tls.rst
   Position: 1 (review comment)
   URL: https://github.com/ansys/pymapdl/pull/4617#discussion_r3312070540
   Type: Review comment (docs)

   Body:

   The phrase "particularly in remote" is grammatically incorrect/unclear. Consider rewriting to something like "particularly for remote connections" to make the intent clear.

---

3) Author: Copilot
   Created: 2026-05-27T15:56:59Z
   Path: doc/source/user_guide/tls.rst
   Position: 1 (review comment)
   URL: https://github.com/ansys/pymapdl/pull/4617#discussion_r3312070609
   Type: Review comment (docs)

   Body:

   The docs describe certificates having "SERVER_AUTH" / "CLIENT_AUTH" extended key usage, but the standard EKU names are typically written as "serverAuth" / "clientAuth" (or described as "server authentication" / "client authentication"). Using the canonical names would reduce confusion when users generate certs with OpenSSL or inspect them with tooling.

---

4) Author: Copilot
   Created: 2026-05-27T15:56:59Z
   Path: doc/source/user_guide/tls.rst
   Position: 1 (review comment)
   URL: https://github.com/ansys/pymapdl/pull/4617#discussion_r3312070648
   Type: Review comment (docs + behavior mismatch)

   Body:

   The example implies that passing `transport_mode="mtls"` and `certs_dir=...` to `launch_mapdl()` will configure the client connection. In the current implementation, `launch_mapdl()`/`connect_to_existing()` constructs `MapdlGrpc` without forwarding `transport_mode`/`certs_dir`, so this code path won’t actually enable mTLS unless the corresponding environment variables are used (or a `MapdlGrpc` is created with those args directly). Please adjust the example/documentation to reflect the real configuration mechanism.

---

5) Author: Copilot
   Created: 2026-05-27T15:56:59Z
   Path: doc/source/user_guide/tls.rst
   Position: 1 (review comment)
   URL: https://github.com/ansys/pymapdl/pull/4617#discussion_r3312070685
   Type: Review comment (docs + behavior mismatch)

   Body:

   This launch example relies on `transport_mode="mtls"` / `certs_dir=...` in `launch_mapdl()`, but `launch_mapdl()` currently does not pass these through when creating the `MapdlGrpc` client. As written, this is likely to start/connect using the default transport unless the `PYMAPDL_GRPC_TRANSPORT` / `ANSYS_GRPC_CERTIFICATES` environment variables are set. Update the example to use the environment variables (or otherwise document how to ensure the client actually uses mTLS).

---

6) Author: Copilot
   Created: 2026-05-27T15:56:59Z
   Path: doc/source/user_guide/tls.rst
   Position: 1 (review comment)
   URL: https://github.com/ansys/pymapdl/pull/4617#discussion_r3312070711
   Type: Review comment (docs + behavior mismatch)

   Body:

   The end-to-end example uses `transport_mode="mtls"` / `certs_dir=...` on `launch_mapdl()`, but the launcher currently doesn’t forward these settings into the constructed `MapdlGrpc` client. This makes the example likely to fall back to the platform default transport unless users also set `PYMAPDL_GRPC_TRANSPORT=mtls` and `ANSYS_GRPC_CERTIFICATES`. Please revise the example accordingly so it works as documented.

---

7) Author: Copilot
   Created: 2026-05-27T15:57:00Z
   Path: doc/source/user_guide/mapdl.rst
   Position: 35 (review comment)
   URL: https://github.com/ansys/pymapdl/pull/4617#discussion_r3312070752
   Type: Review comment (docs + clarification)

   Body:

   The description says the client cert directory is used when `transport_mode` is `mtls`, but for `launch_mapdl()` the transport mode may be selected via environment variables and (currently) not via the `transport_mode` argument. Consider rephrasing to explicitly tie this variable to the gRPC transport selected by `PYMAPDL_GRPC_TRANSPORT` / `ANSYS_MAPDL_GRPC_TRANSPORT` (and/or `MapdlGrpc(transport_mode=...)`) to avoid implying that setting `launch_mapdl(transport_mode="mtls")` alone is sufficient.

---

Notes / suggested next steps (from comments):
- Fix doc phrasing for clarity ("particularly in remote" -> "particularly for remote connections").
- Use canonical EKU names in docs to avoid confusion: "serverAuth" / "clientAuth".
- Update examples to either:
  - Show using MapdlGrpc directly with transport_mode/certs_dir, or
  - Demonstrate setting `PYMAPDL_GRPC_TRANSPORT=mtls` and `ANSYS_GRPC_CERTIFICATES=<path>` so the example actually enables mTLS.
- Clarify which functions/arguments control gRPC transport vs which environment variables are required.

End of file.
