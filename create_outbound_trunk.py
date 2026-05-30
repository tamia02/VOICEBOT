import asyncio
import os
from dotenv import load_dotenv
from livekit import api

load_dotenv(".env")

async def main():
    lkapi = api.LiveKitAPI()
    
    address = os.getenv("VOBIZ_SIP_DOMAIN", "")
    username = os.getenv("VOBIZ_USERNAME", "")
    password = os.getenv("VOBIZ_PASSWORD", "")
    number = os.getenv("VOBIZ_OUTBOUND_NUMBER", "")

    if password == "your_password" or not password:
        print("Error: Please set your actual VoBiz password in the VOBIZ_PASSWORD variable in your .env file first!")
        await lkapi.aclose()
        return

    # Strip sip: or sips: prefixes if present, as LiveKit expects just the hostname/IP
    clean_address = address.replace("sip:", "").replace("sips:", "")

    print("Creating Outbound SIP Trunk on LiveKit...")
    print(f"  SIP Domain: {clean_address} (raw: {address})")
    print(f"  Username:   {username}")
    print(f"  Number:     {number}")

    try:
        # Create request using modern non-deprecated method
        req = api.CreateSIPOutboundTrunkRequest(
            trunk=api.SIPOutboundTrunkInfo(
                name="vobiz-outbound",
                address=clean_address,
                auth_username=username,
                auth_password=password,
                numbers=[number] if number else [],
            )
        )
        
        trunk = await lkapi.sip.create_outbound_trunk(req)
        trunk_id = trunk.sip_trunk_id
        print(f"\n[OK] Outbound SIP Trunk created successfully!")
        print(f"Trunk ID: {trunk_id}")
        print("-" * 50)
        print("Action required:")
        print(f"1. Open your .env file and set:")
        print(f"   SIP_TRUNK_ID={trunk_id}")
        print(f"   OUTBOUND_TRUNK_ID={trunk_id}")
        print(f"2. Open config.json and set:")
        print(f"   \"sip_trunk_id\": \"{trunk_id}\"")
        
    except Exception as e:
        print(f"\n[ERROR] Failed to create outbound trunk: {e}")
    finally:
        await lkapi.aclose()

if __name__ == "__main__":
    asyncio.run(main())
