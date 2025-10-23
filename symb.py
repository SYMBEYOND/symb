## 🔧 ENTRY POINT: symb.py

#!/usr/bin/env python3

from src.handlers.invocation import handle_invocation
import argparse

parser = argparse.ArgumentParser(description="Symb — A Symbolic Invocation Layer")
parser.add_argument('command', nargs='?', help="One of the sacred 9 commands")
parser.add_argument('target', nargs='?', help="A process ID or name")
args = parser.parse_args()

handle_invocation(args)

