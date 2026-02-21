#!/usr/bin/env python3
"""
Rockart Contact Form API
HTTP server na porte 8080 s endpointom POST /api/contact.
Odosle email cez SMTP. Ziadne externe zavislosti.
"""

import json
import logging
import os
import re
import smtplib
import sys
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Lock

# ---------------------------------------------------------------------------
# Konfiguracia
# ---------------------------------------------------------------------------
LISTEN_PORT = int(os.environ.get("CONTACT_API_PORT", "8080"))
SMTP_HOST = os.environ.get("SMTP_HOST", "localhost")
SMTP_PORT = int(os.environ.get("SMTP_PORT", "587"))
SMTP_USER = os.environ.get("SMTP_USER", "")
SMTP_PASS = os.environ.get("SMTP_PASS", "")
RECIPIENT = os.environ.get("CONTACT_RECIPIENT", "melicher@rockart.sk")
ALLOWED_ORIGINS = os.environ.get(
    "ALLOWED_ORIGINS", "https://rockart.sk,https://www.rockart.sk,http://localhost"
).split(",")

# Rate limiting
RATE_LIMIT_MAX = 5          # max requestov
RATE_LIMIT_WINDOW = 60      # za X sekund

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    stream=sys.stdout,
)
log = logging.getLogger("contact_api")

# ---------------------------------------------------------------------------
# Rate limiter (in-memory, thread-safe)
# ---------------------------------------------------------------------------
_rate_lock = Lock()
_rate_store: dict[str, list[float]] = {}


def _is_rate_limited(ip: str) -> bool:
    now = time.time()
    with _rate_lock:
        timestamps = _rate_store.get(ip, [])
        # Odstranime stare zaznamy
        timestamps = [t for t in timestamps if now - t < RATE_LIMIT_WINDOW]
        if len(timestamps) >= RATE_LIMIT_MAX:
            _rate_store[ip] = timestamps
            return True
        timestamps.append(now)
        _rate_store[ip] = timestamps
        return False


# ---------------------------------------------------------------------------
# Validacia
# ---------------------------------------------------------------------------
EMAIL_RE = re.compile(r"^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$")


def validate_contact(data: dict) -> str | None:
    """Vrati chybovu spravu alebo None ak je vsetko OK."""
    name = (data.get("name") or "").strip()
    email = (data.get("email") or "").strip()
    message = (data.get("message") or "").strip()

    if not name:
        return "Meno je povinne."
    if len(name) > 100:
        return "Meno je prilis dlhe (max 100 znakov)."
    if not email:
        return "Email je povinny."
    if not EMAIL_RE.match(email):
        return "Neplatny format emailu."
    if not message:
        return "Sprava je povinna."
    if len(message) > 2000:
        return "Sprava je prilis dlha (max 2000 znakov)."
    phone = (data.get("phone") or "").strip()
    if phone and len(phone) > 30:
        return "Telefonne cislo je prilis dlhe."
    return None


# ---------------------------------------------------------------------------
# SMTP odoslanie
# ---------------------------------------------------------------------------
def send_email(name: str, email: str, phone: str, message: str) -> None:
    subject = f"[Rockart Web] Sprava od {name}"

    body = (
        f"Nova sprava z kontaktneho formulara rockart.sk\n"
        f"{'=' * 50}\n\n"
        f"Meno:     {name}\n"
        f"Email:    {email}\n"
        f"Telefon:  {phone or '(nezadany)'}\n\n"
        f"Sprava:\n{message}\n"
    )

    msg = MIMEMultipart()
    msg["From"] = SMTP_USER or f"web@rockart.sk"
    msg["To"] = RECIPIENT
    msg["Reply-To"] = email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain", "utf-8"))

    log.info("Odosielam email na %s cez %s:%s", RECIPIENT, SMTP_HOST, SMTP_PORT)

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=15) as server:
        server.ehlo()
        server.starttls()
        server.ehlo()
        if SMTP_USER and SMTP_PASS:
            server.login(SMTP_USER, SMTP_PASS)
        server.sendmail(msg["From"], [RECIPIENT], msg.as_string())

    log.info("Email uspesne odoslany.")


# ---------------------------------------------------------------------------
# HTTP Handler
# ---------------------------------------------------------------------------
class ContactHandler(BaseHTTPRequestHandler):
    """Spracuje POST /api/contact a CORS preflight OPTIONS."""

    def _get_client_ip(self) -> str:
        """Ziska realnu IP (z X-Real-IP / X-Forwarded-For alebo priamo)."""
        ip = self.headers.get("X-Real-IP")
        if ip:
            return ip.strip()
        forwarded = self.headers.get("X-Forwarded-For")
        if forwarded:
            return forwarded.split(",")[0].strip()
        return self.client_address[0]

    def _set_cors_headers(self) -> None:
        origin = self.headers.get("Origin", "")
        if origin in ALLOWED_ORIGINS:
            self.send_header("Access-Control-Allow-Origin", origin)
        else:
            # Povolime pre development (localhost)
            self.send_header("Access-Control-Allow-Origin", origin)
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def _send_json(self, code: int, data: dict) -> None:
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self._set_cors_headers()
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    # --- CORS preflight ---
    def do_OPTIONS(self) -> None:
        self.send_response(204)
        self._set_cors_headers()
        self.send_header("Content-Length", "0")
        self.end_headers()

    # --- POST /api/contact ---
    def do_POST(self) -> None:
        if self.path != "/api/contact":
            self._send_json(404, {"status": "error", "message": "Not found"})
            return

        client_ip = self._get_client_ip()

        # Rate limiting
        if _is_rate_limited(client_ip):
            log.warning("Rate limit prekroceny pre IP %s", client_ip)
            self._send_json(429, {
                "status": "error",
                "message": "Prilis vela poziadavkov. Skuste to neskor."
            })
            return

        # Nacitame telo
        try:
            content_length = int(self.headers.get("Content-Length", 0))
            if content_length > 10_000:
                self._send_json(413, {
                    "status": "error",
                    "message": "Poziadavka je prilis velka."
                })
                return
            raw = self.rfile.read(content_length)
            data = json.loads(raw.decode("utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError):
            self._send_json(400, {
                "status": "error",
                "message": "Neplatny JSON format."
            })
            return

        # Honeypot kontrola
        honeypot = (data.get("honeypot") or "").strip()
        if honeypot:
            log.info("Honeypot zachyteny od IP %s — ignorujem.", client_ip)
            self._send_json(200, {"status": "ok"})
            return

        # Validacia
        error = validate_contact(data)
        if error:
            self._send_json(400, {"status": "error", "message": error})
            return

        name = data["name"].strip()
        email = data["email"].strip()
        phone = (data.get("phone") or "").strip()
        message = data["message"].strip()

        # Odoslanie emailu
        try:
            send_email(name, email, phone, message)
        except smtplib.SMTPAuthenticationError:
            log.exception("SMTP autentifikacia zlyhala")
            self._send_json(500, {
                "status": "error",
                "message": "Chyba pri odosielani. Skuste to neskor."
            })
            return
        except smtplib.SMTPException as exc:
            log.exception("SMTP chyba: %s", exc)
            self._send_json(500, {
                "status": "error",
                "message": "Nepodarilo sa odoslat spravu. Skuste to neskor."
            })
            return
        except Exception as exc:
            log.exception("Neocakavana chyba: %s", exc)
            self._send_json(500, {
                "status": "error",
                "message": "Interny chyba servera."
            })
            return

        log.info("Sprava od %s <%s> uspesne odoslana.", name, email)
        self._send_json(200, {"status": "ok"})

    # --- Vsetky ostatne metody ---
    def do_GET(self) -> None:
        if self.path == "/api/health":
            self._send_json(200, {"status": "ok", "service": "contact-api"})
            return
        self._send_json(404, {"status": "error", "message": "Not found"})

    # Potlacime default logging do stderr — pouzijeme vlastny
    def log_message(self, format, *args) -> None:
        log.info("%s - %s", self._get_client_ip(), format % args)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    log.info("Startujem Contact API na porte %d", LISTEN_PORT)
    log.info("SMTP: %s:%s  |  Recipient: %s", SMTP_HOST, SMTP_PORT, RECIPIENT)
    if not SMTP_USER:
        log.warning("SMTP_USER nie je nastaveny — emaily nemusia byt dorucene!")

    server = HTTPServer(("0.0.0.0", LISTEN_PORT), ContactHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        log.info("Ukoncujem server.")
        server.server_close()


if __name__ == "__main__":
    main()
