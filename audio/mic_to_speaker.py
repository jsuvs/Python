#wire microphone input to speaker output
from audiolib import Microphone
from audiolib import Speaker
import asyncio

async def main():
    sample_rate=16000
    block_size=512
    speaker = Speaker(sample_rate, block_size)
    microphone = Microphone(sample_rate, block_size)
    async for d in microphone.get_data():
        speaker.play(d)

asyncio.run(main())