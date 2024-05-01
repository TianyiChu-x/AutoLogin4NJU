# NJU Campus Network Auto-Login

This Python script automates the process of logging into the Nanjing University campus network. It handles the login page, captures and recognizes captcha using OCR, and submits the user credentials.

## Obtaining the Code

You can get the script either by cloning the repository using Git or by downloading a ZIP file directly from GitHub.

### Cloning with Git

If you have Git installed, you can clone the repository using the following command:

```bash
git clone https://github.com/TianyiChu-x/AutoLogin4NJU.git
```

Navigate to the cloned directory:

```bash
cd AutoLogin4NJU
```

### Downloading as ZIP

If you prefer not to use Git, you can download the script as a ZIP file:

1. Visit the GitHub repository webpage ([`https://github.com/TianyiChu-x/AutoLogin4NJU`](https://github.com/TianyiChu-x/AutoLogin4NJU)).
2. Click the `Code` button and then click `Download ZIP`.
3. Extract the ZIP file on your local machine.

## Prerequisites

### Installing Anaconda

To run this script, you need Python, and using Anaconda is a recommended way to manage Python and packages. Follow these steps to install Anaconda:

1. Download Anaconda from the official [Anaconda website](https://www.anaconda.com/download/success). Choose the installer appropriate for your operating system.
2. Follow the installation instructions on the website to install Anaconda.

### Creating a Virtual Environment

After installing Anaconda, create a virtual environment to isolate your package installations:

```bash
conda create -n nju_login python=3.9
conda activate nju_login
```

### Installing Dependencies

Before you can run this script, you need to ensure that Python is installed on your system along with the following packages:
- Selenium
- PaddleOCR (if using PaddleOCR for captcha recognition)
- PyTesseract
- configparser

With your virtual environment activated, install the necessary Python packages:

```bash
pip install selenium pytesseract configparser paddleocr
```

### Installing PaddlePaddle

If you choose to use PaddleOCR for captcha recognition, you must also install PaddlePaddle. Follow these steps to install PaddlePaddle on Linux:

1. Ensure your Python version is 3.7, 3.8, or 3.9 and pip version is 20.2.2 or higher:
   ```bash
   python -m pip install --upgrade pip
   ```
2. Install PaddlePaddle with pip (choose one based on your need):
   - For CPU only:
     ```bash
     python -m pip install paddlepaddle
     ```
   - For GPU support:
     ```bash
     python -m pip install paddlepaddle-gpu
     ```

   Visit the [official PaddlePaddle installation guide](https://www.paddlepaddle.org.cn/install/quick?docurl=/documentation/docs/zh/install/pip/linux-pip.html) for more detailed information and troubleshooting.

After installing PaddlePaddle, install PaddleOCR:
```
pip install paddleocr
```

## Configuration (config.ini)

Configure the script using the `config.ini` file. Below are detailed explanations for each setting:

### [credentials]
- `username`: Your NJU campus network username.
- `password`: Your NJU campus network password.

### [OCR]
- `engine`: The OCR engine used for captcha recognition. Options are `paddleocr` or `tesseract`.

### [settings]
- `sleep_duration`: The time in seconds to wait between attempts to log in or recover from errors.
- `use_headless`: Set to `true` to run Chrome in headless mode (without a GUI), or `false` to run with a GUI.
- `use_gpu`: Set to `true` to enable GPU acceleration for PaddleOCR (if available), or `false` to use CPU only.

### Example `config.ini` Format

```ini
[credentials]
username = your_username
password = your_password

[OCR]
# paddleocr or tesseract
engine = paddleocr

[settings]
sleep_duration = 10
use_headless = true
use_gpu = false
```

## Usage

To run the script, use the following command:

```bash
python njuLogin.py
```

This script will continuously attempt to log in until successful, handling timeouts and retrying as necessary.

## Logging

Logs are generated to help you diagnose any issues during the login process. By default, logs are saved in `nju_login.log` with a rotation mechanism to avoid excessive file size.

## Captcha Recognition

This script supports both PaddleOCR and PyTesseract for captcha recognition. Ensure you have the correct OCR engine configured in your `config.ini`. GPU support can be enabled for PaddleOCR if available.

## Headless Mode

For a seamless background operation, the script can run Chrome in headless mode. This is controlled by the `use_headless` setting in your configuration file.