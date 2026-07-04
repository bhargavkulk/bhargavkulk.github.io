import argparse
import subprocess
import threading
import time
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('serve_dir')
parser.add_argument('-w', '--watch', nargs='*', default=[])
parser.add_argument('-p', '--port', type=int, default=8080)
args = parser.parse_args()

serve_dir: str = args.serve_dir
watch_dirs: list[str] = args.watch
port: int = args.port


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.extensions_map.update({'.html': 'text/html; charset=UTF-8'})
        super().__init__(*args, directory=serve_dir, **kwargs)


def run_server():
    server = ThreadingHTTPServer(('localhost', port), Handler)
    print(f'Server started at http://localhost:{port}/')
    server.serve_forever()


def get_mtimes():
    mtimes: dict[str, float] = dict()
    watch_paths = [Path(w) for w in watch_dirs]

    for watch_path in watch_paths:
        if not watch_path.exists():
            raise ValueError(f'"{watch_path}" does not exist')

        if watch_path.is_dir():
            files = [w for w in watch_path.rglob('*') if not w.is_dir()]
            for file in files:
                if file.name.startswith('.#'):
                    continue
                try:
                    mtimes[str(file)] = file.stat().st_mtime
                except PermissionError:
                    continue
        else:
            try:
                mtimes[str(watch_path)] = watch_path.stat().st_mtime
            except PermissionError:
                pass

    return mtimes


subprocess.run(['ninja'])

server_thread = threading.Thread(target=run_server, daemon=True)
server_thread.start()

last_mtimes = get_mtimes()

try:
    while True:
        time.sleep(1)
        current_mtimes = get_mtimes()

        if current_mtimes != last_mtimes:
            print('\nChange detected! Rebuilding...')
            subprocess.run(['ninja'])
            last_mtimes = current_mtimes
except KeyboardInterrupt:
    print('\nStopping server...')
