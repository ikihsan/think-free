#!/usr/bin/env python3
"""E168 G2 arm A, rows 20-24. See `attempts_a.py` for the protocol.

Rows: 65, 66, 67, 68, 69. n = 24 total, the declared floor.
"""

ATTEMPTS_C = {
65: "'Unable to get certificate CRL' during verification means the verifier "
    "was asked to check revocation and could not fetch a CRL, so it refuses "
    "the chain - it is not a statement that the certificate is untrusted. "
    "Something is turning on CRL checking: your OpenSSL 3.6 build or the "
    "trust store you point SSL_CERT_FILE at is supplying a verify config with "
    "`X509_V_FLAG_CRL_CHECK` set. Build the SSL context explicitly, set "
    "`verify_mode` to VERIFY_PEER with revocation checking left off, and check "
    "whether a corporate trust bundle or an `openssl.cnf` is injecting the "
    "flag. The fact that `openssl s_client` fails the same way points at the "
    "shared OpenSSL configuration rather than at Ruby.",

66: "The numpy source-tree message is numpy's fallback guard: the real import "
    "of the compiled extension failed, so numpy assumes it is being run from a "
    "source checkout and prints that message instead of the real error. After "
    "a macOS upgrade the installed numpy binary is usually the problem - it "
    "was built against an older SDK - so force-reinstall it from the channel "
    "that built it for this platform (`conda install --force-reinstall numpy` "
    "in this environment) rather than leaving a pip-installed wheel in place. "
    "If it persists, remove the numpy directory so the interpreter cannot see a "
    "source tree and read the underlying dlopen failure.",

67: "Those folders are MSBuild build-host working directories that the .NET "
    "SDK creates for the out-of-process build host when a solution contains "
    "projects targeting .NET Framework; the .NET 8 to .NET 10 change altered "
    "which host variant gets instantiated, so both variants now appear. They "
    "are build artifacts, not source: delete them, exclude them from source "
    "control, and stop them being recreated by setting "
    "`MSBUILDDISABLENODEREUSE=1` if the churn is the actual problem you are "
    "solving.",

68: "That attribute was removed from pip's internal `InstallRequirement`, and "
    "pip-tools 7.5.1 still reads it, so this is a pip/pip-tools version "
    "incompatibility rather than anything in your requirements file. Pin pip to "
    "a release from before the attribute was removed, or upgrade pip-tools to "
    "a release that no longer touches it; do both environment pins in your "
    "build so the resolver, pip and the compiler agree. Reading it from a "
    "public compatibility table is what you are missing - there is no "
    "in-error-message pointer to the pairing.",

69: "On a simulator the APNs token only exists if the simulator is allowed to "
    "register with Apple's push service, and after an Xcode change that "
    "entitlement and capability are usually the thing that got regenerated "
    "away. Confirm the app target still has the Push Notifications capability "
    "and an entitlements file containing `aps-environment` set to "
    "`development`, that the provisioning profile on the simulator carries it, "
    "and that the macOS host is signed into an Apple ID - a simulator with no "
    "signed-in Apple ID never receives a token, which produces exactly this "
    "error with no other symptom.",
}