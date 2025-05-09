from pathlib import Path

def verify_file(file_path, replace: bool = False, verbose: bool = False) -> bool:
    """
    Ensure parent directories exist.  
    Return True if we should go ahead and (re‑)write the file.
    Return False if the file exists and replace=False.
    """
    p = Path(file_path)
    p.parent.mkdir(parents=True, exist_ok=True)

    if p.exists() and not replace:
        if verbose:
            print(f"verify_file: {p} already exists and replace=False → skipping")
        return False
    return True
