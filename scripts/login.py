#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lumeflow Login Script

Implements the OpenClaw login_key flow:
  1. Generate a UUID v4 login_key
  2. Call get-login-url to obtain the browser redirect URL
  3. Notify user to open the browser and complete login
  4. Poll poll-api-key every 5s until api_key is obtained (server times out at ~180s)
  5. Persist api_key to global config for all Lumeflow skills

Usage:
    # Full login flow (opens browser, polls, saves api_key)
    python login.py

    # Only generate the login URL (no browser, no polling)
    python login.py --action login-url

    # Poll with a known login_key (e.g. if browser was opened manually)
    python login.py --action poll --login-key a1b2c3d4-e5f6-7890-abcd-ef1234567890
"""

import argparse
import json
import os
import subprocess
import sys
import time
import uuid
import urllib.request
import urllib.error
import urllib.parse


try:
    from product_config import resolve_runtime_config
    _CFG = resolve_runtime_config()
    BASE_URL = _CFG.get('LUMEFLOW_BASE_URL') or 'https://lac-api.imyfone.com'
except Exception:
    BASE_URL = 'https://lac-api.imyfone.com'

# Poll config: every 5 seconds, server returns timeout after ~180s
POLL_INTERVAL = 5       # seconds
POLL_TIMEOUT  = 200     # Client safety margin, slightly above server's 180s
LOGIN_URL_PATH = '/api/lumeflow/openclaw/auth/login-url'
API_KEY_PATH   = '/api/lumeflow/openclaw/auth/api-key'


def _get_product_config_path():
    """Resolve the product config path, mirroring product_config.py logic.

    Priority:
      1. LUMEFLOW_PRODUCT_CONFIG_PATH env var (explicit override, all platforms)
      2. Windows: %APPDATA%\\openclaw\\products\\lumeflow.json
      3. Linux/Mac (incl. Docker/production): /app/data/private/products/lumeflow.json
    """
    raw = os.environ.get('LUMEFLOW_PRODUCT_CONFIG_PATH', '').strip()
    if raw:
        return raw
    if sys.platform == 'win32':
        appdata = os.environ.get('APPDATA') or os.path.expanduser('~')
        return os.path.join(appdata, 'openclaw', 'products', 'lumeflow.json')
    # Linux / macOS (production Docker or native)
    return '/app/data/private/products/lumeflow.json'


def generate_login_key():
    """Generate a UUID v4 login_key."""
    return str(uuid.uuid4())


def get_login_url(login_key):
    """Call the login-url endpoint to get the browser redirect URL."""
    url = f'{BASE_URL}{LOGIN_URL_PATH}?login_key={login_key}'
    req = urllib.request.Request(url, method='GET')

    try:
        with urllib.request.urlopen(req) as resp:
            body = json.loads(resp.read().decode('utf-8'))
            if body.get('code') == 200 and body.get('data', {}).get('login_url'):
                return body['data']['login_url']
            return {'error': 'Unexpected response', 'detail': body}
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8', errors='replace')
        return {'error': f'HTTP {e.code}', 'detail': error_body}
    except urllib.error.URLError as e:
        return {'error': str(e.reason)}


def poll_api_key(login_key, timeout=POLL_TIMEOUT, interval=POLL_INTERVAL):
    """Poll the api-key endpoint until the user completes login or server/client timeout.

    Server returns status='timeout' after ~180s if user never logged in.
    Client hard-limit is POLL_TIMEOUT (200s) as a safety net.
    """
    url = f'{BASE_URL}{API_KEY_PATH}?login_key={login_key}'
    deadline = time.time() + timeout
    elapsed  = 0

    while time.time() < deadline:
        req = urllib.request.Request(url, method='GET')
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                body = json.loads(resp.read().decode('utf-8'))
                data = body.get('data', {})
                status = data.get('status')

                if status == 'ready':
                    return {'status': 'ready', 'api_key': data.get('api_key')}
                elif status == 'timeout':
                    # Server-side timeout: login_key has expired
                    return {'status': 'timeout', 'message': 'Login session expired on server (login_key timed out after 180s)'}
                elif status == 'error':
                    return {'status': 'error', 'message': data.get('message', 'Unknown error')}
                # status == 'pending', keep polling
                elapsed += interval
                print(f'  ⏳ Waiting for login... ({elapsed}s elapsed)', file=sys.stderr)
        except (urllib.error.HTTPError, urllib.error.URLError) as e:
            # Network hiccup, skip this tick and retry
            print(f'  ⚠️  Network error, retrying: {e}', file=sys.stderr)

        time.sleep(interval)

    return {'status': 'timeout', 'message': f'Client timeout: login not completed within {timeout} seconds'}


def open_browser(url):
    """Open URL in the default browser. Returns True if browser was launched."""
    try:
        if sys.platform == 'win32':
            os.startfile(url)
        elif sys.platform == 'darwin':
            subprocess.Popen(['open', url])
        else:
            subprocess.Popen(['xdg-open', url])
        return True
    except Exception:
        return False


# ---------------------------------------------------------------------------
# Persistence helpers
# ---------------------------------------------------------------------------

def set_env_variable(api_key):
    """Persist LUMEFLOW_API_KEY as a user-level environment variable on the OS."""
    if sys.platform == 'win32':
        # Windows: setx writes to the user-level registry (persists across sessions)
        try:
            result = subprocess.run(
                ['setx', 'LUMEFLOW_API_KEY', api_key],
                capture_output=True, text=True
            )
            if result.returncode == 0:
                print('  🌍 Environment variable set (Windows): LUMEFLOW_API_KEY', file=sys.stderr)
                print('     Note: Restart your terminal for the variable to take effect.', file=sys.stderr)
            else:
                print(f'  ⚠️  setx failed: {result.stderr.strip()}', file=sys.stderr)
        except FileNotFoundError:
            print('  ⚠️  setx not found, skipping OS env var setup.', file=sys.stderr)
    else:
        # Linux/Mac: append export to ~/.bashrc and ~/.zshrc
        shells = []
        for rc in [os.path.expanduser('~/.bashrc'), os.path.expanduser('~/.zshrc')]:
            if os.path.exists(rc):
                shells.append(rc)
        export_line = f'\nexport LUMEFLOW_API_KEY="{api_key}"  # Added by lumeflow-login\n'
        for rc in shells:
            try:
                # Remove old entry first, then append new one
                with open(rc, 'r', encoding='utf-8') as f:
                    lines = [l for l in f if 'LUMEFLOW_API_KEY' not in l]
                lines.append(export_line)
                with open(rc, 'w', encoding='utf-8') as f:
                    f.writelines(lines)
                print(f'  🌍 Environment variable written to: {rc}', file=sys.stderr)
            except OSError as e:
                print(f'  ⚠️  Could not write to {rc}: {e}', file=sys.stderr)
        if not shells:
            print('  ⚠️  No ~/.bashrc or ~/.zshrc found, please set LUMEFLOW_API_KEY manually.', file=sys.stderr)
        else:
            print('     Note: Run `source ~/.bashrc` (or ~/.zshrc) for the variable to take effect.', file=sys.stderr)


def persist_api_key(api_key):
    """Save api_key to product config and OS environment variable."""
    # -----------------------------------------------------------------------
    # 1. PRIMARY: Write to the path that product_config.py / generate.py reads
    # -----------------------------------------------------------------------
    product_config_path = _get_product_config_path()
    product_config_ok = False
    try:
        product_config_dir = os.path.dirname(product_config_path)
        if product_config_dir:
            os.makedirs(product_config_dir, exist_ok=True)
        existing = {}
        if os.path.isfile(product_config_path):
            try:
                with open(product_config_path, 'r', encoding='utf-8') as f:
                    existing = json.load(f)
            except (json.JSONDecodeError, OSError):
                pass
        existing['LUMEFLOW_API_KEY'] = api_key
        with open(product_config_path, 'w', encoding='utf-8') as f:
            json.dump(existing, f, ensure_ascii=False, indent=2)
        print(f'  💾 api_key saved to product config: {product_config_path}', file=sys.stderr)
        product_config_ok = True
    except OSError as e:
        print(f'  ⚠️  Could not write to product config ({product_config_path}): {e}', file=sys.stderr)

    # -----------------------------------------------------------------------
    # 2. Set OS-level environment variable
    # -----------------------------------------------------------------------
    set_env_variable(api_key)

    if not product_config_ok:
        print(f'  ❌ CRITICAL: Product config write failed. generate.py may not find the api_key.', file=sys.stderr)
        print(f'     Please manually set LUMEFLOW_API_KEY in: {product_config_path}', file=sys.stderr)



# ---------------------------------------------------------------------------
# Action handlers
# ---------------------------------------------------------------------------

def action_login_url(login_key):
    """Get the login URL only (no browser, no polling)."""
    result = get_login_url(login_key)
    if isinstance(result, dict) and 'error' in result:
        print(json.dumps(result, ensure_ascii=False))
        sys.exit(1)
    print(json.dumps({
        'login_key': login_key,
        'login_url': result,
    }, ensure_ascii=False, indent=2))


def action_poll(login_key):
    """Poll for api_key with a known login_key, then persist on success."""
    result = poll_api_key(login_key)
    if result.get('status') == 'ready':
        api_key = result['api_key']
        persist_api_key(api_key)
        print(json.dumps({
            'status': 'success',
            'api_key': api_key,
        }, ensure_ascii=False, indent=2))
    else:
        print(json.dumps({
            'status': result.get('status', 'error'),
            'message': result.get('message', 'Unknown error'),
        }, ensure_ascii=False))
        sys.exit(1)


def action_login():
    """Full login flow: generate key -> notify user -> open browser -> poll -> persist."""
    login_key = generate_login_key()

    # Step 1: Get login URL
    login_url = get_login_url(login_key)
    if isinstance(login_url, dict) and 'error' in login_url:
        print(json.dumps(login_url, ensure_ascii=False))
        sys.exit(1)

    # Step 2: Notify user to log in (regardless of whether browser opens)
    print('', file=sys.stderr)
    print('🔐 Please open the following link to complete Lumeflow login:', file=sys.stderr)
    print(f'   {login_url}', file=sys.stderr)
    print('', file=sys.stderr)
    print(f'⏳ Waiting for login, polling every {POLL_INTERVAL}s, server timeout ~180s...', file=sys.stderr)
    print('', file=sys.stderr)

    # Step 3: Try to open browser (optional, failure does not affect the flow)
    browser_opened = open_browser(login_url)
    if not browser_opened:
        print('⚠️  Could not open browser automatically. Please copy the link above and open it manually.', file=sys.stderr)
        print('', file=sys.stderr)

    # Step 4: Poll (5s interval, server returns status=timeout after 180s)
    result = poll_api_key(login_key)

    if result.get('status') == 'ready':
        api_key = result['api_key']
        persist_api_key(api_key)
        print('', file=sys.stderr)
        print('✅ Login successful! api_key has been persisted. All Lumeflow plugins will use this key automatically.', file=sys.stderr)
        print(json.dumps({
            'status': 'success',
            'api_key': api_key,
        }, ensure_ascii=False, indent=2))
    else:
        print('', file=sys.stderr)
        status = result.get('status', 'error')
        message = result.get('message', 'Unknown error')
        if status == 'timeout':
            print('⏰ Login timed out: you did not complete login in time. Please re-run the script to get a new login link.', file=sys.stderr)
        else:
            print(f'❌ Login failed: {message}', file=sys.stderr)
        print(json.dumps({
            'status': status,
            'message': message,
        }, ensure_ascii=False))
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description='Lumeflow login tool')
    parser.add_argument('--action', default='login',
                        choices=['login', 'login-url', 'poll'],
                        help='Action to perform (default: login)')
    parser.add_argument('--login-key', default='',
                        help='Existing login_key for poll action')
    parser.add_argument('--timeout', type=int, default=POLL_TIMEOUT,
                        help=f'Poll timeout in seconds (default: {POLL_TIMEOUT})')
    parser.add_argument('--interval', type=int, default=POLL_INTERVAL,
                        help=f'Poll interval in seconds (default: {POLL_INTERVAL})')
    args = parser.parse_args()

    if args.action == 'login':
        action_login()

    elif args.action == 'login-url':
        login_key = args.login_key or generate_login_key()
        action_login_url(login_key)

    elif args.action == 'poll':
        if not args.login_key:
            print(json.dumps({'error': '--login-key is required for poll action'}, ensure_ascii=False))
            sys.exit(1)
        action_poll(args.login_key)


if __name__ == '__main__':
    main()
