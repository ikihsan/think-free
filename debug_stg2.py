#!/usr/bin/env python3
import subprocess
import os
import sys
import tempfile

d = tempfile.mkdtemp(prefix='debug2-')
subprocess.run(['git', 'init'], cwd=d, capture_output=True)
subprocess.run(['git', 'config', 'user.email', 'test@test'], cwd=d, capture_output=True)
subprocess.run(['git', 'config', 'user.name', 'Test'], cwd=d, capture_output=True)

# Write initial content and commit
with open(os.path.join(d, 'f'), 'w') as f:
    f.write('def foo():\n    x = 1\n    y = 2\n    return x + y\n')
print('Initial file content:')
with open(os.path.join(d, 'f'), 'r') as f:
    print(repr(f.read()))

subprocess.run(['git', 'add', 'f'], cwd=d, capture_output=True)
subprocess.run(['git', 'commit', '-m', 'init', '--no-gpg-sign'], cwd=d, capture_output=True)

# Now modify
with open(os.path.join(d, 'f'), 'w') as f:
    f.write('def foo():\n    x = 10\n    y = 20\n    return x + y\n')
print('After modify file content:')
with open(os.path.join(d, 'f'), 'r') as f:
    print(repr(f.read()))

print('git status:')
r = subprocess.run(['git', 'status'], cwd=d, capture_output=True, text=True)
print(r.stdout)

print('git diff:')
r2 = subprocess.run(['git', 'diff', '-U0', '--no-color'], cwd=d, capture_output=True, text=True)
print(r2.stdout)

print('git diff --cached:')
r3 = subprocess.run(['git', 'diff', '--cached', '-U0', '--no-color'], cwd=d, capture_output=True, text=True)
print(r3.stdout)

print('stg list:')
r4 = subprocess.run([sys.executable, '/home/ubuntu/think-free/stage-lines/stg', 'list'], cwd=d, capture_output=True, text=True)
print(r4.stdout)