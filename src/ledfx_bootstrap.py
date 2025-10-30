# Bootstrap script for starting LedFx on Android
# Will first try to use external storage for config directory with fallback to dedicated app storage
# If running on Android TV, will use alternate port for LedFx server so webview shows leanback UI

import logging
import os
import sys

from android.storage import app_storage_path, primary_external_storage_path

from leanback import is_leanback
from ports import LEDFX_PORT_LEANBACK, WEBVIEW_PORT


def start_ledfx():
    
    os.name = 'posix'  # Force os.name to 'posix' for compatibility
    sys.platform = 'linux'  # Force sys.platform to 'linux' for compatibility
    
    from ledfx.__main__ import main as ledfx_main
    from ledfx.config import CONFIG_DIRECTORY
        
    port = LEDFX_PORT_LEANBACK if is_leanback() else WEBVIEW_PORT
    
    try:
        # try to use external storage first
        config_dir = os.path.join(primary_external_storage_path(), CONFIG_DIRECTORY)
        os.makedirs(config_dir, exist_ok=True)
    except:
        # fall back to app storage directory if external storage is inaccessible
        config_dir = app_storage_path()
    
    # Reduce logging of noisy modules
    logging.getLogger('kivy.jnius.reflect').setLevel(logging.INFO)
    logging.getLogger('ledfx.api').setLevel(logging.INFO)
    
    sys.argv += [
        f'--config={config_dir}',
        f'--port={port}',
        '--offline',
    ]
    
    ledfx_main()
