from hashlib import sha512, sha256, sha1
import time

class TOTP:
    '''
    TOTP class
    Uses the TOTP algorithm to generate a one-time password
    SHA-512 is used as the hash function
    '''

    def __init__(self):
        pass

    @staticmethod
    def hexStr2Bytes(hexStr: str):
        return bytes.fromhex(hexStr)

    @staticmethod
    def generateTOTP(key: str, time: str, returnDigits=6,
                     crypto='sha1', time_step=30):
        result = ""

        time = hex(int(time) // time_step * time_step)[2:]
        # Using the counter
        # First 8 bytes are for the movingFactor
        # Compliant with base RFC 4226 (HOTP)
        while (len(time) < 16):
            time = "0" + time

        # Get the HEX in a Byte[]
        msg = TOTP.hexStr2Bytes(time)
        k = TOTP.hexStr2Bytes(key)
        if crypto == 'sha512':
            hash = sha512(k + msg).hexdigest()
        elif crypto == 'sha256':
            hash = sha256(k + msg).hexdigest()
        elif crypto == 'sha1':
            hash = sha1(k + msg).hexdigest()

        offset = ord(hash[-1]) & 0xf
        binary = ((ord(hash[offset]) & 0x7f) << 24) | \
            ((ord(hash[offset + 1]) & 0xff) << 16) | \
            ((ord(hash[offset + 2]) & 0xff) << 8) | \
            ((ord(hash[offset + 3]) & 0xff))

        otp = binary % (10 ** returnDigits)

        result = str(otp)
        while (len(result) < returnDigits):
            result = "0" + result

        return result

if __name__ == '__main__':
    key='6723a63fc813efa037dab2128781cbc395a90ffd83bf2b520d6d62488350d898fd5624717ac2fa443388cb80fb7a784a04aa4fa6659c4fcce87e62dec718bb95'
    totp = TOTP()

    print(totp.generateTOTP(key, str(int(time.time()))[-16:]))