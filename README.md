# Klyro

> A lightweight Linux screenshot and screen recording tool built with Python.

Klyro is a Linux desktop utility designed to make taking screenshots and recording the screen simple and accessible from a single application.

The project is built with Python and integrates with Linux desktop technologies for capturing and managing screen content.

---

##  Features

*  Screenshot capture
*  Screen recording
*  Designed for Linux
*  Desktop GUI
*  Lightweight Python-based application
*  Simple and focused interface
*  Built with Linux multimedia tools

---

##  Tech Stack

| Technology | Purpose                           |
| ---------- | --------------------------------- |
| Python     | Core application logic            |
| GTK        | Desktop graphical interface       |
| FFmpeg     | Media processing / recording      |
| PipeWire   | Linux multimedia / screen capture |
| Linux      | Target platform                   |

---

##  Requirements

Before installing Klyro, make sure your system has:

* Linux
* Python 3
* GTK
* FFmpeg
* PipeWire
* Python dependencies listed in `requirements.txt`

> Package names may vary depending on your Linux distribution.

---

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/vanshsainiprime/Klyro.git
```

### 2. Enter the project directory

```bash
cd Klyro
```

### 3. Create a virtual environment

```bash
python3 -m venv .venv
```

### 4. Activate the virtual environment

```bash
source .venv/bin/activate
```

### 5. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 6. Run Klyro

```bash
python3 run.py
```

---

## 🖥️ Usage

After launching Klyro, use the application's interface to access its available screenshot and screen-recording functionality.

```bash
python3 run.py
```

---

##  Project Structure

```text
Klyro/
│
├── app/
│   ├── ...
│   └── ...
│
├── run.py
├── requirements.txt
├── CONTRIBUTING.md
├── LICENSE
└── README.md
```

> The project structure may change as Klyro develops.

---

##  How Klyro Works

At a high level, Klyro connects a desktop interface with Linux's multimedia stack.

```text
┌─────────────────────┐
│       Klyro         │
│     GTK Interface   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   Capture Control   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│      PipeWire       │
│  Linux Media Stack  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│       FFmpeg        │
│   Media Processing  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│     Output File     │
└─────────────────────┘
```

---

## 🐧 Linux Compatibility

Klyro is designed primarily for Linux desktop environments.

Its functionality may depend on:

* Desktop environment
* Display server
* Wayland/X11 configuration
* PipeWire availability
* FFmpeg installation
* Permissions and portal configuration

For this reason, behavior can vary between Linux distributions and desktop environments.

---

##  Development

Clone the repository:

```bash
git clone https://github.com/vanshsainiprime/Klyro.git
cd Klyro
```

Create a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python3 run.py
```

---

## 🤝 Contributing

Contributions are welcome.

If you want to contribute:

1. Fork the repository.
2. Create a new branch.

```bash
git checkout -b feature/your-feature
```

3. Make your changes.
4. Test your changes.
5. Commit your work.

```bash
git add .
git commit -m "Add your feature"
```

6. Push your branch.

```bash
git push origin feature/your-feature
```

7. Open a Pull Request.

Please read [`CONTRIBUTING.md`](CONTRIBUTING.md) before contributing.

---

## 🐛 Bug Reports

If you find a bug, please open an issue and include:

* Linux distribution
* Desktop environment
* Wayland or X11
* Python version
* FFmpeg version
* PipeWire version
* Steps to reproduce the issue
* Error messages or logs
* Screenshots, if relevant

Example:

```text
OS: Kali Linux
Desktop: XFCE
Display Server: X11
Python: 3.x
FFmpeg: x.x
PipeWire: x.x
```

---

##  Security

If you discover a security-related issue, please avoid publicly exposing sensitive details in an issue until the problem has been investigated.

---

##  License

Klyro is distributed under the license included in this repository.

See [`LICENSE`](LICENSE) for the complete license text.

---

##  Author

**Vansh Saini**

GitHub: [@vanshsainiprime](https://github.com/vanshsainiprime)

---

## ⭐ Support

If you find Klyro useful, consider giving the repository a ⭐ on GitHub.

[![GitHub](https://img.shields.io/badge/GitHub-Klyro-black?logo=github)](https://github.com/vanshsainiprime/Klyro)

---

##  Repository

https://github.com/vanshsainiprime/Klyro
