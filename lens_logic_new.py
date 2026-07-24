import http.client
import secrets
import ssl
import urllib.parse
import webbrowser

LENS_HOST = "lens.google.com"
LENS_UPLOAD_PATH = "/upload"
REQUEST_TIMEOUT = 25  # seconds

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
)

# Anonymous requests to Google from an EU/EEA IP are otherwise served a GDPR
# consent interstitial instead of the expected redirect. This is the same
# "consent already given" cookie long used by Google-scraping tools to skip
# that interstitial for unauthenticated, cookie-less requests.
CONSENT_COOKIE = "CONSENT=YES+"

# Optional UI hook (e.g. tray notification) so upload status is visible
# instead of running silently in the background.
_status_callback = None


def set_status_callback(callback):
    """Registers callback(message: str) to surface upload status to the UI."""
    global _status_callback
    _status_callback = callback


def _notify(message):
    print(message)
    if _status_callback:
        try:
            _status_callback(message)
        except Exception:
            pass


def _build_multipart_body(image_bytes):
    """Builds a multipart/form-data body matching what lens.google.com/upload expects."""
    boundary = "----LensAnywhereBoundary" + secrets.token_hex(16)

    header = (
        f'--{boundary}\r\n'
        'Content-Disposition: form-data; name="image_content"\r\n\r\n\r\n'
        f'--{boundary}\r\n'
        'Content-Disposition: form-data; name="encoded_image"; filename="image.png"\r\n'
        'Content-Type: image/png\r\n\r\n'
    ).encode("utf-8")
    footer = f'\r\n--{boundary}--\r\n'.encode("utf-8")

    return boundary, header + image_bytes + footer


def _upload_to_lens(image_bytes):
    """POSTs the image bytes directly to Google Lens (a plain outbound HTTPS
    request, like any browser upload) and returns the resulting search-results
    URL taken from the redirect. No public exposure of the image is involved."""
    boundary, body = _build_multipart_body(image_bytes)

    headers = {
        "Content-Type": f"multipart/form-data; boundary={boundary}",
        "Content-Length": str(len(body)),
        "User-Agent": USER_AGENT,
        "Accept-Language": "en-US,en;q=0.9",
        "Cookie": CONSENT_COOKIE,
    }

    query = urllib.parse.urlencode({"hl": "en", "gl": "us"})

    conn = http.client.HTTPSConnection(
        LENS_HOST, timeout=REQUEST_TIMEOUT, context=ssl.create_default_context()
    )
    try:
        conn.request("POST", f"{LENS_UPLOAD_PATH}?{query}", body=body, headers=headers)
        response = conn.getresponse()
        response.read()  # drain the body so the connection can close cleanly

        if response.status in (301, 302, 303, 307, 308):
            location = response.getheader("Location")
            if location:
                if location.startswith("/"):
                    location = f"https://{LENS_HOST}{location}"
                return location

        _notify(f"[ERROR] Google Lens upload returned unexpected status {response.status}.")
        return None
    finally:
        conn.close()


def search_lens(image_bytes: bytes):
    """Uploads the capture directly to Google Lens and opens the resulting
    search page in the default browser. Nothing is served or exposed
    publicly: the image travels in a single outbound HTTPS request."""
    _notify("LensAnywhere: uploading capture to Google Lens...")

    try:
        result_url = _upload_to_lens(image_bytes)
    except Exception as e:
        _notify(f"[ERROR] Could not reach Google Lens: {e}")
        return

    if not result_url:
        _notify("[ERROR] Google Lens upload failed. Please try again.")
        return

    webbrowser.open(result_url)


if __name__ == "__main__":
    print("This module is meant to be imported and run via main.py")
