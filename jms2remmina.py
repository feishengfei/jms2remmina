#!/usr/bin/env python3

# Copyright (c) 2025 Xiang Zhou <felix@sietium.com>
# Author: Xiang Zhou <felix@sietium.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import base64
import json
import os
import sys
import re
import tempfile
import shutil
import os
import configparser

DEFAULT_REMMINA_PATH='/usr/share/jms2remmina.remmina'

def parse_jms_uri(jms_uri):
    if not jms_uri.startswith("jms://"):
        raise ValueError("Invalid JMS URI, must start with 'jms://'")
    
    encoded_data = jms_uri[len("jms://"):]
    
    try:
        decoded_data = base64.b64decode(encoded_data).decode("utf-8")
        return json.loads(decoded_data)
    except Exception as e:
        raise ValueError(f"Failed to decode JMS URI content: {e}")

def parse_rdp_config(config):
    address_match = re.search(r"full address:s:(\S+)", config)
    username_match = re.search(r"username:s:(\S+)", config)
    
    if not address_match or not username_match:
        raise ValueError("Invalid RDP config, missing required fields.")

    address = address_match.group(1)
    username = username_match.group(1)
    return address, username

def gen_temp_remmina(address, username):
    temp_remmina = ''

    config = configparser.ConfigParser()
    config.read(DEFAULT_REMMINA_PATH)

    username_abbrev = username.split('|')[0] if '|' in username else username

    remmina_section = config['remmina']
    remmina_section['username'] = username
    remmina_section['server'] = address
    remmina_section['name'] = f'{username_abbrev}@{address}'

    # Create a temporary file to write the modified content
    with tempfile.NamedTemporaryFile(delete=False, suffix='.remmina') as temp_file:
        temp_file_path = temp_file.name  # Temporary file path

        # Write the modified content to the temporary file
        with open(temp_file_path, 'w') as configfile:
            config.write(configfile)

        temp_remmina = temp_file_path

    return temp_remmina 

def launch_remmina(address, username, config):
    temp_remmina = gen_temp_remmina(address, username)
    remmina_command = f"remmina -c {temp_remmina}"

    print(f"Executing: {remmina_command}")
    os.system(remmina_command)

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 jms_client.py '<jms://URI>'")
        sys.exit(1)
    
    jms_uri = sys.argv[1]
    
    try:
        decoded_json = parse_jms_uri(jms_uri)
        print(f"Decoded JSON: {decoded_json}")
        
        config = decoded_json.get("config", "")
        address, username = parse_rdp_config(config)
        
        launch_remmina(address, username, config)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
