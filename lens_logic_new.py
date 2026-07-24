import http.server
import socketserver
import threading
import subprocess
import re
import secrets
import urllib.parse
import webbrowser
import os
import sys
import time

PORT = 8998  # Internal local server port

# Idle time to keep the Cloudflare tunnel open after a capture, to give
# Google Lens time to fetch the image, before it is torn down automatically.
TUNNEL_IDLE_TIMEOUT = 45
# Max time to wait for cloudflared to print a public URL on startup.
TUNNEL_STARTUP_TIMEOUT = 15

CURRENT_IMAGE = None
CURRENT_TOKEN = None
PUBLIC_URL = None
SERVER_READY = False

_tunnel_process = None
_tunnel_lock = threading.Lock()
_shutdown_timer = None

_local_server_started = False
_local_server_lock = threading.Lock()

# Optional UI hook (e.g. tray notification) so the tunnel lifecycle is
# visible instead of running fully silently in the background.
_status_callback = None


def set_status_callback(callback):
    """Registers callback(message: str) to surface tunnel status to the UI."""
    global _status_callback
    _status_callback = callback


def _notify(message):
    print(message)
    if _status_callback:
        try:
            _status_callback(message)
        except Exception:
            pass


def get_resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller bundling."""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), relative_path)


class ImageHandler(http.server.BaseHTTPRequestHandler):
    """Serves the latest captured screenshot from RAM behind a random, per-capture token."""

    def do_GET(self):
        requested_path = self.path.split("?", 1)[0]
        expected_path = f"/{CURRENT_TOKEN}/image.png" if CURRENT_TOKEN else None

        if CURRENT_IMAGE and expected_path and requested_path == expected_path:
            self.send_response(200)
            self.send_header("Content-Type", "image/png")
            self.send_header("Content-Length", str(len(CURRENT_IMAGE)))
            self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
            self.end_headers()
            self.wfile.write(CURRENT_IMAGE)
        else:
            self.send_error(404, "Not Found")

    def log_message(self, format, *args):
        # Silence local HTTP server logs in console
        pass


def _run_local_server():
    """Runs a tiny local web server in a background thread, bound to localhost only."""
    socketserver.TCPServer.allow_reuse_address = True
    try:
        with socketserver.TCPServer(("127.0.0.1", PORT), ImageHandler) as httpd:
            httpd.serve_forever()
    except Exception as e:
        print(f"Local server error: {e}")


def _ensure_local_server():
    """Starts the local (loopback-only) server once, lazily on first capture."""
    global _local_server_started
    with _local_server_lock:
        if _local_server_started:
            return
        threading.Thread(target=_run_local_server, daemon=True).start()
        _local_server_started = True


def _start_tunnel_blocking():
    """Launches cloudflared for this capture only and blocks until a public URL is parsed."""
    global PUBLIC_URL, SERVER_READY, _tunnel_process

    exe_name = "cloudflared.exe" if sys.platform == "win32" else "cloudflared"
    exe_path = get_resource_path(exe_name)

    if not os.path.exists(exe_path):
        _notify(f"[ERROR] '{exe_name}' not found next to the application.")
        return False

    _notify("LensAnywhere: opening a temporary tunnel for this capture...")

    creation_flags = subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0

    process = subprocess.Popen(
        [exe_path, "tunnel", "--url", f"http://127.0.0.1:{PORT}"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        creationflags=creation_flags
    )
    _tunnel_process = process

    url_regex = re.compile(r'https://[a-zA-Z0-9-]+\.trycloudflare\.com')
    deadline = time.time() + TUNNEL_STARTUP_TIMEOUT

    while time.time() < deadline:
        line = process.stdout.readline()
        if not line:
            break
        match = url_regex.search(line)
        if match:
            PUBLIC_URL = match.group(0)
            SERVER_READY = True
            _notify("LensAnywhere: tunnel active for this capture.")
            return True

    return SERVER_READY


def _stop_tunnel():
    """Kills the cloudflared process and resets tunnel state, closing the exposure window."""
    global PUBLIC_URL, SERVER_READY, _tunnel_process, CURRENT_IMAGE, CURRENT_TOKEN

    proc = _tunnel_process
    _tunnel_process = None
    PUBLIC_URL = None
    SERVER_READY = False
    CURRENT_IMAGE = None
    CURRENT_TOKEN = None

    if proc and proc.poll() is None:
        try:
            proc.terminate()
            proc.wait(timeout=5)
        except Exception:
            try:
                proc.kill()
            except Exception:
                pass

    _notify("LensAnywhere: tunnel closed.")


def _schedule_tunnel_shutdown(delay=TUNNEL_IDLE_TIMEOUT):
    global _shutdown_timer
    if _shutdown_timer:
        _shutdown_timer.cancel()
    _shutdown_timer = threading.Timer(delay, _stop_tunnel)
    _shutdown_timer.daemon = True
    _shutdown_timer.start()


def is_server_ready():
    """The capture overlay no longer waits on the tunnel: it is opened on demand per capture."""
    return True


def search_lens(image_bytes: bytes):
    """Serves the capture locally behind a random token and opens Google Lens via a
    freshly-started, short-lived Cloudflare tunnel that is torn down shortly after use."""
    global CURRENT_IMAGE, CURRENT_TOKEN

    _ensure_local_server()

    with _tunnel_lock:
        if _shutdown_timer:
            _shutdown_timer.cancel()

        CURRENT_TOKEN = secrets.token_urlsafe(16)
        CURRENT_IMAGE = image_bytes

        if not SERVER_READY:
            if not _start_tunnel_blocking():
                _notify("[ERROR] Tunnel unavailable. Make sure cloudflared is present next to the application.")
                CURRENT_IMAGE = None
                CURRENT_TOKEN = None
                return

        # Random per-capture token instead of a fixed, guessable path.
        img_url = f"{PUBLIC_URL}/{CURRENT_TOKEN}/image.png"
        lens_url = "https://lens.google.com/uploadbyurl?url=" + urllib.parse.quote(img_url, safe="")

        _notify("LensAnywhere: opening search in Google Lens...")
        webbrowser.open(lens_url)

        _schedule_tunnel_shutdown()


if __name__ == "__main__":
    print("This module is meant to be imported and run via main.py")
