# TODO: CLI Routing & DynDNS Automation

This document outlines how to automate the update of your public IP address to Cloudflare DNS using CLI-capable devices like RouterOS, OpenWRT, or DD-WRT.

## Prerequisites

1.  **Domain on Cloudflare**: You need a domain (e.g., `gogmagog.win`) managed by Cloudflare.
2.  **API Token**: Create a Cloudflare API Token with the following permissions:
    -   `Zone - DNS - Edit`
    -   `Zone - Zone - Read`
    -   *Restriction*: All zones (or specifically your domain).

## Option 1: RouterOS (MikroTik)

If you replace your Fritz!Box or put a MikroTik device behind it:

```bash
# Script to update Cloudflare A Record
:local CFToken "YOUR_CLOUDFLARE_TOKEN"
:local CFZoneID "YOUR_ZONE_ID"
:local CFRecordID "YOUR_RECORD_ID"
:local CFRecordName "camera.gogmagog.win"

:local currentIP [/ip address get [/ip address find interface=ether1] address]
:set currentIP [:pick $currentIP 0 [:find $currentIP "/"]]

/tool fetch http-method=put mode=https \
    url="https://api.cloudflare.com/client/v4/zones/$CFZoneID/dns_records/$CFRecordID" \
    http-header-field="Authorization: Bearer $CFToken,Content-Type: application/json" \
    http-data="{\"type\":\"A\",\"name\":\"$CFRecordName\",\"content\":\"$currentIP\",\"ttl\":120,\"proxied\":false}" \
    keep-result=no
```

## Option 2: OpenWRT / DD-WRT

Use the `ddns-scripts` package with the Cloudflare provider.

1.  `opkg update && opkg install ddns-scripts ddns-scripts-cloudflare curl`
2.  Configure via LuCI (Services -> Dynamic DNS) or `/etc/config/ddns`:
    -   **Lookup Hostname**: `camera.gogmagog.win`
    -   **Domain**: `camera@gogmagog.win`
    -   **Password**: Your API Token.
    -   **IP address source**: `network` (if WAN is on device) or `URL` (using `http://checkip.amazonaws.com`).

## Option 3: Fritz!Box (Legacy/Manual)

Fritz!Box allows custom DynDNS providers. However, Cloudflare's API requires a `PATCH` or `PUT` request with JSON, which the Fritz!Box native DynDNS client cannot easily do.

### The "Proxy" Solution
You can host a tiny script (e.g., a Cloudflare Worker) that accepts a simple GET request from the Fritz!Box and performs the complex API call to Cloudflare.

**Fritz!Box Update URL:**
`https://your-worker.workers.dev/update?ip=<ipaddr>&token=secret`

**Cloudflare Worker (Conceptual):**
```javascript
addEventListener('fetch', event => {
  event.respondWith(handleRequest(event.request))
})

async function handleRequest(request) {
  const { searchParams } = new URL(request.url)
  const ip = searchParams.get('ip')
  // ... perform Cloudflare API call here ...
  return new Response('OK')
}
```

## Organizational Steps

1.  **Domain Migration**: Move your domain's nameservers to Cloudflare.
2.  **Static Lease**: Ensure the camera has a static IP in the local network (Done).
3.  **Port Forwarding**: Ensure Port 81 (or your choice) is forwarded in the Router (Done).
4.  **Token Security**: Never commit the API Token to GitHub. Use GitHub Secrets for CI/CD and keep them local on your router.
