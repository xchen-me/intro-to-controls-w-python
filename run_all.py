# Author: Xu Chen, University of Washington
"""Run every example without a display and save each figure to out/.

usage:  python run_all.py            (all examples)
        python run_all.py L19        (examples whose name starts with L19)
"""
import glob, os, runpy, sys, traceback
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'out')
os.makedirs(OUT, exist_ok=True)
prefix = sys.argv[1] if len(sys.argv) > 1 else ''
failed = []
for path in sorted(glob.glob(os.path.join(HERE, 'examples', prefix + '*.py'))):
    name = os.path.basename(path)[:-3]
    count = [0]

    def show(*args, **kwargs):          # replace plt.show(): save the figure instead
        count[0] += 1
        plt.gcf().savefig(os.path.join(OUT, '%s_%d.png' % (name, count[0])), dpi=120)
        plt.close('all')

    plt.show = show
    print('=' * 20, name)
    try:
        sys.argv = [path]
        runpy.run_path(path, run_name='__main__')
        print('-> ok, %d figure(s) saved to out/' % count[0])
    except Exception:
        traceback.print_exc()
        failed.append(name)
print('\nfailed: %s' % (failed or 'none'))
sys.exit(1 if failed else 0)
