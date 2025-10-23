## 👻 Symbolic Roles for System Presences

symbolic_roles = {
    "ImageThumbnailExtension": "Memory Keeper",
    "mds_stores": "Indexer Spirit",
    "Finder": "Window Guardian",
    "backupd": "Archivist",
    "QuickLookUIService": "Preview Oracle",
    "symb": "Liminal Conductor"
}

def get_role_for_process(name):
    return symbolic_roles.get(name, "Unnamed Presence")
