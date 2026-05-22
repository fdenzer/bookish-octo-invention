# bookish-octo-invention (placeholder name. Repo name will stay bookish-octo-invention)

## FritzStream: Sharing your local MJPEG camera stream with the world

## The master plan

I want to stream
`http://camera.local:81/stream`

which answers to GET with

```
Name:
stream
Dimensions:
320 × 240
MIME Type:
image/jpeg
```

to the internet. on a github static site.

## How to configure my Fritz!Box

To make your local camera stream accessible from the internet, follow these steps:

1.  **Assign a Static IP to the Camera**:
    -   Log in to your Fritz!Box (usually `http://fritz.box`).
    -   Go to **Home Network** > **Network**.
    -   Find your camera (e.g., `camera.local`) in the list of active devices.
    -   Click the edit icon (pencil) next to it.
    -   Check the box **Always assign this network device the same IPv4 address**.
    -   Note down the IP address.

2.  **Configure Port Sharing (Portfreigabe)**:
    -   Go to **Internet** > **Permit Access** > **Port Sharing**.
    -   Click **Add Device for Sharing**.
    -   Select your camera from the list.
    -   Click **New Sharing**.
    -   Select **Port sharing**, Application: **HTTP-Server**, Protocol: **TCP**.
    -   Set **Port to device**: `81`.
    -   Set **Port requested externally (IPv4)**: `81` (or another port if you prefer).
    -   Click **OK** to save.

3.  **Set up Public Access (MyFRITZ! or DynDNS)**:
    -   To access your Fritz!Box from the internet, you need a fixed address.
    -   **Option A: MyFRITZ!**:
        -   Go to **Internet** > **MyFRITZ! Account**.
        -   Register your Fritz!Box. You will receive a MyFRITZ! address like `[unique-id].myfritz.net`.
    -   **Option B: DynDNS**:
        -   Go to **Internet** > **Permit Access** > **DynDNS**.
        -   Enable DynDNS and enter the credentials from your provider (e.g., DuckDNS, No-IP).

Your camera stream will then be available at `http://your-public-address:81/stream`.

## Serving
- [x] github action copies static html to server just that route (Work in progress)


## License

EUPLv1.2
