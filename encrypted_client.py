from ExeSteganography import ExeSteganography

# Create an instance
stego = ExeSteganography()

# Embed an executable
stego.embed_exe(
    image_path="path/to/carrier.png",
    exe_path="path/to/program.exe",
    output_path="path/to/output.png"
)

# Extract the executable
stego.extract_exe(
    stego_image_path="path/to/output.png",
    output_exe_path="path/to/extracted.exe"
)