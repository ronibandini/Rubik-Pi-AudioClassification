# RUBIK Pi 3 Window Break Detection
# Roni Bandini @RoniBandini
# November 2025
# MIT License

import subprocess
import time
import json
import re
from periphery import GPIO



banner = """
██╗    ██╗██╗███╗    ██╗██████╗  ██████╗ ██╗    ██╗    ██████╗ ██████╗ ███████╗ █████╗ ██╗  ██╗
██║    ██║██║████╗  ██║██╔══██╗██╔═══██╗██║    ██║    ██╔══██╗██╔══██╗██╔════╝██╔══██╗██║ ██╔╝
██║ █╗ ██║██║██╔██╗ ██║██║  ██║██║  ██║██║ █╗ ██║    ██████╔╝██████╔╝█████╗  ███████║█████╔╝ 
██║███╗██║██║██║╚██╗██║██║  ██║██║  ██║██║███╗██║    ██╔══██╗██╔══██╗██╔══╝  ██╔══██║██╔═██╗ 
╚███╔███╔╝██║██║ ╚████║██████╔╝╚██████╔╝╚███╔███╔╝    ██████╔╝██║  ██║███████╗██║  ██║██║  ██╗
 ╚══╝╚══╝ ╚═╝╚═╝  ╚═══╝╚═════╝  ╚═════╝  ╚══╝╚══╝     ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝
"""

print(banner)

print("Roni Bandini, Nov 2025, Argentina, @RoniBandini")
print("Machine Learning with Edge Impulse")
print("Monitoring for glass breaking sounds...")
print("Stop with CTRL-C")
print("")

# Settings
CONFIDENCE_THRESHOLD = 75.0
GPIO_PIN = 571
LED_ON_TIME = 3
output_file = open('output.txt', 'w')


# Initialize GPIO
try:
    out_gpio = GPIO(GPIO_PIN, "out")
    print(f"✓ GPIO pin {GPIO_PIN} initialized as output.")
except Exception as e:
    out_gpio = None
    print(f"⚠️ GPIO init error {GPIO_PIN}: {e}")

print("")

RUNNER_PATH = "/home/ubuntu/edge-impulse-tools/node/bin/edge-impulse-linux-runner"
subprocess.Popen([RUNNER_PATH], stdout=output_file)

try:
    with open("output.txt", "r") as f:
        lines_seen = set()
        while True:
            line = f.readline()
            if not line:
                time.sleep(1)
                continue
            
            if "[]" in line:
                continue
            
            # classifyRes 53ms. {'glass_break': 0.91, 'noise': 0.09}
            match = re.search(r"classifyRes \d+ms\. ({.*})", line)
            if match and line not in lines_seen:
                raw = match.group(1)
                
                # Fix formatting quirks
                raw_fixed = raw.replace("'", '"')
                raw_fixed = re.sub(r'([a-zA-Z0-9_]+):', r'"\1":', raw_fixed)
                
                try:
                    classifications = json.loads(raw_fixed)
                    
                    # Print all classifications
                    print("\n--- Inference ---")
                    for label, score in classifications.items():
                        pct = score * 100.0
                        print(f" {label}: {pct:.2f}%")
                    
                    # Only check for glass label
                    if 'glass' in classifications:
                        glass_confidence = classifications['glass'] * 100.0
                        
                        # Check if glass passes threshold
                        if glass_confidence >= CONFIDENCE_THRESHOLD:
                            print(f"\n🚨 WINDOW BREAK SOUND DETECTED! (Confidence: {glass_confidence:.2f}%)")
                            
                            # Trigger GPIO
                            if out_gpio:
                                try:
                                    out_gpio.write(True)
                                    print(f"🟢 Alert LED activated on GPIO {GPIO_PIN}")
                                    time.sleep(LED_ON_TIME)
                                    out_gpio.write(False)
                                    print(f"🔴 Alert LED deactivated\n")
                                except Exception as e:
                                    print(f"GPIO error: {e}")
                            else:
                                print("⚠️ GPIO not initialized\n")
                
                except json.JSONDecodeError as e:
                    print("JSON decode error:", e)
                    print("Attempted to parse:", raw_fixed)
                
                lines_seen.add(line)

except KeyboardInterrupt:
    print("\n\nStopping window break detection (CTRL-C).")
except Exception as e:
    print(f"\nError: {e}")
finally:
    try:
        if out_gpio is not None:
            out_gpio.write(False)
            out_gpio.close()
            print(f"GPIO {GPIO_PIN} closed.")
    except Exception:
        pass
    output_file.close()
    print("Execution ended.")