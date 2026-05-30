import asyncio
import os
from dotenv import load_dotenv
from livekit import api

load_dotenv(".env")

async def main():
    lkapi = api.LiveKitAPI()
    try:
        inbound = await lkapi.sip.list_sip_inbound_trunk(api.ListSIPInboundTrunkRequest())
        print("Inbound SIP Trunks:")
        for t in inbound.items:
            print(f"  Trunk ID: {t.sip_trunk_id}")
            print(f"    Numbers: {list(t.numbers)}")
            print(f"    Name: {t.name}")
    except Exception as e:
        print(f"Failed: {e}")
    finally:
        await lkapi.aclose()

if __name__ == "__main__":
    asyncio.run(main())
