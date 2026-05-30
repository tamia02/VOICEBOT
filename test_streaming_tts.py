import asyncio, base64, os, time, certifi
from dotenv import load_dotenv
load_dotenv(".env")
os.environ["SSL_CERT_FILE"] = certifi.where()
from sarvamai import AsyncSarvamAI
from sarvamai.types import AudioOutput, EventResponse

async def test():
    print("Starting test...")
    client = AsyncSarvamAI(api_subscription_key=os.environ["SARVAM_API_KEY"])
    start = time.time()
    first_chunk = None

    print("Connecting to streaming TTS...")
    async with client.text_to_speech_streaming.connect(model="bulbul:v3") as ws:
        print("Connected! Configuring...")
        await ws.configure(
            target_language_code="hi-IN",
            speaker="kavya",
            pace=1.1,
            min_buffer_size=50,
            output_audio_codec="pcm",
        )
        print("Configured! Converting...")
        await ws.convert("नमस्ते! मैं आपकी कैसे सहायता कर सकती हूं?")
        print("Flushing...")
        await ws.flush()
        print("Reading messages...")
        chunks = 0
        async for msg in ws:
            print("Received message type:", type(msg), "content:", getattr(msg, 'data', msg))
            if isinstance(msg, AudioOutput):
                chunks += 1
                if chunks == 1:
                    first_chunk = time.time()
                    print(f"✅ First chunk arrived in {(first_chunk - start)*1000:.0f}ms")
            elif isinstance(msg, EventResponse):
                if msg.data.event_type == "final":
                    print(f"✅ Stream complete. {chunks} chunks in {(time.time()-start)*1000:.0f}ms total")
                    break
        print("Loop finished! Total chunks:", chunks)

asyncio.run(test())
