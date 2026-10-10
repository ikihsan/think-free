<!-- origin-meta
owner: EXPERIMENTS/092-module-provider-demand/PROTOCOL.md
status: active
last-verified: 2026-10-10
-->

# E092 Discrimination Test Results

Positive controls: 20
Negative controls: 20

=== POSITIVE CONTROLS (expected: module-only) ===
  ✓ so-1: module-only (expected module-only) - ImportError: No module named 'sklearn'
  ✓ so-2: module-only (expected module-only) - ModuleNotFoundError: No module named 'PIL'
  ✓ so-3: module-only (expected module-only) - ImportError: No module named 'cv2'
  ✓ so-4: module-only (expected module-only) - No module named 'yaml'
  ✓ so-5: module-only (expected module-only) - ModuleNotFoundError: No module named 'bs4'
  ✓ so-6: module-only (expected module-only) - ImportError: No module named 'dateutil'
  ✓ so-7: module-only (expected module-only) - No module named 'serial'
  ✓ so-8: module-only (expected module-only) - ImportError: No module named 'attr'
  ✓ so-9: module-only (expected module-only) - ModuleNotFoundError: No module named 'Crypto'
  ✓ so-10: module-only (expected module-only) - ImportError: No module named 'skimage'
  ✓ so-11: module-only (expected module-only) - No module named 'redis'
  ✓ so-12: module-only (expected module-only) - ModuleNotFoundError: No module named 'pymongo'
  ✓ so-13: module-only (expected module-only) - ImportError: No module named 'dotenv'
  ✓ so-14: module-only (expected module-only) - No module named 'jwt'
  ✓ so-15: module-only (expected module-only) - ModuleNotFoundError: No module named 'magic'
  ✓ so-16: module-only (expected module-only) - ImportError: No module named 'ldap'
  ✓ so-17: module-only (expected module-only) - No module named 'mysql'
  ✓ so-18: module-only (expected module-only) - ModuleNotFoundError: No module named 'psycopg2'
  ✓ so-19: module-only (expected module-only) - ImportError: No module named 'requests'
  ✓ so-20: module-only (expected module-only) - No module named 'flask'

=== NEGATIVE CONTROLS (expected: NOT module-only) ===
  ✓ so-neg-1: module-and-dist (expected module-and-dist) - ImportError after installing scikit-learn: No module named '
  ✓ so-neg-2: module-and-dist (expected module-and-dist) - pip install pillow but ImportError: No module named 'PIL'
  ✓ so-neg-3: module-and-dist (expected module-and-dist) - ModuleNotFoundError: No module named 'cv2' after pip install
  ✓ so-neg-4: environment (expected environment) - Virtualenv activation issue: ImportError in one env but not
  ✓ so-neg-5: environment (expected environment) - sys.path issue: ModuleNotFoundError for local package
  ✓ so-neg-6: stdlib (expected stdlib) - ImportError: No module named 'os'
  ✓ so-neg-7: stdlib (expected stdlib) - ModuleNotFoundError: No module named 'sys'
  ✓ so-neg-8: environment (expected environment) - Multiple Python versions: import works in 3.8 but not 3.10
  ✓ so-neg-9: environment (expected environment) - pip install numpy but ImportError in Jupyter notebook
  ✓ so-neg-10: environment (expected environment) - conda install vs pip install: ImportError for pandas
  ✓ so-neg-11: stdlib (expected stdlib) - ImportError: No module named 'json'
  ✓ so-neg-12: stdlib (expected stdlib) - ModuleNotFoundError: No module named 'datetime'
  ✓ so-neg-13: module-and-dist (expected module-and-dist) - Issue: ImportError after pip install -r requirements.txt
  ✓ so-neg-14: module-and-dist (expected module-and-dist) - Bug report: ModuleNotFoundError for 'torch' in CI
  ✗ so-neg-15: module-only (expected environment) - ImportError for local module 'utils'
  ✗ so-neg-16: environment (expected module-and-dist) - Docker build fails: ModuleNotFoundError for 'psycopg2'
  ✓ so-neg-17: stdlib (expected stdlib) - ImportError: No module named 'pathlib' in Python 3.6
  ✓ so-neg-18: stdlib (expected stdlib) - ModuleNotFoundError: No module named 'typing' in Python 3.4
  ✓ so-neg-19: module-and-dist (expected module-and-dist) - poetry install but ImportError for 'click'
  ✓ so-neg-20: environment (expected environment) - ImportError in pytest but not in python -m

Positive accuracy: 20/20 = 1.00
Negative accuracy: 18/20 = 0.90
Overall accuracy: 38/40 = 0.95

G2 PASSES: Discrimination test passed (accuracy >= 0.80)