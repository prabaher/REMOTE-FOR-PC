import sys
import qrcode

if len(sys.argv) < 2:
    print("ERROR: IP address not provided.")
    sys.exit(1)

ip = sys.argv[1]
url = f"http://{ip}:5000"

qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=1,
    border=2
)

qr.add_data(url)
qr.make(fit=True)

matrix = qr.get_matrix()

print()
print("=" * 50)
print("          LAPTOP REMOTE QR CODE")
print("=" * 50)
print()
print(f"URL: {url}")
print()
print("Scan this QR code with your phone:")
print()

# Print two rows at a time for a more square QR
for y in range(0, len(matrix), 2):
    line = ""
    for x in range(len(matrix[0])):
        top = matrix[y][x]
        bottom = matrix[y + 1][x] if y + 1 < len(matrix) else False

        if top and bottom:
            line += "█"
        elif top and not bottom:
            line += "▀"
        elif not top and bottom:
            line += "▄"
        else:
            line += " "

    print(line)

print()
print("=" * 50)
print("  Scan QR → Remote opens on your phone")
print("=" * 50)
print()