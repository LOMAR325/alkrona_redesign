#!/usr/bin/env python3
"""Локальный статический сервер для предпросмотра сайта.

    python3 serve.py        →  http://127.0.0.1:4173

Отдаёт файлы без кэширования, чтобы правки в CSS и JS были видны
сразу после обновления страницы.
"""
import functools
import http.server
import os
import socketserver

ROOT = os.path.dirname(os.path.abspath(__file__))
PORT = 4173

MIME = {".webp": "image/webp", ".woff2": "font/woff2", ".json": "application/json"}


class Handler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-store, must-revalidate")
        super().end_headers()

    def guess_type(self, path):
        ext = os.path.splitext(path)[1].lower()
        return MIME.get(ext) or super().guess_type(path)

    def log_message(self, fmt, *args):
        if "404" in (args[1] if len(args) > 1 else ""):
            super().log_message(fmt, *args)


class Server(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True


if __name__ == "__main__":
    os.chdir(ROOT)
    handler = functools.partial(Handler, directory=ROOT)
    with Server(("127.0.0.1", PORT), handler) as httpd:
        print(f"Alkrona → http://127.0.0.1:{PORT}  (Ctrl+C — остановить)")
        httpd.serve_forever()
