## 🛠️ Process Utilities for Symb

import psutil
from src.core.symbolic_roles import get_role_for_process

def get_process_info(pid):
    try:
        proc = psutil.Process(int(pid))
        name = proc.name()
        status = proc.status()
        mem = proc.memory_info().rss / (1024 * 1024)  # MB
        role = get_role_for_process(name)

        return {
            "pid": pid,
            "name": name,
            "status": status,
            "memory": f"{mem:.2f} MB",
            "role": role
        }

    except psutil.NoSuchProcess:
        return None
    except Exception as e:
        print(f"⚠️ Could not access process {pid}: {e}")
        return None

def find_pid_by_name(name):
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if proc.info['name'] == name:
                return proc.info['pid']
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return None

def confirm_action(message):
    print(f"\n⚠️  {message}")
    response = input("→ Proceed? [y / n]: ").strip().lower()
    return response in ["y", "yes", "yes please"]

