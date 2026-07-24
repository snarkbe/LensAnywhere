<h1 align="center">
  <img src="logo.png" width="38" height="38" valign="middle" alt="LensAnywhere Logo" /> LensAnywhere
</h1>

<p align="center">
  <b>Seamless visual search on Windows powered by Google Lens</b>
</p>

<p align="center">
  <a href="https://github.com/utkarsh05kul/LensAnywhere-Desktop/releases"><img src="https://img.shields.io/badge/release-v1.0.0-2563EB?style=flat-square" alt="Latest Release"></a>
  <a href="https://github.com/utkarsh05kul/LensAnywhere-Desktop/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-38BDF8?style=flat-square" alt="MIT License"></a>
  <img src="https://img.shields.io/badge/Platform-Windows-0284C7?style=flat-square" alt="Platform">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue?style=flat-square" alt="Python Version">
</p>

---

## 🎯 Objective

**LensAnywhere** is a lightweight desktop utility for Windows that enables instant visual search for any portion of your screen. 

By pressing a customizable global hotkey, you can crop any on-screen element and immediately trigger a **Google Lens** search in your default web browser—without browser extensions or third-party image hosting services.

---

## 🚀 Download Desktop App (Executable)

If you just want to use the app without running Python scripts:

1. Go to the **[GitHub Releases Page](https://github.com/utkarsh05kul/LensAnywhere-Desktop/releases)**.
2. Download the latest `LensAnywhere.exe` file.
3. Run `LensAnywhere.exe` directly—no installation or extra setup required!

---

## ✨ Key Features

- ✂️ **Instant Region Cropping**: Capture any screen region using a global hotkey combination.
- 🌐 **Direct Lens Search**: Opens visual search directly in your browser with zero 3rd-party image uploads.
- 📋 **Clipboard & Auto-Save**: Optionally copy captures to your clipboard or save directly to a designated folder.
- ⚡ **Background System Tray**: Runs quietly in the system tray with minimal memory and CPU usage.

---

## 🛠️ How It Works

```
┌─────────────────┐     ┌──────────────────┐     ┌────────────────────────┐     ┌─────────────────────┐
│ Press Hotkey    │ ──> │ Capture Region   │ ──> │ Upload Image Directly  │ ──> │ Open Google Lens in │
│ (Ctrl+Shift+Alt+S)│   │ Screen Overlay   │     │ to Google Lens (HTTPS) │     │ Default Web Browser │
└─────────────────┘     └──────────────────┘     └────────────────────────┘     └─────────────────────┘
```

1. **Trigger**: Activate the capture overlay using your custom global hotkey.
2. **Select**: Draw a crop box over the region you want to search.
3. **Upload**: The captured region is held in RAM and POSTed directly to Google Lens (`https://lens.google.com/upload`) over a single outbound HTTPS request — nothing is ever served or exposed publicly.
4. **Search**: LensAnywhere follows the redirect Google Lens returns and opens the resulting search page in your default web browser.

---

## 💻 Tech Stack

- **UI Framework**: [PySide6](https://pypi.org/project/PySide6/) (Qt6 for Python)
- **Language**: Python 3.10+
- **System Hooks**: Native Windows Global Hotkeys & System Tray Integration

---

## 🛡️ Security & Antivirus False Positives

Earlier versions shipped a background Cloudflare Tunnel (`cloudflared`) to
expose the capture at a public URL that Google Lens's servers would fetch —
a background subprocess plus a persistent outbound tunnel is exactly the
pattern antivirus/SmartScreen heuristics flag. That whole mechanism has been
removed: captures are now POSTed directly to `https://lens.google.com/upload`
over a single outbound HTTPS request, the same way a browser upload works.
There is no tunnel, no bundled `cloudflared.exe`, no locally-listening HTTP
server, and no public exposure window at all.

This removes the main source of AV false positives outright, but a couple of
things are worth knowing about the new upload path:

- **GDPR consent cookie**: anonymous requests to Google from an EU/EEA IP are
  otherwise served a cookie-consent interstitial instead of the expected
  redirect. The upload request sends the long-standing `CONSENT=YES+` cookie
  used by Google-scraping tools to skip that interstitial.
- **Unofficial endpoint**: `lens.google.com/upload` isn't a documented public
  API — it's the same endpoint the Lens website itself uses for file
  uploads, reverse-engineered like the previous `uploadbyurl` approach. It
  could change without notice.
- **Build**: release binaries are still built one-folder (`--onedir`) with
  UPX compression disabled (`--noupx`, see `LensAnywhere.spec`) rather than a
  single UPX-packed `--onefile` executable, which lowers the entropy/packing
  signature that static AV engines key on.

Two additional steps further reduce SmartScreen/Defender false positives but
require an account/cost and can't be automated in this repo:

- **Code-signing** the released executable with a code-signing certificate
  (e.g. an OV cert from Sectigo/SSL.com) — by far the most effective lever
  against reputation-based warnings.
- **Submitting** the built binary to
  [Microsoft Security Intelligence](https://www.microsoft.com/en-us/wdsi/filesubmission)
  so Defender/SmartScreen can build reputation for it ahead of releases.

---

## 🔒 Privacy & Legal Disclaimer

> **Important Notice:**
> 
> 1. **Data Handling**: LensAnywhere does **not** store, collect, or transmit your captured screenshots to any external server or third-party storage service. Screen captures are passed directly to Google Lens in your default browser.
> 2. **Non-Affiliation**: LensAnywhere is an independent open-source utility created by Utkarsh Kulshrestha and is not affiliated, endorsed, authorized, or in any way officially connected with **Google LLC**.
> 3. **Trademarks**: *Google Lens* is a registered trademark of Google LLC.
> 4. **Service Changes**: Visual search functionality is powered by Google Lens. LensAnywhere holds no responsibility for search accuracy or changes to Google Lens policies and services.

---

## 📄 License

This project is licensed under the **[MIT License](LICENSE)**.

---

## 👤 Author

Crafted with ❤️ by **Utkarsh Kulshrestha**

- **GitHub**: [@utkarsh05kul](https://github.com/utkarsh05kul)
- **Repository**: [LensAnywhere-Desktop](https://github.com/utkarsh05kul/LensAnywhere-Desktop)
```
