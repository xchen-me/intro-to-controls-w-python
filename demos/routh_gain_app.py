"""Lecture 10 gain and stability laboratory.
Author: Xu Chen, University of Washington, 2026.

python demos/routh_gain_app.py                  # build and serve the interactive app
python demos/routh_gain_app.py --build-only     # export offline HTML for slides/site
python demos/routh_gain_app.py --gain 1000      # inspect any non-grid gain in Python

SciPy computes unit-step responses of K/(s^3+18s^2+77s+K). The exported
browser app selects from an explicitly listed gain grid, including K=1386,
so it works offline and on a static course website without a Python server.
The time-window control displays a subset of the precomputed 0–10 s interval.
"""
import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import numpy as np
from scipy import signal

ROOT = Path(__file__).resolve().parent
BOUNDARY = 1386.0


def simulate(gain, duration=10, samples=1601):
    gain = float(gain)
    if not np.isfinite(gain):
        raise ValueError('Gain must be finite.')
    poles = np.roots([1, 18, 77, gain])
    time = np.linspace(0, duration, samples)
    if gain == 0:
        response = np.zeros_like(time)
    else:
        _, response = signal.step(signal.TransferFunction([gain], [1, 18, 77, gain]), T=time)
    label = ('asymptotically stable' if 0 < gain < BOUNDARY else
             'marginally stable' if gain == BOUNDARY else
             'boundary: internal pole at zero' if gain == 0 else 'unstable')
    return {'k': gain, 'poles': [[round(p.real, 9), round(p.imag, 9)] for p in poles],
            'y': np.round(response, 7).tolist(), 'status': label,
            'firstColumn': [1, 18, (1386-gain)/18, gain]}


def build(output=None):
    output = Path(output) if output else ROOT / 'routh_gain_app.html'
    gains = sorted(set(range(-100, 2401, 20)) | {1386})
    data = {'dt': 10/1600, 'duration': 10, 'curves': [simulate(k) for k in gains]}
    source = (ROOT / 'gain_app_template.html').read_text()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(source.replace('__SIMULATION_DATA__', json.dumps(data, separators=(',', ':'))))
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--build-only', action='store_true')
    parser.add_argument('--output', type=Path)
    parser.add_argument('--port', type=int, default=8766)
    parser.add_argument('--gain', type=float)
    args = parser.parse_args()
    if args.gain is not None:
        result = simulate(args.gain)
        print(json.dumps({k: v for k, v in result.items() if k != 'y'}, indent=2))
        return
    output = build(args.output)
    print(f'Built {output}', flush=True)
    if args.build_only:
        return
    server = ThreadingHTTPServer(('127.0.0.1', args.port), partial(SimpleHTTPRequestHandler, directory=str(output.parent)))
    print(f'Open http://127.0.0.1:{args.port}/{output.name}', flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\nStopped.')
    finally:
        server.server_close()


if __name__ == '__main__':
    main()
