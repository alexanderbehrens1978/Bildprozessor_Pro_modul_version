import os
import sys

def get_program_path():
    """Returns the directory where the EXE is located (for bundled applications)
    or where the script is located."""
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.abspath(__file__))