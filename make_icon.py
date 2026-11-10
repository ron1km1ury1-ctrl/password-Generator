"""Create a custom shield-and-lock Windows icon using only Python's standard library."""

import struct
import zlib
from pathlib import Path

SIZE = 256


def in_polygon(x, y, points):
    inside = False
    j = len(points) - 1
    for i, (xi, yi) in enumerate(points):
        xj, yj = points[j]
        if (yi > y) != (yj > y) and x < (xj - xi) * (y - yi) / (yj - yi) + xi:
            inside = not inside
        j = i
    return inside


def png_chunk(kind, data):
    return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)


def create_png():
    shield = [(128, 28), (216, 59), (207, 147), (180, 193), (128, 226), (76, 193), (49, 147), (40, 59)]
    inner = [(128, 47), (195, 72), (187, 142), (165, 179), (128, 203), (91, 179), (69, 142), (61, 72)]
    rows = bytearray()
    for y in range(SIZE):
        rows.append(0)
        for x in range(SIZE):
            # Dark rounded-square background with transparent corners.
            in_square = 14 <= x < 242 and 14 <= y < 242
            if in_square:
                radius = 46
                for cx, cy in ((60, 60), (196, 60), (60, 196), (196, 196)):
                    if (x < 60 or x >= 196) and (y < 60 or y >= 196) and (x-cx)**2 + (y-cy)**2 > radius**2:
                        in_square = False
                        break
            color = (11, 17, 32, 255) if in_square else (0, 0, 0, 0)
            if in_polygon(x, y, shield):
                color = (14, 165, 233, 255)
            if in_polygon(x, y, inner):
                color = (17, 28, 46, 255)

            # Mint lock shackle and body.
            body = 87 <= x <= 169 and 119 <= y <= 181
            outer_shackle = ((x - 128) ** 2 + (y - 115) ** 2 <= 43 ** 2 and y <= 132)
            inner_shackle = ((x - 128) ** 2 + (y - 115) ** 2 < 27 ** 2 and y <= 132)
            if body or (outer_shackle and not inner_shackle):
                color = (52, 211, 153, 255)
            if ((x - 128) ** 2 + (y - 145) ** 2 <= 9 ** 2) or (124 <= x <= 132 and 145 <= y <= 164):
                color = (17, 28, 46, 255)
            rows.extend(color)

    png = b"\x89PNG\r\n\x1a\n"
    png += png_chunk(b"IHDR", struct.pack(">IIBBBBB", SIZE, SIZE, 8, 6, 0, 0, 0))
    png += png_chunk(b"IDAT", zlib.compress(bytes(rows), 9))
    png += png_chunk(b"IEND", b"")
    return png


def main():
    png = create_png()
    # ICO header + one 256x256 PNG image resource.
    ico_header = struct.pack("<HHH", 0, 1, 1)
    image_entry = struct.pack("<BBBBHHII", 0, 0, 0, 0, 1, 32, len(png), 22)
    Path("app_icon.ico").write_bytes(ico_header + image_entry + png)
    print("Created app_icon.ico")


if __name__ == "__main__":
    main()
