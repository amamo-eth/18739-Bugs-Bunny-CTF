#!/usr/bin/env python3
import os
import subprocess
import tempfile


BLOCK = 16


def oracle_valid(ct: bytes) -> bool:
    """
    Call ./oracle on a temporary file containing `ct`.
    RETURN:
        True  = valid padding
        False = invalid padding
    """
    # Write ciphertext to a temporary file
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(ct)
        name = tmp.name

    try:
        # Run oracle in *binary mode* (text=False)
        proc = subprocess.run(
            ["./oracle", name],
            capture_output=True,
            text=False,
        )
        # Decode safely, ignoring invalid UTF-8
        out = proc.stdout.decode(errors="ignore")

    finally:
        os.unlink(name)

    # Look for the poems (padding oracle leak)
    if "Your padding's in a SHOCK!" in out:
        return False

    if (
        "This padding's lookin' comfy as a carrot bed." in out
        or "Heh, not bad doc!" in out
    ):
        return True

    # Should not reach here, but assume bad padding if unsure
    return False


def recover_intermediate_block(cblock: bytes) -> bytes:
    """
    Recover intermediate value I = Dec_k(Cblock) using the padding oracle.
    """
    I = bytearray(BLOCK)
    prev = bytearray(BLOCK)

    # pad = 1..16
    for pad in range(1, BLOCK + 1):
        idx = BLOCK - pad

        for g in range(256):
            # bytes AFTER idx need proper padding
            for j in range(idx + 1, BLOCK):
                prev[j] = I[j] ^ pad

            # byte we are guessing
            prev[idx] = g ^ pad

            # bytes before idx can be anything (0 is fine)
            for j in range(0, idx):
                prev[j] = 0

            test_ct = bytes(prev) + cblock

            if oracle_valid(test_ct):
                I[idx] = g
                break

    return bytes(I)


def decrypt(cipher: bytes) -> bytes:
    """
    Decrypt full CBC ciphertext using the padding oracle.
    """
    blocks = [cipher[i:i + BLOCK] for i in range(0, len(cipher), BLOCK)]
    intermediates = [recover_intermediate_block(b) for b in blocks]

    # Compute plaintext: P_i = I_i XOR C_{i-1}
    plaintext = b""

    for i, I in enumerate(intermediates):
        if i == 0:
            prev = b"\x00" * BLOCK  # IV = 0 in oracle.c
        else:
            prev = blocks[i - 1]

        P = bytes(a ^ b for a, b in zip(I, prev))
        plaintext += P

    # Strip PKCS#7 padding
    pad = plaintext[-1]
    if 1 <= pad <= BLOCK and plaintext.endswith(bytes([pad]) * pad):
        plaintext = plaintext[:-pad]

    return plaintext


def main():
    # Stage 1
    print("[*] Decrypting carrot_stage1.bin...")
    with open("carrot_stage1.bin", "rb") as f:
        c1 = f.read()
    pt1 = decrypt(c1)
    print(pt1.decode(errors="replace"))
    print()

    # Stage 2
    print("[*] Decrypting carrot_stage2.bin...")
    with open("carrot_stage2.bin", "rb") as f:
        c2 = f.read()
    pt2 = decrypt(c2)
    print(pt2.decode(errors="replace"))
    print()


if __name__ == "__main__":
    main()
