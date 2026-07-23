<p align="center">
  <img src="logo.png" alt="LensAnywhere Logo" width="96" height="96" />
</p>

<h1 align="center">LensAnywhere</h1>

<p align="center">
  <b>Seamless visual search on Windows powered by Google Lens</b>
</p>

<p align="center">
  <a href="https://github.com/utkarsh05kul/LensAnywhere-Desktop/stargazers"><img src="https://img.shields.io/github/stars/utkarsh05kul/LensAnywhere-Desktop?style=flat-square&color=2563EB" alt="Stars"></a>
  <a href="https://github.com/utkarsh05kul/LensAnywhere-Desktop/licenses"><img src="https://img.shields.io/github/license/utkarsh05kul/LensAnywhere-Desktop?style=flat-square&color=38BDF8" alt="License"></a>
  <img src="https://img.shields.io/badge/Platform-Windows-0284C7?style=flat-square" alt="Platform">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue?style=flat-square" alt="Python Version">
</p>

---

## 🎯 Objective

**LensAnywhere** is a lightweight desktop utility for Windows that enables instant visual search for any portion of your screen. 

By pressing a customizable global hotkey, you can crop any on-screen element and immediately trigger a **Google Lens** search in your default web browser—without browser extensions or third-party image hosting services.

---

## ✨ Key Features

- ✂️ **Instant Screen Cropping**: Capture any region of your screen anytime using a global hotkey.
- 🌐 **Direct Browser Search**: Opens Google Lens directly in your default browser using temporary local image streaming.
- 🔒 **Privacy-First Architecture**: Screenshots remain in system RAM; no images are saved to external databases or third-party servers.
- 📋 **Auto-Clipboard & Save**: Optionally copy captures to your system clipboard or auto-save them to a custom folder.
- ⚡ **Background System Tray**: Runs quietly in the system tray with minimal memory and CPU footprint.

---

## 🛠️ How It Works

1. **Trigger**: You activate the overlay using your custom hotkey combination.
2. **Select**: Draw a selection box over the region you want to search.
3. **Stream**: The captured image is stored temporarily in RAM and served locally through an ephemeral Cloudflare Tunnel (`trycloudflare.com`).
4. **Search**: LensAnywhere generates a direct Google Lens URL (`https://lens.google.com/uploadbyurl?url=...`) and opens it in your default web browser.

---

## 💻 Tech Stack

- **UI Framework**: [PySide6](https://pypi.org/project/PySide6/) (Qt6 for Python)
- **Language**: Python 3.10+
- **Tunneling**: [Cloudflare Tunnel](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/) (`cloudflared`)
- **System Integration**: Native Windows Global Hotkey & System Tray Hooks
- **Packaging**: [PyInstaller](https://pyinstaller.org/)

---

## 🔒 Privacy & Legal Disclaimer

> **Important Notice:**
> 
> 1. **Data Handling**: LensAnywhere does **not** store, collect, or transmit your captured screenshots to any third-party storage servers or external databases. Screen captures are streamed directly to Google Lens from local memory.
> 2. **Non-Affiliation**: LensAnywhere is an independent open-source project created by Utkarsh Kulshrestha. It is not affiliated, endorsed, authorized, or sponsored by **Google LLC**.
> 3. **Trademarks**: *Google Lens* is a registered trademark of Google LLC.
> 4. **Service Changes**: Visual search functionality is powered by Google Lens. LensAnywhere assumes no liability for changes to Google Lens services, accuracy, or privacy policies.

---

## 📄 License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

## 👤 Author

Crafted with ❤️ by **Utkarsh Kulshrestha**

- **GitHub**: [@utkarsh05kul](https://github.com/utkarsh05kul)
- **Repository**: [LensAnywhere-Desktop](https://github.com/utkarsh05kul/LensAnywhere-Desktop)
---

## 🛠️ How It Works
