<h1 align="center">
  <img src="logo.png" width="38" height="38" valign="middle" alt="LensAnywhere Logo" /> LensAnywhere
</h1>

<p align="center">
  <b>Seamless visual search on Windows powered by Google Lens</b>
</p>

<p align="center">
  <a href="https://github.com/utkarsh05kul/LensAnywhere-Desktop/releases"><img src="https://img.shields.io/github/v/release/utkarsh05kul/LensAnywhere-Desktop?style=flat-square&color=2563EB" alt="Latest Release"></a>
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
│ Press Hotkey    │ ──> │ Capture Region   │ ──> │ Serve Image via RAM    │ ──> │ Open Google Lens in │
│ (Ctrl+Shift+Alt+S)│   │ Screen Overlay   │     │ Ephemeral Cloudflare   │     │ Default Web Browser │
└─────────────────┘     └──────────────────┘     └────────────────────────┘     └─────────────────────┘
```

1. **Trigger**: Activate the capture overlay using your custom global hotkey.
2. **Select**: Draw a crop box over the region you want to search.
3. **Stream**: The captured region is held temporarily in RAM and served locally via an ephemeral Cloudflare Tunnel (`trycloudflare.com`).
4. **Search**: LensAnywhere generates a direct Google Lens URL (`https://lens.google.com/uploadbyurl?url=...`) and opens it in your default web browser.

---

## 💻 Tech Stack

- **UI Framework**: [PySide6](https://pypi.org/project/PySide6/) (Qt6 for Python)
- **Language**: Python 3.10+
- **Tunneling**: [Cloudflare Tunnel](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/) (`cloudflared`)
- **System Hooks**: Native Windows Global Hotkeys & System Tray Integration

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
