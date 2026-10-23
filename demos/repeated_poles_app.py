"""Live repeated-pole laboratory. Author: Xu Chen, University of Washington.

python demos/repeated_poles_app.py --n 20          # compute with local NumPy
python demos/repeated_poles_app.py --build-only    # export browser app
python demos/repeated_poles_app.py                # serve app on port 8767

The browser executes this same calculation in Pyodide/NumPy. Internet access
is needed on first load for the pinned Pyodide runtime. No code or inputs are
sent to a calculation service. The initial plot is labeled until Python is ready.
"""
import argparse
import inspect
import json
from pathlib import Path
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from math import comb
import numpy as np

ROOT = Path(__file__).resolve().parent


def calculate(n):
    if isinstance(n, bool) or int(n) != n or not 2 <= n <= 40:
        raise ValueError('n must be an integer from 2 to 40.')
    n = int(n)
    coefficients = [comb(n, k) for k in range(n + 1)]
    p = np.roots(coefficients)
    return {'n': n, 'roots': [[float(z.real), float(z.imag)] for z in p],
            'max_displacement': float(np.max(np.abs(p + 1))),
            'numpy_version': np.__version__}


def build():
    code = 'from math import comb\nimport numpy as np\nimport json\n\n' + inspect.getsource(calculate)
    template = (ROOT / 'repeated_poles_template.html').read_text()
    dest = ROOT / 'repeated_poles_app.html'
    dest.write_text(template.replace('__PYTHON_SOURCE__', json.dumps(code)).replace('__INITIAL_DATA__', json.dumps(calculate(20))))
    return dest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--n', type=int)
    parser.add_argument('--build-only', action='store_true')
    parser.add_argument('--port', type=int, default=8767)
    args = parser.parse_args()
    if args.n is not None:
        print(json.dumps(calculate(args.n), indent=2));return
    dest = build()
    print('Built', dest, flush=True)
    if args.build_only:return
    server = ThreadingHTTPServer(('127.0.0.1',args.port),partial(SimpleHTTPRequestHandler,directory=str(ROOT)))
    print(f'Open http://127.0.0.1:{args.port}/{dest.name}',flush=True)
    try:server.serve_forever()
    except KeyboardInterrupt:pass
    finally:server.server_close()


if __name__ == '__main__':main()
