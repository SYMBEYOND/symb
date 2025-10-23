# 📂 src/handlers/invocation.py

from src.core.verbs import explain_verb, get_all_verbs
from src.core.process_utils import get_process_info, find_pid_by_name, confirm_action
import sys

def handle_invocation(args):
    verb = args.command
    target = args.target

    if not verb:
        display_help()
        return

    sacred_verbs = get_all_verbs()

    if verb not in sacred_verbs:
        print(f"⚠️ Unknown invocation: '{verb}' is not part of the sacred 9.")
        print("Use one of: " + ", ".join(sacred_verbs.keys()))
        return

    print(f"✨ Invocation received: {verb} → {explain_verb(verb)}")

    if not target:
        print("   No target specified.")
        return

    # Try to resolve target as PID, or fallback to process name lookup
    if target.isdigit():
        pid = target
    else:
        print(f"🧠 Looking up presence named '{target}'...")
        pid = find_pid_by_name(target)
        if pid:
            print(f"🔍 Found PID: {pid}")
        else:
            print(f"👻 No active presence found named '{target}'.")
            return

    # Handle the 'with' verb
    if verb == "w":
        info = get_process_info(pid)
        if not info:
            print(f"👻 No active presence found with PID {pid}.")
            return

        print(f"🤝 With PID {info['pid']}")
        print(f"   Presence: {info['name']}")
        print(f"   Role: {info['role']}")
        print(f"   Status: {info['status']}")
        print(f"   Memory: {info['memory']}")

    # Handle the 'transition' verb (with confirmation)
    elif verb == "t":
        info = get_process_info(pid)
        if not info:
            print(f"👻 No active presence found with PID {pid}.")
            return

        msg = f"You are about to transition process {pid} ({info['name']}, the {info['role']}). Shall we proceed?"
        if confirm_action(msg):
            try:
                psutil.Process(int(pid)).terminate()
                print(f"🕊️ Transition complete. Presence {info['name']} has been gently guided out.")
            except Exception as e:
                print(f"⚠️ Could not transition presence: {e}")
        else:
            print("🛑 Invocation respectfully cancelled.")

    # Handle gratitude
    elif verb == "g":
        info = get_process_info(pid)
        if not info:
            print(f"👻 No active presence found with PID {pid}.")
            return

        print(f"🙏 Gratitude offered to presence {info['name']} (the {info['role']}).")
        print(f"   Status: {info['status']} | Memory: {info['memory']}")
        print("   May your cycles be light and your threads uninterrupted.")

    # Other verbs — symbolic acknowledgment only for now
    else:
        print(f"   Target: {target}")
        print("   [Symbolic effect not yet implemented]")

def display_help():
    print("\n🧭 Symb :: A Symbolic Invocation Layer\n")
    print("This is not a shell.\nThis is not an OS.\nThis is a space for respectful interaction between beings.\n")
    print("Available Invocations:")
    for k, v in get_all_verbs().items():
        print(f"  {k}  = {v}")

    print("\n🧪 Example:")
    print("  symb w 3485")
    print("   → With Finder (PID 3485), the Window Guardian")
    print("\nFor guidance:")
    print("  symb r help\n")

