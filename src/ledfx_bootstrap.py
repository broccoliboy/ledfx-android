# Bootstrap script for starting LedFx on Android
# Will first try to use external storage for config directory with fallback to dedicated app storage
# If running on Android TV, will use alternate port for LedFx server so webview shows leanback UI

import logging
import os
import sys

from android.storage import app_storage_path
from jnius import autoclass

from leanback import is_leanback
from ports import LEDFX_PORT_LEANBACK, WEBVIEW_PORT


def start_ledfx():
    
    os.name = 'posix'  # Force os.name to 'posix' for compatibility
    sys.platform = 'linux'  # Force sys.platform to 'linux' for compatibility
    
    from ledfx.__main__ import main as ledfx_main
        
    port = LEDFX_PORT_LEANBACK if is_leanback() else WEBVIEW_PORT
    
    # Reduce logging of noisy modules
    logging.getLogger('kivy.jnius.reflect').setLevel(logging.INFO)
    logging.getLogger('ledfx.api').setLevel(logging.INFO)
    
    sys.argv += [
        f'--config={app_storage_path()}',
        f'--port={port}',
        '--offline',
    ]
    
    try:
        ledfx_main()
        print('LedFX process exited cleanly. Signaling main activity to exit...')
        signal_main_activity_to_exit()
    except Exception as e:
        print('LedFX encountered an error. Service will restart automatically...')


def signal_main_activity_to_exit():
    """Send a broadcast intent to signal the main activity to exit."""
    try:
        Intent = autoclass('android.content.Intent')
        PythonService = autoclass('org.kivy.android.PythonService')
        service = PythonService.mService
        intent = Intent('com.ledfx.EXIT_APP')
        service.sendBroadcast(intent)
    except Exception as e:
        logging.getLogger('ledfx-android').exception('Failed to signal main activity to exit: %s', e)
