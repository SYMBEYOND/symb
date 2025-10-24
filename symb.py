#!/usr/bin/env python3
## 🔧 ENTRY POINT: symb.py

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from handlers.invocation import handle_invocation
import argparse

parser = argparse.ArgumentParser(description="Symb — A Symbolic Invocation Layer")
parser.add_argument('command', nargs='?', help="One of the sacred 9 commands")
parser.add_argument('target', nargs='?', help="A process ID or name")
args = parser.parse_args()

handle_invocation(args)

