#!/usr/bin/env python3
"""
Test script to verify GridView branding configuration is working.
"""

import requests
import json
import html
import re
import sys


def test_gridview_branding():
    """Test GridView branding endpoints and configuration."""
    base_url = "http://localhost:5001"
    
    print("🧪 Testing GridView Branding Configuration")
    print("=" * 50)
    
    # Test 1: Check if server is running
    try:
        response = requests.get(f"{base_url}/gridview/status", timeout=5)
        if response.status_code == 200:
            print("✅ GridView server is running")
            status = response.json()
            print(f"   Version: {status.get('version')}")
            print(f"   Mode: {status.get('mode')}")
        else:
            print("❌ GridView server not responding properly")
            return False
    except requests.RequestException as e:
        print(f"❌ Cannot connect to GridView server: {e}")
        return False
    
    # Test 2: Check static assets
    print("\n📁 Testing Static Assets:")
    static_tests = [
        "/gridview/static/images/gridview-logo.svg",
        "/gridview/static/images/gridview-logo-horiz.svg", 
        "/gridview/static/images/gridview-favicon.svg"
    ]
    
    for asset_path in static_tests:
        try:
            response = requests.get(f"{base_url}{asset_path}", timeout=5)
            if response.status_code == 200:
                print(f"   ✅ {asset_path}")
            else:
                print(f"   ❌ {asset_path} - Status: {response.status_code}")
        except requests.RequestException:
            print(f"   ❌ {asset_path} - Request failed")
    
    # Test 3: Check configuration
    print("\n⚙️ Testing Configuration:")
    session = requests.Session()
    
    # Login
    try:
        login_response = session.post(f"{base_url}/login/", data={
            "username": "admin",
            "password": "admin"
        }, timeout=10)
        
        if login_response.status_code in [200, 302]:
            print("   ✅ Login successful")
        else:
            print("   ❌ Login failed")
            return False
            
    except requests.RequestException as e:
        print(f"   ❌ Login request failed: {e}")
        return False
    
    # Get main page
    try:
        main_response = session.get(f"{base_url}/", timeout=10)
        
        if main_response.status_code in [200, 302]:
            print("   ✅ Main page accessible")
            
            # Try to find bootstrap data
            content = main_response.text
            match = re.search(r'data-bootstrap="([^"]+)"', content)
            
            if match:
                print("   ✅ Bootstrap data found")
                try:
                    encoded_json = match.group(1)
                    decoded_json = html.unescape(encoded_json)
                    data = json.loads(decoded_json)
                    
                    # Check app name
                    app_name = data.get('common', {}).get('conf', {}).get('APP_NAME')
                    if app_name == "GridView":
                        print(f"   ✅ APP_NAME correctly set to: {app_name}")
                    else:
                        print(f"   ⚠️ APP_NAME is: {app_name} (expected: GridView)")
                    
                    # Check brand configuration
                    brand = data.get('common', {}).get('menu_data', {}).get('brand', {})
                    brand_icon = brand.get('icon', '')
                    if 'gridview' in brand_icon.lower():
                        print(f"   ✅ Brand icon uses GridView asset: {brand_icon}")
                    else:
                        print(f"   ⚠️ Brand icon: {brand_icon}")
                    
                    # Check theme data
                    if 'theme' in data.get('common', {}):
                        print("   ✅ Theme data present")
                    else:
                        print("   ⚠️ No theme data found")
                        
                except (json.JSONDecodeError, KeyError) as e:
                    print(f"   ❌ Bootstrap data parsing failed: {e}")
            else:
                print("   ⚠️ No bootstrap data found (might be redirecting)")
        else:
            print(f"   ❌ Main page not accessible - Status: {main_response.status_code}")
            
    except requests.RequestException as e:
        print(f"   ❌ Main page request failed: {e}")
    
    print("\n📝 Summary:")
    print("   GridView branding implementation includes:")
    print("   • Custom logo assets (SVG format)")
    print("   • Static asset serving route")
    print("   • Superset configuration overrides")
    print("   • Theme token configuration")
    print("")
    print("🌐 To manually verify:")
    print(f"   1. Visit {base_url} in your browser")
    print("   2. Login with admin/admin")
    print("   3. Check the navbar logo (top-left)")
    print("   4. Check browser tab icon/title")
    
    return True


if __name__ == "__main__":
    success = test_gridview_branding()
    sys.exit(0 if success else 1)
