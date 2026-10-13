#!/usr/bin/env python3
"""Test old classifier_discourse on GNOME unclassified samples."""

import sys
from pathlib import Path
import os

repo_root = Path(__file__).resolve().parent.parent.parent
e121_path = repo_root / "EXPERIMENTS" / "121-codereview-e119"
sys.path.insert(0, str(e121_path))
old_cwd = Path.cwd()
os.chdir(e121_path)
from classifier_discourse import classify_discourse_item
os.chdir(old_cwd)

samples = [
    'Google Drive in GNOME 50',
    'Useful documentation for GTK',
    'Add a setting to change trackpad scroll speed',
    'Way to remove widgets',
    'How Install Gtk 4.X on Raspberry Pi OS (Debian)',
    'Install on mobile',
    'Pixel drawing with Cairo and GtkDrawingArea',
    'Gtk4 - Blueprint as default .ui format?',
    'File metadata and gio',
    'Changing bakground color and foreground color of tooltip',
    'Gtk4: Get the mouse position relative to widget',
    'Trying to compile GTK4 C code on Windows with Visual Studio 2022',
]

print('=== Old classifier_discourse on GNOME unclassified samples ===')
for s in samples:
    result = classify_discourse_item(s)
    print(f'  [{result:12s}] {s}')