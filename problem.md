# Bugs Bunny's Carrot Cake Cipher Oracle

- Namespace: 18739
- ID: bugs-bunny-oracle
- Type: custom
- Category: Crypto
- Points: 500
- Templatable: no
- MaxUsers: 1

## Description

Bugs Bunny has built his very own encryption machine to protect his super-secret carrot cake recipe.
Unfortunately… Bugs isn’t a cryptographer.

You’ve recovered:

- `carrot_stage1.bin` — encrypted carrot cake recipe #1
- `carrot_stage2.bin` — encrypted carrot cake recipe #2

Rumor has it Bugs accidentally turned his decryption errors into cryptic poems.
Maybe those poems leak more than he intended…

## Details

Recover **Flag 1** from `carrot_stage1.bin`, then use the hint inside it to recover **Flag 2** from `carrot_stage2.bin`.
Download the carrots from your challenge instance:

Download carrot_stage1.bin {{url_for("carrot_stage1.bin", "here")}}.
Download carrot_stage2.bin {{url_for("carrot_stage2.bin", "here")}}.


## Hints

- Bugs’ oracle behaves strangely, sometimes it rhymes.
- Could the oracle be leaking **padding validity**?
- AES-CBC + padding leaks are dangerous…

## Solution Overview

Use a **padding oracle attack** to recover the plaintext from `carrot_stage1.bin`.
Inside, you’ll find a hint that helps you decrypt `carrot_stage2.bin`.

## Challenge Options

```yaml
cpus: 0.5
memory: 128m
pidslimit: 20
ulimits:
  - nofile=128:128
diskquota: 64m
init: true
```
