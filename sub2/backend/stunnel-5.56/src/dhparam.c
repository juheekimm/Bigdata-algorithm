/* dhparam.c: initial DH parameters for stunnel */
#include "common.h"
#ifndef OPENSSL_NO_DH
#define DN_new DH_new
DH *get_dh2048(void)
{
    static unsigned char dhp_2048[] = {
        0xD5, 0x75, 0xF1, 0x23, 0xC1, 0x81, 0x4B, 0x44, 0x23, 0xBE,
        0x97, 0x81, 0x7A, 0xDA, 0x97, 0x1F, 0x1F, 0x0D, 0xD5, 0xEC,
        0xC5, 0x5F, 0x86, 0x42, 0x7F, 0x38, 0xA3, 0x95, 0xEE, 0xA0,
        0x52, 0x2C, 0xB7, 0x20, 0x29, 0xC1, 0xC7, 0xE6, 0x8E, 0x6F,
        0xE5, 0xC1, 0x0D, 0xDD, 0x8A, 0xEF, 0x8D, 0xE7, 0xA8, 0x63,
        0xB4, 0xF7, 0x58, 0x32, 0x0E, 0x24, 0xAC, 0x30, 0x94, 0xF5,
        0xC7, 0x02, 0x81, 0x1B, 0xC7, 0x68, 0xE5, 0x71, 0xD7, 0x1E,
        0x3D, 0xE4, 0x2E, 0x2F, 0xC0, 0x0A, 0xED, 0x34, 0xAC, 0xC0,
        0x1F, 0x0A, 0x56, 0xA4, 0x12, 0x02, 0xFD, 0x68, 0xD2, 0x4D,
        0x5E, 0x0A, 0x5D, 0x78, 0xE3, 0xA0, 0x85, 0x75, 0xD2, 0xA9,
        0xC1, 0xF2, 0xAD, 0x65, 0x11, 0xDE, 0xE8, 0x05, 0x68, 0x36,
        0x4C, 0x92, 0x99, 0x21, 0xB9, 0x69, 0xD0, 0x6F, 0xD8, 0xA3,
        0xEA, 0x35, 0x13, 0x93, 0xDC, 0x1B, 0x13, 0x16, 0xB2, 0x15,
        0x8E, 0x10, 0x22, 0xCE, 0x01, 0x1F, 0x1C, 0x09, 0x86, 0xD5,
        0xE7, 0xCB, 0xCF, 0xFA, 0xED, 0x2F, 0xE2, 0x3A, 0x65, 0x14,
        0xC9, 0xFA, 0x70, 0x99, 0xF7, 0xE0, 0x30, 0xBF, 0x7F, 0xEA,
        0x84, 0x14, 0x8A, 0x51, 0xC9, 0xE9, 0x85, 0x73, 0x7F, 0xA1,
        0xB0, 0xC3, 0x33, 0x9A, 0xAB, 0x69, 0x4E, 0x75, 0xFB, 0x12,
        0xB0, 0x9E, 0xB1, 0xD9, 0xD1, 0xB9, 0x32, 0x1D, 0xC6, 0xD9,
        0x2C, 0xAA, 0xB0, 0xC5, 0x3E, 0x69, 0x56, 0xA2, 0xB3, 0xA2,
        0x81, 0xCA, 0x9D, 0x77, 0xBB, 0x52, 0x44, 0xA2, 0xED, 0xE0,
        0xF0, 0x2A, 0x81, 0x85, 0x90, 0xB6, 0x04, 0x60, 0xEB, 0x09,
        0x72, 0x08, 0x44, 0xAF, 0x28, 0xF5, 0x15, 0x34, 0x87, 0x5C,
        0x8A, 0xB4, 0x5B, 0x15, 0x6A, 0xAD, 0x27, 0x4E, 0xA0, 0xDE,
        0x99, 0x22, 0xCF, 0xAB, 0x4C, 0xFD, 0x75, 0x10, 0x5D, 0xFF,
        0xE8, 0x81, 0x50, 0xC4, 0xC0, 0x4B
    };
    static unsigned char dhg_2048[] = {
        0x02
    };
    DH *dh = DH_new();
    BIGNUM *p, *g;

    if (dh == NULL)
        return NULL;
    p = BN_bin2bn(dhp_2048, sizeof(dhp_2048), NULL);
    g = BN_bin2bn(dhg_2048, sizeof(dhg_2048), NULL);
    if (p == NULL || g == NULL
            || !DH_set0_pqg(dh, p, NULL, g)) {
        DH_free(dh);
        BN_free(p);
        BN_free(g);
        return NULL;
    }
    return dh;
}
#endif /* OPENSSL_NO_DH */
/* built for stunnel 5.56 */