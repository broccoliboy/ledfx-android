# Alternative UI for Android TV (leanback) mode
# Super-simple HTTP server to show QR code for accessing the web UI on a mobile device

import base64
from functools import cache
from importlib import resources
from io import BytesIO
import os
import socket

import qrcode
from PIL import Image

from ports import LEDFX_PORT_LEANBACK, WEBVIEW_PORT
from aiohttp import web


@cache
def is_leanback():
    from jnius import autoclass

    # Determine if we're running on Android TV
    ctx = autoclass('org.kivy.android.PythonService').mService
    if not ctx:
        ctx = autoclass('org.kivy.android.PythonActivity').mActivity
    pm = ctx.getPackageManager()
    features = pm.getSystemAvailableFeatures()
    if features:
        for f in features:
            if f.name == pm.FEATURE_LEANBACK:
                return True
    return False


HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LedFx</title>
    <style>
        body {
            background-color: black;
            color: white;
            font-family: Arial, sans-serif;
            text-align: center;
            margin: 0;
            padding: 0;
        }
        .image-container {
            margin: 20px auto;
        }
        img {
            width: 300px;
            height: 300px;
            display: block;
            margin: 0 auto;
        }
        .navigate-button {
            margin-top: 20px;
            padding: 10px 20px;
            font-size: 16px;
            color: white;
            background-color: #007BFF;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            text-decoration: none;
        }
        .navigate-button:hover {
            background-color: #0056b3;
        }
        .button-row {
            display: flex;
            justify-content: center;
            gap: 20px;
        }
    </style>
</head>
<body>
    <h1>LedFx: Leanback Mode</h1>
    <div>Scan the QR code or navigate to <strong>{{ledfx_lan_address}}</strong> from your mobile device to control LedFx<br>Note: devices must be on the same LAN</div>
    <div class="image-container">
        <img src="{{qr_src}}">
    </div>
    <div class="button-row">
        <a href="{{ledfx_local_address}}" class="navigate-button">Open LedFx UI</a>
        <button id="exit-btn" class="navigate-button" style="background-color:#dc3545;">Shutdown</button>
    </div>
    <script>
    document.getElementById('exit-btn').onclick = function() {
        fetch('{{ledfx_local_address}}/api/power', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({action: 'shutdown'})
        }).then(response => {
            if (response.ok) {
                alert('Shutting down...');
            } else {
                alert('Failed to shutdown: ' + response.status);
            }
        }).catch(err => {
            alert('Error: ' + err);
        });
    };
    </script>
</body>
</html>
"""


def create_qr_with_logo(data, logo_path):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    qr_img = qr.make_image(fill_color='black', back_color='white').convert('RGB')

    if os.path.exists(logo_path):
        logo = Image.open(logo_path)
        logo_size = (qr_img.size[0] // 4, qr_img.size[1] // 4)
        logo = logo.resize(logo_size)
        pos = ((qr_img.size[0] - logo_size[0]) // 2, (qr_img.size[1] - logo_size[1]) // 2)
        qr_img.paste(logo, pos, mask=logo if logo.mode == 'RGBA' else None)

    return qr_img


@cache
def get_local_ip():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.connect(('10.254.254.254', 1))  # dummy address
        return s.getsockname()[0]


@cache
def get_html():
    try:
        local_ip = get_local_ip()
        ledfx_lan_address = f'http://{local_ip}:{LEDFX_PORT_LEANBACK}'
    except:
        ledfx_lan_address = None

    if ledfx_lan_address:
        with resources.path('res', 'icon.png') as logo_path:
            qr_img = create_qr_with_logo(ledfx_lan_address, logo_path)
        buffer = BytesIO()
        qr_img.save(buffer, format='png')
        buffer.seek(0)
        img_base64 = base64.b64encode(buffer.read()).decode('utf-8')
        qr_src = f'data:image/png;base64,{img_base64}'
    else:
        qr_src = ''
        ledfx_lan_address = 'Unable to determine local IP address'

    html = HTML_TEMPLATE.replace('{{qr_src}}', qr_src)
    html = html.replace('{{ledfx_lan_address}}', ledfx_lan_address)
    html = html.replace('{{ledfx_local_address}}', f'http://127.0.0.1:{LEDFX_PORT_LEANBACK}')
    
    return html


def serve():
    
    async def handle_root(request):
        html = get_html()
        return web.Response(text=html, content_type='text/html')

    app = web.Application()
    app.add_routes([
        web.get('/', handle_root),
    ])
    web.run_app(app, host='0.0.0.0', port=WEBVIEW_PORT)


if __name__ == '__main__':
    serve()
