#!/usr/bin/env python3
"""Generate deterministic synthetic PDF and PNG fixtures. Python 3, no dependencies."""
import argparse
import struct
import zlib
from pathlib import Path


def pdf(letter):
    stream = f"BT /F1 48 Tf 36 108 Td (PAGE {letter}) Tj ET\n".encode("ascii")
    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 240 240] "
        b"/Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
        b"<< /Length %d >>\nstream\n" % len(stream) + stream + b"endstream",
    ]
    out = bytearray(b"%PDF-1.4\n")
    offsets = []
    for number, obj in enumerate(objects, 1):
        offsets.append(len(out))
        out.extend(b"%d 0 obj\n" % number + obj + b"\nendobj\n")
    xref = len(out)
    out.extend(b"xref\n0 6\n0000000000 65535 f \n")
    for offset in offsets:
        out.extend(b"%010d 00000 n \n" % offset)
    out.extend(b"trailer\n<< /Size 6 /Root 1 0 R >>\nstartxref\n%d\n%%%%EOF\n" % xref)
    return bytes(out)


def chunk(kind, data):
    return struct.pack(">I", len(data)) + kind + data + struct.pack(
        ">I", zlib.crc32(kind + data) & 0xFFFFFFFF
    )


def png():
    width, height = 192, 128
    palette = [(29, 54, 85), (29, 138, 144), (249, 190, 82), (247, 240, 220)]
    rows = bytearray()
    for y in range(height):
        rows.append(0)  # PNG filter: None
        for x in range(width):
            index = ((x // 24) + (y // 16)) % len(palette)
            rows.extend(palette[index])
    return (
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0))
        + chunk(b"IDAT", zlib.compress(bytes(rows), level=0))
        + chunk(b"IEND", b"")
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output_dir", nargs="?", type=Path, default=Path("fixtures"))
    directory = parser.parse_args().output_dir
    directory.mkdir(parents=True, exist_ok=True)
    for filename, content in (("page-a.pdf", pdf("A")), ("page-b.pdf", pdf("B")),
                              ("color-grid.png", png())):
        path = directory / filename
        with path.open("xb") as handle:
            handle.write(content)
        print(f"{path} ({len(content)} bytes)")


if __name__ == "__main__":
    main()
