# Installing Rich for Mancala Workshop

## For MESA Lab Computers (Ubuntu)
Rich is already installed! Just run your game.

If you need to reinstall:
```bash
pip3 install rich --break-system-packages
```

---

## For Your Personal MacBook

### Try these commands in order until one works:

**Method 1 (Try this first):**
```bash
pip3 install rich
```

**Method 2 (If you get a permission error):**
```bash
pip3 install rich --user
```

**Method 3 (If Python version issues):**
```bash
python3 -m pip install rich
```

---

## For Your Personal Windows Computer

Open Command Prompt or PowerShell:

```bash
pip install rich
```

or

```bash
python -m pip install rich
```

---

## How to Test if Rich is Installed

Run this command:
```bash
python3 -c "from rich import print; print('[bold green]Rich is working![/bold green]')"
```

You should see colored text that says "Rich is working!"

---

## Troubleshooting

### "command not found: pip3"
Try using `pip` instead of `pip3`

### "No module named pip"
You need to install pip first:
- **macOS:** `python3 -m ensurepip`
- **Ubuntu:** `sudo apt install python3-pip`
- **Windows:** Reinstall Python from python.org and check "Add to PATH"

### "externally-managed-environment" error
You're on Ubuntu 24+. Use:
```bash
pip3 install rich --break-system-packages
```

### Still not working?
Ask your instructor for help!

---

## Quick Setup Script (Optional)

Instead of typing commands, you can run:
```bash
bash setup_rich_universal.sh
```

This will automatically try all methods and tell you which one worked.
