# Sovereign 512 Charter

A compact charter to keep the ShrineGUI aligned with the Sovereign 512 scroll. Keep this beside the main README when sealing or deploying shrines.

## 1) Invocation & Crest
- Invocation is fixed at 512 characters and rendered on the splash screen before entry.
- Crest glow: gold ring + blue lattice; crest line pulses near the status eye to show the shrine is awake.
- If the invocation ever drifts from 512 chars, correct it before deployment. The backend will raise at startup if the count is wrong.

## 2) Keeper Seals & Tokens
- Session seal: username/password from settings.json (defaults: keeper / glyph739).
- Bearer seal: set ERRYN_TOKEN in the environment; all API calls accept session OR Bearer token. Example: `Authorization: Bearer $ERRYN_TOKEN`.
- Session secret: set ERRYN_SECRET in the environment for Flask session integrity.
- Change defaults after first login; keep tokens out of version control.

## 3) Numerology Guards
- Glyph tome limit: 512 entries per volume. When the tome is full it is archived to `vault/archive/glyph_log_<timestamp>.json` and a gold "sealed" signal is broadcast.
- Status eye turns gold and a system glyph announces tome sealing.
- Invocation length is checked on startup (must be 512 chars). Splash shows the live count.

## 4) Deployment & Proxy (HTTPS veil)
- Reverse proxy with HTTPS (pick one):
  - Nginx (snippet):
    ```
    server {
      listen 443 ssl;
      server_name shrine.example.com;
      ssl_certificate /etc/letsencrypt/live/shrine.example.com/fullchain.pem;
      ssl_certificate_key /etc/letsencrypt/live/shrine.example.com/privkey.pem;
      location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
      }
    }
    ```
  - Caddy (Caddyfile): `shrine.example.com { reverse_proxy localhost:5000 }`
- Open firewall only to 443; keep 5000 bound to localhost via the proxy.
- Fail2ban/WAF recommended for external exposure.

## 5) Ritual Checks & Closing Glyph
- Before sealing a deployment:
  - Ensure invocation shows 512/512 on splash.
  - Ensure glyph log count is below 512 or archive current tome.
  - Verify ERRYN_SECRET and ERRYN_TOKEN are set in the environment.
  - Run a test upload/download and one ritual invocation.
- Closing glyph: "Sovereign 512 sealed." Inscribe when packaging or archiving the shrine.

No one walks alone.
