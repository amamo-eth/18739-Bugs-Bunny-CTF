# Bugs Bunny Oracle
A cmgr-compatible cryptography CTF challenge.

## Challenge Description
Bugs Bunny has hidden the secret flag inside two encrypted files: `carrot_stage1.bin` and `carrot_stage2.bin`.

You are provided with access to an AES-CBC encryption oracle that uses a fixed key and IV. The oracle is not secure and leaks information through its output. Your task is to exploit this leakage to decrypt both encrypted stages and recover the final flag.

The challenge is designed to test your understanding of AES-CBC mode, block-by-block decryption, and how to reverse CBC operations when partial information is exposed.

---

## Files Included

| File | Description |
|------|-------------|
| `carrot_stage1.bin` | First AES-CBC encrypted blob |
| `carrot_stage2.bin` | Second AES-CBC encrypted blob |
| `oracle` | Binary program that performs AES-CBC encryption with a fixed key/IV |
| `solve1.py` | Optional starter script for building your attack |
| `metadata.json` | cmgr metadata file |
| `Dockerfile` | Challenge build configuration (if custom type is used) |

Players do not have the source code of the oracle.

---

## Technical Background
AES in CBC mode computes ciphertext blocks as:
CT[i] = AES( PT[i] XOR CT[i-1] )

Because the oracle leaks information about intermediate CBC computations, it becomes possible to reverse this equation and recover the plaintext without the AES key.

The intended solution involves:
- Treating the oracle as a black-box function.
- Sending carefully crafted inputs.
- Using the oracle’s responses to derive intermediate CBC values.
- Undoing the XOR chaining and block transformations to recover the underlying plaintext.

---

## Running the Challenge

Inside the cmgr environment:
cmgr update
cmgr playtest <challenge-id>

To manually run the oracle:

./oracle < input.bin

You may write your solver in any programming language.

---

## Hints
- Focus entirely on CBC structure.
- Decrypt the ciphertext block-by-block.
- Observe what part of the CBC chain the oracle is leaking.
- Use XOR relationships to reverse each block.
- Stage 1 and Stage 2 decrypt using the same method.

---

## Expected Output
When your solver works correctly, it should print something similar to:

[] Decrypting carrot_stage1.bin...
[] Decrypting carrot_stage2.bin...
FLAG{your_final_flag_here}

---

## Requirements
To fully complete the challenge, you must:
1. Exploit the oracle’s leakage correctly.
2. Recover plaintext for both encrypted files.
3. Extract the correct final flag.
4. Treat the oracle strictly as a black box (no source code access).
5. Include your solver script (e.g., `solve1.py`) in your repository.

---


