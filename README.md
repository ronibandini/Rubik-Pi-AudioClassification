![PXL_20251117_143455765 PORTRAIT](https://github.com/user-attachments/assets/a655760a-35e4-47f3-8b7a-c2231b3e0617)

# 🎙️🪟 Rubik Pi Audio Classification

**Real-time glass-break detection with Machine Learning, Edge Impulse, and the Qualcomm-powered RUBIK Pi 3.**

This project demonstrates how to deploy an **audio classification model** on a **Thundercomm RUBIK Pi 3** and use the classification result to trigger physical hardware through GPIO.

A USB microphone continuously captures ambient sound. An **Edge Impulse** model classifies the audio as normal street noise or breaking glass. When the confidence for the `glass` class exceeds a configured threshold, a GPIO output is activated.

The example implementation lights an LED, but the same signal could trigger a siren, relay, notification service, recording system, or other automation.

> ⚠️ This is an experimental Machine Learning project. It should not be treated as a certified alarm or security system.

---

# ✨ Features

* 🎙️ Real-time audio classification
* 🧠 Machine Learning with Edge Impulse
* 🪟 Glass-break detection
* ⚡ Local inference on RUBIK Pi 3
* 🐉 Qualcomm Dragonwing QCS6490 platform
* 🐍 Python result parser
* 🚨 Configurable confidence threshold
* 💡 GPIO response when glass is detected
* ⏱️ Configurable output activation time
* 🎤 Standard USB microphone input
* 🐧 Canonical Ubuntu environment
* 📜 MIT licensed

---

# 🎯 Objective

The original experiment was motivated by detecting the characteristic sound of a car window being broken.

Instead of continuously monitoring video footage, a dedicated edge device can listen for a particular acoustic event:

```text
Street sound
      ↓
 Microphone
      ↓
Audio classifier
      ↓
Is it breaking glass?
      ↓
    YES
      ↓
GPIO alert
```

The same architecture can be adapted to many other acoustic-event detection tasks.

---

# ⚙️ Architecture

```text
┌───────────────────────────┐
│      Ambient Sound        │
│                           │
│  traffic / voices / glass │
└─────────────┬─────────────┘
              │
              ▼
      ┌──────────────┐
      │ USB Microphone│
      └───────┬──────┘
              │
              ▼
┌───────────────────────────┐
│       RUBIK Pi 3          │
│                           │
│ Edge Impulse Linux Runner │
│                           │
│     Audio inference       │
└─────────────┬─────────────┘
              │
              │ classifyRes
              ▼
┌───────────────────────────┐
│        glass.py           │
│                           │
│ • Parse probabilities     │
│ • Read `glass` confidence │
│ • Apply 75% threshold     │
└─────────────┬─────────────┘
              │
              │ GPIO
              ▼
        ┌───────────┐
        │    LED    │
        │  / Alarm  │
        └───────────┘
```

---

# 🧠 Machine Learning

The model is built and deployed with **Edge Impulse**.

Two main sound categories are used:

```text
street
glass
```

The project trains an audio classifier using recordings of:

* normal street noise
* breaking glass

The resulting model is deployed to the RUBIK Pi through the Edge Impulse Linux runner.

Example inference output:

```text
classifyRes 2ms. { street: 0.9999, glass: 0.0001 }
classifyRes 2ms. { street: 0.8629, glass: 0.1371 }
```

The Python script continuously parses these results.

---

# 🌐 Edge Impulse project

The Machine Learning project is publicly available in Edge Impulse Studio:

**[Open the public Edge Impulse project](https://studio.edgeimpulse.com/studio/828677)**

The Edge Impulse project can be used to inspect the dataset, impulse configuration, training process, and deployment options.

---

# 🖥️ RUBIK Pi 3

The project runs on the **Thundercomm RUBIK Pi 3**, a Raspberry Pi-style edge-AI development platform based on the Qualcomm Dragonwing QCS6490.

Relevant specifications include:

| Specification  | RUBIK Pi 3                     |
| -------------- | ------------------------------ |
| Platform       | Qualcomm Dragonwing QCS6490    |
| CPU            | Kryo / Cortex-A78 + Cortex-A55 |
| GPU            | Adreno 643                     |
| AI performance | Up to 12 TOPS                  |
| RAM            | 8 GB LPDDR4x                   |
| Storage        | 128 GB UFS 2.2                 |
| Network        | Gigabit Ethernet, Wi-Fi        |
| GPIO           | 40-pin header                  |
| Audio          | USB / 3.5 mm interfaces        |

Official documentation:

**[RUBIK Pi 3 Documentation](https://www.thundercomm.com/rubik-pi-3/en/docs/)**

> ℹ️ The original tutorial instructs Edge Impulse users to select the **unoptimized** Linux deployment option. The RUBIK Pi hardware includes Qualcomm AI acceleration capabilities, but this particular example should not be assumed to use the NPU unless an optimized deployment is explicitly selected.

---

# 🧰 Hardware

| Component                      | Purpose                         |
| ------------------------------ | ------------------------------- |
| **Thundercomm RUBIK Pi 3**     | Edge inference and GPIO control |
| **RUBIK Pi active cooler**     | Thermal management              |
| **12 V / 3 A USB-C PD supply** | Power                           |
| **USB microphone**             | Audio capture                   |
| **LED**                        | Detection indicator             |
| **2 jumper wires**             | LED connection                  |
| Ethernet cable                 | Initial networking / SSH        |

A microphone connected to the 3.5 mm audio interface can also be used if appropriately configured.

---

# 🔌 GPIO

The reference build connects an LED between:

```text
RUBIK Pi GPIO header pin 13
          │
          ▼
         LED
          │
          ▼
Pin 6 / GND
```

The RUBIK Pi Linux GPIO mapping used by the Python program is:

```python
GPIO_PIN = 571
```

This corresponds to **header pin 13** in the project configuration.

---

# 🐍 `glass.py`

The repository contains a single Python application:

```text
glass.py
```

It performs four main tasks:

```text
Start Edge Impulse runner
        ↓
Read inference output
        ↓
Extract classification scores
        ↓
Trigger GPIO when glass is detected
```

---

# 🎚️ Detection threshold

The current source defines:

```python
CONFIDENCE_THRESHOLD = 75.0
```

This means the GPIO alert is activated when:

```text
glass confidence ≥ 75%
```

For example:

```text
street: 18.00%
glass: 82.00%
```

results in:

```text
🚨 WINDOW BREAK SOUND DETECTED!
```

---

# 💡 GPIO response

When detection exceeds the threshold, the script activates the output:

```python
out_gpio.write(True)
```

The LED remains on for:

```python
LED_ON_TIME = 3
```

seconds.

Then the output returns low:

```python
out_gpio.write(False)
```

Conceptually:

```text
Glass confidence
       │
       │ ≥ 75%
       ▼
GPIO HIGH
       │
       │ 3 seconds
       ▼
GPIO LOW
```

---

# 🧾 Parsing Edge Impulse output

`glass.py` launches the Edge Impulse runner directly:

```python
RUNNER_PATH = "/home/ubuntu/edge-impulse-tools/node/bin/edge-impulse-linux-runner"
```

and writes its output to:

```text
output.txt
```

The script monitors the file and searches for lines matching:

```text
classifyRes ... { ... }
```

It then converts the classification result into JSON-compatible data and reads the individual scores.

For example:

```text
classifyRes 53ms. {'glass': 0.91, 'street': 0.09}
```

becomes approximately:

```json
{
  "glass": 0.91,
  "street": 0.09
}
```

The `glass` value is converted to a percentage before being compared with the configured threshold.

---

# 🚀 Installation

## 1. Clone the repository

```bash
git clone https://github.com/ronibandini/Rubik-Pi-AudioClassification.git
cd Rubik-Pi-AudioClassification
```

Repository structure:

```text
Rubik-Pi-AudioClassification/
├── LICENSE
├── README.md
└── glass.py
```

---

# 🐧 Operating system

The project tutorial assumes the RUBIK Pi is running:

**Canonical Ubuntu for Qualcomm platforms**

Connect:

* power supply
* USB microphone
* Ethernet

Boot the RUBIK Pi and obtain its IP address from your router or local console.

Then connect through SSH:

```bash
ssh ubuntu@RUBIK_PI_IP
```

---

# ⚡ Install Edge Impulse

Update the system:

```bash
sudo apt update
```

Download the Qualcomm Linux setup script:

```bash
wget https://cdn.edgeimpulse.com/firmware/linux/setup-edge-impulse-qc-linux.sh
```

Install the SELinux utility required by the setup:

```bash
sudo apt install selinux-utils
```

Then:

```bash
source ~/.profile
chmod +x setup-edge-impulse-qc-linux.sh
./setup-edge-impulse-qc-linux.sh
```

Official Edge Impulse documentation:

**[Audio Classification and GPIO Response — RUBIK Pi 3](https://docs.edgeimpulse.com/projects/expert-network/audio-classification-gpio-rubik-pi)**

---

# 🎙️ Configure the microphone

Connect the USB microphone and run:

```bash
alsamixer
```

Press:

```text
F6
```

to select the USB input.

Increase the recording level if required using the arrow keys.

---

# 🐍 Install Python GPIO support

Install:

```bash
sudo apt install python3-pip
sudo apt install python3-periphery
```

The script imports:

```python
from periphery import GPIO
```

---

# 🔐 Configure GPIO permissions

Create a GPIO user group:

```bash
sudo groupadd -f gpio
sudo usermod -aG gpio ubuntu
```

Edit:

```bash
sudo nano /etc/udev/rules.d/99-gpio.rules
```

Add rules granting the `gpio` group access to GPIO devices.

After saving the file:

```bash
sudo udevadm control --reload-rules
sudo udevadm trigger
sudo reboot
```

Reconnect to the board after reboot.

---

# 🧪 Test Edge Impulse inference

Run:

```bash
edge-impulse-linux-runner --clean
```

Log in with your Edge Impulse account.

Select:

1. the audio-classification project
2. the unoptimized model
3. the USB microphone

You should begin seeing output similar to:

```text
classifyRes 2ms. { street: 0.9999, glass: 0.0001 }
```

Stop the runner with:

```text
CTRL-C
```

---

# 🚨 Run the detector

Start:

```bash
python3 glass.py
```

The application displays:

```text
Machine Learning with Edge Impulse
Monitoring for glass breaking sounds...
Stop with CTRL-C
```

When a classification arrives, the scores are printed:

```text
--- Inference ---
 street: 4.23%
 glass: 95.77%
```

If the confidence exceeds 75%:

```text
🚨 WINDOW BREAK SOUND DETECTED!
🟢 Alert LED activated on GPIO 571
```

Three seconds later:

```text
🔴 Alert LED deactivated
```

Stop the program with:

```text
CTRL-C
```

The script closes the GPIO cleanly before terminating.

---

# 🔧 Configuration

The main configuration values are at the beginning of `glass.py`:

```python
CONFIDENCE_THRESHOLD = 75.0
GPIO_PIN = 571
LED_ON_TIME = 3
```

| Variable               | Default | Purpose                    |
| ---------------------- | ------: | -------------------------- |
| `CONFIDENCE_THRESHOLD` |  `75.0` | Minimum glass probability  |
| `GPIO_PIN`             |   `571` | Linux GPIO number          |
| `LED_ON_TIME`          |     `3` | Output duration in seconds |

---

# 🔬 Ideas for extending the project

1. **📲 Send notifications** — call a webhook when glass is detected to trigger WhatsApp, email, Telegram, n8n, Home Assistant, or another automation system.

2. **📹 Trigger video recording** — connect the detector to a security camera and preserve footage from immediately before and after the acoustic event.

3. **🎧 Add more sound classes** — extend the model to distinguish breaking glass from alarms, impacts, car horns, shouting, or other urban acoustic events.

---

# 📰 External references

This project is documented and indexed outside GitHub on both **Edge Impulse** and the official **RUBIK Pi / Thundercomm documentation**.

---

# ⚡ Edge Impulse

## Expert Network project

**[Audio Classification and GPIO Response — RUBIK Pi 3](https://docs.edgeimpulse.com/projects/expert-network/audio-classification-gpio-rubik-pi)**

Edge Impulse hosts the complete project in its official **Expert Network** documentation.

The page covers:

* project motivation
* RUBIK Pi 3 specifications
* hardware setup
* Edge Impulse installation
* audio dataset
* USB microphone setup
* GPIO configuration
* Python parser
* alert output
* possible webhook integration

Most importantly, the Edge Impulse page explicitly references this repository:

**[github.com/ronibandini/Rubik-Pi-AudioClassification](https://github.com/ronibandini/Rubik-Pi-AudioClassification)**

---

## Edge Impulse project directory

**[Edge Impulse Expert Network — Project List](https://docs.edgeimpulse.com/projects/expert-network/project-list)**

Edge Impulse also lists:

> **Audio Classification and GPIO Response - Rubik Pi 3**

among its **Featured Machine Learning Projects**.

---

## Public Edge Impulse project

**[Rubik Pi Audio Classification — Edge Impulse Studio](https://studio.edgeimpulse.com/studio/828677)**

Public Edge Impulse Studio project associated with the audio-classification experiment.

---

# 🐉 Thundercomm / RUBIK Pi

## Official RUBIK Pi documentation

**[Audio Classification and GPIO Response — RUBIK Pi 3](https://www.thundercomm.com/rubik-pi-3/en/docs/audio-classification-and-gpio-response-rubik-pi-3/)**

Thundercomm includes the project directly in the official **RUBIK Pi 3 documentation**.

The page identifies:

**Created By: Roni Bandini**

and explicitly links to:

* the public Edge Impulse project
* this GitHub repository

It documents the complete workflow from hardware setup through audio inference and GPIO activation.

---

## RUBIK Pi AI & Machine Learning index

**[RUBIK Pi — AI & Machine Learning](https://www.thundercomm.com/rubik-pi-3/en/docs/ai-machine-learning/)**

Thundercomm also indexes the project as one of the official RUBIK Pi AI/ML examples alongside other edge-AI applications.

---

# 📚 Useful references

* **[Edge Impulse](https://edgeimpulse.com/)**
* **[Edge Impulse Linux](https://docs.edgeimpulse.com/tools/libraries/sdks/inference/linux)**
* **[RUBIK Pi 3 Documentation](https://www.thundercomm.com/rubik-pi-3/en/docs/)**
* **[RUBIK Pi GitHub](https://github.com/rubikpi-ai)**
* **[python-periphery](https://github.com/vsergeev/python-periphery)**

---

# 🔗 You may also be interested in...

Other projects by **Roni Bandini** involving Edge Impulse, audio classification, and the RUBIK Pi.

## 📈🤖 RUBIK Pi 3 Anomaly Detection

**Anomaly detection on the RUBIK Pi 3 using Edge Impulse and n8n.**

The closest companion project in terms of hardware: it also explores Machine Learning deployment on the Qualcomm-powered RUBIK Pi 3, with n8n handling the higher-level automation workflow.

**[github.com/ronibandini/rubikpi3-anomaly-detection](https://github.com/ronibandini/rubikpi3-anomaly-detection)**

---

## 🗂️🤖 PunchedCards

**Punched-card recognition using computer vision, Edge Impulse, and LattePanda IOTA.**

Another Edge Impulse project demonstrating how local inference results can be consumed by a small Python application running on Linux edge hardware.

**[github.com/ronibandini/PunchedCards](https://github.com/ronibandini/PunchedCards)**

---

## 🎧🚫 Reggaeton Be Gone

**Machine Learning audio classification with a Raspberry Pi and Edge Impulse.**

Another project centered on real-time audio classification, where the detected sound class triggers a physical/wireless response.

**[github.com/ronibandini/reggaetonBeGone](https://github.com/ronibandini/reggaetonBeGone)**

---

# ⚠️ Detection limitations

Audio classification is probabilistic.

Factors that can affect accuracy include:

* microphone sensitivity
* microphone placement
* distance from the sound source
* room acoustics
* background noise
* audio clipping
* sounds similar to breaking glass
* differences between training and real-world environments

The `75%` confidence threshold is an experimental value, not a guaranteed security threshold.

For a real alarm application, consider combining audio classification with additional evidence such as:

```text
audio detection
      +
camera event
      +
vibration sensor
      +
multiple consecutive classifications
```

---

# 📜 License

Rubik-Pi-AudioClassification is released under the **MIT License**.

See [`LICENSE`](LICENSE) for details.

---

# 👤 Author

**Roni Bandini**

Maker, AI developer, electronic artist and writer.

* 🐙 GitHub: **[@ronibandini](https://github.com/ronibandini)**
* 📸 Instagram: **[@ronibandini](https://www.instagram.com/ronibandini/)**
* 🐦 X: **[@RoniBandini](https://x.com/RoniBandini)**
* ✍️ Medium: **[bandini.medium.com](https://bandini.medium.com/)**
* 🤖 Edge Impulse: **[Expert Network](https://docs.edgeimpulse.com/projects/expert-network/project-list)**

Contributions, forks, alternative sound models, notification integrations, and other RUBIK Pi experiments are welcome.
