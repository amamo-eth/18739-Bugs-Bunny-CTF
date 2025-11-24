#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <openssl/aes.h>
#include <openssl/rand.h>

// The Fake traps
static const char *FAKE_FLAG = "bugsCTFflag{nice_try_doc}";
static const char *FAKE_KEY = "DEBUG: key = 0xdeadbeef\n";

// AES key
unsigned char KEY[16] = {0x12,0x34,0x56,0x78,0x90,0xab,0xcd,0xef,0x11,0x22,0x33,0x44,0x55,0x66,0x77,0x88};

// Poem messages
void poem_bad_padding() {
    printf("Eh... what's up, doc?\n");
    printf("Your padding's in a SHOCK!\n");
    printf("Try nibblin' the bytes,\n");
    printf("Flip 'em just right,\n");
    printf("Maybe then I'll unlock!\n");
}

void poem_good_padding() {
    printf("Heh, not bad doc!\n");
    printf("This padding's lookin' comfy as a carrot bed.\n");
}

void poem_stage2_hint() {
    printf("Tick... tock... tick... tock...\n");
    printf("Watchin' the clock won't help ya, doc!\n");
    printf("Timing ain't your friend,\n");
    printf("The rabbit never breaks... unless the padding bends.\n");
}

// CBC decryption
int decrypt_cbc(unsigned char *cipher, int len, unsigned char *out) {
    AES_KEY aes_key;
    AES_set_decrypt_key(KEY, 128, &aes_key);

    unsigned char iv[16] = {0};
    AES_cbc_encrypt(cipher, out, len, &aes_key, iv, AES_DECRYPT);

    int pad = out[len - 1];
    if (pad <= 0 || pad > 16) return 0;

    for (int i = 1; i <= pad; i++) {
        if (out[len - i] != pad) return 0;
    }
    return 1;
}


int main(int argc, char *argv[]) {

    // Fake trap print
    if (rand() % 7 == 0) {
        printf("%s", FAKE_KEY);
    }
    if (rand() % 9 == 0) {
        printf("%s\n", FAKE_FLAG);
    }

    if (argc < 2) {
        printf("Eh… what's up, doc?\n");
        printf("Usage: %s <cipherfile>\n", argv[0]);
        return 0;
    }

    // time delay trap
    usleep(rand() % 800);


    FILE *f = fopen(argv[1], "rb");
    if (!f) {
        printf("I knew I shoulda taken that left turn at Albuquerque...\n");
        return 0;
    }

    fseek(f, 0, SEEK_END);
    int len = ftell(f);
    fseek(f, 0, SEEK_SET);

    unsigned char *cipher = malloc(len);
    unsigned char *plain = malloc(len);

    fread(cipher, 1, len, f);
    fclose(f);

    int ok = decrypt_cbc(cipher, len, plain);

    if (!ok) {
        poem_bad_padding();
        return 0;
    }

    poem_good_padding();

    printf("\nDecrypted message:\n%s\n", plain);

    return 0;
}
