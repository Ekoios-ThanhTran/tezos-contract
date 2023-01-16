function bitLength(number) {
    return Math.floor(Math.log2(number)) + 1;
}

function byteLength(number) {
    return Math.ceil(bitLength(number) / 8);
}

function toBytes(number) {
    if (!Number.isSafeInteger(number)) {
        throw new Error("Number is out of range");
    }

    const size = number === 0 ? 0 : byteLength(number);
    const bytes = new Uint8ClampedArray(size);
    let x = number;
    for (let i = (size - 1); i >= 0; i--) {
        const rightByte = x & 0xff;
        bytes[i] = rightByte;
        x = Math.floor(x / 0x100);
    }

    return bytes.buffer;
}

function fromBytes(buffer) {
    const bytes = new Uint8ClampedArray(buffer);
    const size = bytes.byteLength;
    let x = 0;
    for (let i = 0; i < size; i++) {
        const byte = bytes[i];
        x *= 0x100;
        x += byte;
    }
    return x;
}

[0, 1, 2, 3, 0xf, 0xff, 0x100, Number.MAX_SAFE_INTEGER].forEach(n => {
    const tb = toBytes(n);
    const fb = fromBytes(tb);
    console.log(n, tb, fb);
})