# NinjaArt

A network infrastructure penetration testing tool - a fork and enhancement of SPARTA.

## Enhanced by
[Bushidokarat3](https://github.com/bushidokarat3)

## Original Framework Authors
**SECFORCE**
- Antonio Quina (@st3r30byt3)
- Leonidas Stavliotis (@lstavliotis)

---

## Description

NinjaArt is a Python GUI application which simplifies network infrastructure penetration testing by aiding the penetration tester in the scanning and enumeration phase. It allows the tester to save time by having point-and-click access to their toolkit and by displaying all tool output in a convenient way. If little time is spent setting up commands and tools, more time can be spent focusing on analysing results.

Despite the automation capabilities, the commands and tools used are fully customisable as each tester has their own methods, habits and preferences.

---

## What's New in This Fork

### Core Upgrades
- **Python 3 Support** - Fully ported from Python 2 to Python 3
- **PyQt5 Migration** - Upgraded from PyQt4 to PyQt5 for modern GUI support
- **Removed Elixir Dependency** - Replaced with direct SQLAlchemy ORM for improved database handling

### New Features

#### NetExec (nxc) Integration
Full integration with NetExec (formerly CrackMapExec) for comprehensive network enumeration:
- Dedicated **Nxc tab** with GUI interface for building and running nxc commands
- **SMB Enumeration**: users, groups, shares, sessions, disks, RID brute-forcing
- **Password Policy Checks**: retrieve domain password policies
- **SMB Signing Detection**: identify relay attack opportunities
- **Multi-Protocol Support**: SMB, LDAP, MSSQL, RDP, SSH, FTP, WinRM
- Pre-configured context menu actions for quick enumeration

#### Theme System
Multiple built-in themes for comfortable extended use:
- **Default** - Classic appearance
- **Dark** - Dark mode for low-light environments
- **Light** - Clean, light interface
- **Hacker** - Classic green-on-black terminal aesthetic
- **Midnight** - Deep blue theme with accent colors

#### Customizable Fonts
- Configurable font family and size
- Apply your preferred monospace font for tool output

#### Enhanced Brute Force Module
- **Account Lockout Protection**: configurable threshold and delay
- **Safe Mode**: prevent account lockouts during password attacks
- Expanded service support

#### Expanded Tool Actions
- Additional nmap scan profiles (fast TCP, full TCP, fast UDP, top 1000 UDP, full UDP)
- Unicornscan integration for UDP scanning
- NetExec quick-action commands for common enumeration tasks

---

## Requirements

It is recommended to use **Kali Linux** as it already has most tools installed. NinjaArt should also work on other Debian-based systems.

### Kali 2025+:
```bash
sudo apt install python3-sqlalchemy python3-pyqt5 wkhtmltopdf
```

### Core Dependencies
- **nmap** - for adding hosts and scanning
- **hydra** - for the brute force tab
- **nxc** (NetExec) - for the nxc tab and enumeration actions

### Optional Tools
For full functionality with default configuration:
```bash
apt-get install ldap-utils rwho rsh-client x11-apps finger
```

---

## Installation

```bash
cd /usr/share/
git clone https://github.com/bushidokarat3/ninjaArt.git

# Place the "ninjaart" launcher in /usr/bin/ and make it executable
sudo cp ninjaArt/ninjaart /usr/bin/
sudo chmod +x /usr/bin/ninjaart

# Launch the application
ninjaart
```

### Running from Source
```bash
cd ninjaArt
python3 ninjaart.py
```

### Command Line Options
```bash
ninjaart -t <target>     # Auto-launch staged nmap against target IP/range
ninjaart -f <file.xml>   # Import nmap XML and start automated enumeration
```

---

## Configuration

NinjaArt uses `ninjaart.conf` for all settings. On first run, default settings are automatically created.

### Key Settings Groups
- **GeneralSettings** - Terminal, themes, fonts, scheduler options
- **BruteSettings** - Wordlists, lockout protection, service configurations
- **StagedNmapSettings** - Port ranges for each scanning stage
- **ToolSettings** - Paths to external tools (nmap, hydra, nxc, etc.)
- **HostActions** - Right-click actions for hosts
- **PortActions** - Right-click actions for services/ports
- **SchedulerSettings** - Automated scanning configurations

---

## Credits

- Original nmap XML parsing engine based on code by yunshu, modified by ketchup
- ms08-067_check script by Bernardo Damele A.G.
- Logo design by Diana Guardão ([Behance](https://www.behance.net/didoquinhasfaaa))
- Built upon the work of the SECFORCE team and all contributors to the original SPARTA project

NinjaArt relies on many excellent open source tools including nmap, hydra, NetExec, Python, PyQt5, SQLAlchemy, and others.

---

## License

GNU General Public License v3.0

---

Happy hacking!
