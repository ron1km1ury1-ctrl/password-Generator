"""Create a Windows .ico file using only Python's standard library."""

import math
import struct
import zlib
from pathlib import Path

SIZE = 256


def inside_rounded_rect(x, y, left, top, right, bottom, radius):
    if left + radius <= x <= right - radius or top + radius <= y <= bottom - radius:
        return left <= x <= right and top <= y <= bottom
    cx = left + radius if x < left + radius else right - radius
    cy = top + radius if y < top + radius else bottom - radius
    return (x - cx) ** 2 + (y - cy) ** 2 <= radius ** 2


def inside_polygon(x, y, points):
    inside = False
    j = len(points) - 1
    for i, (xi, yi) in enumerate(points):
        xj, yj = points[j]
        if ((yi > y) != (yj > y)) and x < (xj - xi) * (y - yi) / (yj - yi) + xi:
            inside = not inside
        j = i
    return inside


def make_png():
    pixels = bytearray()
    shield = [(128, 30), (211, 60), (203, 145), (177, 190), (128, 222),
              (79, 190), (53, 145), (45, 60)]

    for y in range(SIZE):
        pixels.append(0)  # PNG filter type: None
        for x in range(SIZE):
            color = (16, 24, 32, 255) if inside_rounded_rect(x, y, 8, 8, 248, 248, 48) else (0, 0, 0, 0)

            # Cyan shield with a subtle darker outline.
            if inside_polygon(x, y, shield):
                color = (0, 217, 255, 255)
            if inside_polygon(x, y, [(128, 48), (190, 70), (184, 141), (165, 177),
                                     (128, 201), (91, 177), (72, 141), (66, 70)]):
                color = (24, 46, 58, 255)

            # Mint-green lock body and shackle.
            in_body = 91 <= x <= 165 and 118 <= y <= 174
            in_shackle_outer = ((x - 128) ** 2 + (y - 112) ** 2 <= 37 ** 2 and y <= 122)
            in_shackle_inner = ((x - 128) ** 2 + (y - 112) ** 2 <= 21 ** 2 and y <= 122)
            if in_body or (in_shackle_outer and not in_shackle_inner):
                color = (0, 255, 153, 255)

            # Keyhole.
            if ((x - 128) ** 2 + (y - 139) ** 2 <= 9 ** 2) or (123 <= x <= 133 and 139 <= y <= 157):
                color = (24, 46, 58, 255)

            pixels.extend(color)

    def chunk(kind, data):
        return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)

    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", struct.pack(">IIBBBBB", SIZE, SIZE, 8, 6, 0, 0, 0))
    png += chunk(b"IDAT", zlib.compress(bytes(pixels), 9))
    png += chunk(b"IEND", b"")
    return png


def main():
    png = make_png()
    # Windows ICO directory containing one 256x256 PNG image.
    header = struct.pack("<HHH", 0, 1, 1)
    entry = struct.pack("<BBBBHHII", 0, 0, 0, 0, 1, 32, len(png), 22)
    Path("app_icon.ico").write_bytes(header + entry + png)
    print("Created app_icon.ico")


if __name__ == "__main__":
    main()
