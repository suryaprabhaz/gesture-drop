# Gesture Drop

Gesture Drop is a computer-vision and networking experiment that lets you trigger a desktop-to-mobile content transfer using a hand gesture.

## Architecture

`Webcam → gesture detector → trigger/debounce → HTTP API → mobile web client`

The desktop sender detects a closed-fist gesture and sends clipboard text to the local Flask service. A phone connected through the displayed URL can consume the latest content.

## Production-minded improvements

- Input validation and upload size limits
- Image type validation and collision-resistant filenames
- Automated API tests
- Python CI
- Security guidance for tunnel/network exposure
- Tunnel binaries excluded from source control

## Run

```bash
pip install -r requirements.txt
start.bat
```

The startup script expects the `ngrok` command to be available on the machine; the executable itself is intentionally not committed to the repository.

## Security

Do not expose the Flask receiver to the public internet without authentication and transport security. Treat received content as untrusted.

## Author

[@suryaprabhaz](https://github.com/suryaprabhaz)
