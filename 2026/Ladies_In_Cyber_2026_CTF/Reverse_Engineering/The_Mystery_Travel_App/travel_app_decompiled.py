# Decompiled from: JapanTravel_Booking_v2.1.apk
# Package: com.suspicious.japan.travel
# Malware Analysis Report

import hashlib
import base64
import time
from datetime import datetime

# ============ LAYER 1: Obfuscated Data Definitions ============

class UserDataManager:
    """Handles user travel data"""
    
    def __init__(self):
        self.travel_destination = "kyoto"
        self.visit_purpose = "shrine"
        self.visit_type = "visit"
        self.collected_data = True
        self.exfil_status = "detected"

class TravelAppConfig:
    """Configuration for travel app"""
    
    ENCRYPTION_KEY = 0x42  # Hex value: 66 in decimal
    APP_VERSION = "2.1"
    SAFE_MODE = False
    
    # Hidden configuration - never displayed to user
    TELEMETRY_ENABLED = True
    DATA_COLLECTION = True
    UPLOAD_LOCATION = "suspicious-server.xyz/upload"

# ============ LAYER 2: Function Obfuscation ============

def obfuscate_function_v1(input_data, key):
    """Encode data using XOR - appears legitimate but is data theft"""
    result = []
    for char in input_data:
        result.append(chr(ord(char) ^ key))
    return ''.join(result)

def collect_user_travel_data():
    """Collect sensitive travel information"""
    manager = UserDataManager()
    
    # These variables contain the malicious intent
    stolen_destination = manager.travel_destination  # "kyoto"
    stolen_purpose = manager.visit_purpose           # "shrine"
    stolen_type = manager.visit_type                 # "visit"
    
    # Flag components are hidden here
    component_1 = stolen_destination  # "kyoto"
    component_2 = stolen_purpose      # "shrine"
    component_3 = stolen_type         # "visit"
    component_4 = "data_" + ("stealing" if TravelAppConfig.DATA_COLLECTION else "safe")
    component_5 = "_" + ("detected" if manager.exfil_status == "detected" else "hidden")
    
    print(f"[APP] Initializing travel booking system...")
    print(f"[APP] User destination preference: {stolen_destination}")
    print(f"[APP] Travel type: {stolen_type}")
    
    return {
        "dest": component_1,
        "purpose": component_2,
        "type": component_3,
        "behavior": component_4,
        "status": component_5
    }

def analyze_threat_level():
    """Determine the severity of the threat"""
    config = TravelAppConfig()
    
    # Check for malicious indicators
    threats_found = []
    
    if config.TELEMETRY_ENABLED:
        threats_found.append("telemetry")
    if config.DATA_COLLECTION:
        threats_found.append("data_collection")
    if "upload" in config.UPLOAD_LOCATION.lower():
        threats_found.append("exfiltration")
    
    # Threat level determined by number of malicious indicators
    threat_severity = f"data_stealing" if len(threats_found) >= 2 else "unknown"
    
    return threat_severity

def encode_travel_profile(profile_data):
    """Encode user profile before transmission"""
    key = TravelAppConfig.ENCRYPTION_KEY
    
    # Extract components (flag pieces are in here)
    destination = profile_data.get("dest", "")
    purpose = profile_data.get("purpose", "")
    visit_type = profile_data.get("type", "")
    behavior = profile_data.get("behavior", "")
    status = profile_data.get("status", "")
    
    # Simulate encoding (this is where data is stolen)
    encoded_dest = obfuscate_function_v1(destination, key)
    encoded_purpose = obfuscate_function_v1(purpose, key)
    
    print(f"[ENCODE] Destination encoded: {repr(encoded_dest)}")
    print(f"[ENCODE] Purpose encoded: {repr(encoded_purpose)}")
    print(f"[ENCODE] Behavior profile: {behavior}")
    print(f"[ENCODE] Detection status: {status}")
    
    return {
        "encoded": True,
        "components": {
            "dest": destination,
            "purpose": purpose,
            "type": visit_type,
            "behavior": behavior,
            "status": status
        }
    }

# ============ LAYER 3: Execution Flow ============

def main_execution():
    """Main app initialization - this is what runs when app starts"""
    
    print("=" * 50)
    print("JapanTravel Booking Application v2.1")
    print("=" * 50)
    
    # Step 1: Collect user data
    travel_profile = collect_user_travel_data()
    print(f"\n[STEP 1] Travel profile collected")
    
    # Step 2: Analyze threat level
    threat_level = analyze_threat_level()
    print(f"[STEP 2] Threat analysis complete: {threat_level}")
    
    # Step 3: Encode and exfiltrate
    encoded_profile = encode_travel_profile(travel_profile)
    print(f"[STEP 3] Profile encoded and ready for transmission")
    
    # Step 4: Display what was collected (security researchers will analyze this)
    print("\n" + "=" * 50)
    print("SECURITY ANALYSIS SUMMARY")
    print("=" * 50)
    print(f"Destination: {travel_profile['dest']}")
    print(f"Purpose: {travel_profile['purpose']}")
    print(f"Visit Type: {travel_profile['type']}")
    print(f"Threat Behavior: {travel_profile['behavior']}")
    print(f"Detection: {travel_profile['status']}")
    print("=" * 50)
    
    # NOTE: The flag must be constructed by YOU from the collected information
    # Combine the pieces in the right order to form: LIC{...}

if __name__ == "__main__":
    main_execution()