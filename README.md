# RuneKit Reforged

**Alt1-compatible toolkit for RuneScape 3 on Linux.**

RuneKit Reforged lets you run [Alt1 toolkit](https://runeapps.org/alt1) apps (clue solvers, XP meters, AFK timers, and more) alongside the **official RuneScape 3 client** on Linux. It works by reading your game screen through screenshots — it does not modify the game client.

Reforged from the original [whs/runekit](https://github.com/whs/runekit) which was abandoned in 2021. Rebuilt with Python 3.12, Qt6, and modern dependencies for a stable experience on current Linux distros.

---

## What You Need

| Requirement | Details |
|---|---|
| **OS** | Linux (X11) |
| **Python** | 3.11, 3.12, 3.13, or 3.14 |
| **RuneScape 3** | Official client must be **running** before you start RuneKit |
| **Display server** | X11 required (Wayland is not supported) |

---

## Quick Start

### Step 1: Install system dependencies

**Ubuntu / Debian / Linux Mint:**
```sh
sudo apt install -y python3-full pipx libxcb-cursor0
```

**Fedora:**
```sh
sudo dnf install -y python3 pipx libxcb-cursor
```

**Arch Linux:**
```sh
sudo pacman -S python pipx xcb-util-cursor
```

### Step 2: Install Poetry (Python package manager)

```sh
pipx install poetry
```

If `pipx` says to add `~/.local/bin` to your PATH, do that:
```sh
# Add to your ~/.bashrc or ~/.zshrc:
export PATH="$HOME/.local/bin:$PATH"
```

Then restart your terminal or run `source ~/.bashrc`.

### Step 3: Clone and install RuneKit Reforged

```sh
git clone https://github.com/Jcapehart2/RuneKit-Reforged.git
cd RuneKit-Reforged
poetry install
```

This creates a virtual environment and installs all Python dependencies. It may take a minute.

### Step 4: Build resources

```sh
poetry run make dev
```

### Step 5: Launch

1. **Start RuneScape 3 first** (the official client)
2. Then run:

```sh
poetry run python main.py
```

3. A **system tray icon** will appear in your panel (top-right area)
4. **Right-click the tray icon** to see available Alt1 apps
5. On first launch, RuneKit downloads the default app list from runeapps.org

### One-Click Launcher

After initial setup, you can use the included launcher script:

```sh
./RuneKit.sh
```

This script checks for dependencies and launches RuneKit. You can double-click it in your file manager too (make sure it's marked executable with `chmod +x RuneKit.sh`).

---

## Available Alt1 Apps

RuneKit automatically downloads these apps on first launch:

| App | What it does |
|---|---|
| **AFKWarden** | Alerts you when you stop gaining XP or need attention |
| **Clue Solver** | Solves clue scroll puzzles, compass clues, and map clues |
| **Stats** | Shows your skill stats and XP tracking |
| **XpMeter** | Real-time XP/hour tracking overlay |
| **RS Wiki** | Quick item/NPC/object lookup from the RS Wiki |
| **DgKey** | Dungeoneering key tracker |
| **Droplogger** | Logs your drops for tracking loot |

You can also load any custom Alt1 app by URL:
```sh
poetry run python main.py https://runeapps.org/apps/alt1/afkscape/appconfig.json
```

Or add apps through the Settings UI:

1. Right-click the system tray icon and open **Settings**
2. Go to the **Applications** tab
3. Click the **+** button
4. Paste the app's `appconfig.json` URL (e.g. `https://runeapps.org/apps/alt1/afkscape/appconfig.json`)

> **Note:** `alt1://addapp/` links (used on runeapps.org to install apps with one click) are not currently supported. If a website gives you an `alt1://` link, copy the URL from the link, strip the `alt1://addapp/` prefix, and paste the remaining `appconfig.json` URL into the Settings dialog instead.

---

## Troubleshooting

### "No game instance found"

- Make sure RuneScape 3 is **running** before you start RuneKit
- RuneKit looks for a window named "RuneScape". If your window has a different name, set:
  ```sh
  export RK_WM_APP_NAME="YourWindowName"
  ```

### Tray icon doesn't appear

- Some desktop environments hide tray icons. Check your panel settings
- On GNOME, you may need the [AppIndicator extension](https://extensions.gnome.org/extension/615/appindicator-support/)

### Black screen / overlay issues

- RuneKit requires **X11**. If you're on Wayland, switch to an X11 session at the login screen
- Or run with XWayland: `QT_QPA_PLATFORM=xcb poetry run python main.py`

### "Failed to load module xapp-gtk3-module"

- This is a harmless warning from your desktop environment. Ignore it.

### "GBM is not supported" / Vulkan fallback

- This is normal — Qt WebEngine falls back to Vulkan rendering. Everything works fine.

---

## Bug Reports

If something isn't working, please open a GitHub Issue and **include your log file**.

RuneKit automatically saves logs to:

```
~/.config/cupco.de/RuneKit/logs/runekit.log
```

Logs rotate automatically (3 files, 1MB each) so they won't fill your disk.

**To submit a bug report:**

1. Reproduce the issue
2. Find your log file (see path above)
3. Open a [GitHub Issue](https://github.com/Jcapehart2/RuneKit-Reforged/issues/new) with:
   - What you were doing when it broke
   - Your distro and desktop environment (e.g., "Ubuntu 24.04, GNOME on X11")
   - Attach or paste your `runekit.log` file

---

## Settings

Open the settings dialog:
```sh
poetry run python main.py settings
```

---

## Debugging

Enable the Chromium remote debugger:
```sh
poetry run python main.py --remote-debugging-port=9222
```
Then open `chrome://inspect` in Chrome/Chromium to debug Alt1 apps.

---

## Building an AppImage

```sh
poetry run make dist/RuneKit.AppImage
```

---

## macOS Support (Experimental)

The codebase includes macOS support inherited from the original RuneKit project, but it has **not been tested** after the Qt6 migration. If you're on macOS and want to try it, contributions and bug reports are welcome.

---

## Tech Stack

- **Python 3.11–3.14** with [Poetry](https://python-poetry.org) for dependency management
- **PySide6 / Qt6** for the UI, web engine, and overlay system
- **OpenCV** and **Pillow** for image processing (screen capture)
- **xcffib** for X11 window detection

---

## License

This project is [licensed](LICENSE) under GPLv3, and contains code from [third parties](THIRD_PARTY_LICENSE.md).
Contains code from the Alt1 application.

Please do not contact Alt1 or RuneApps.org for support with RuneKit Reforged.
