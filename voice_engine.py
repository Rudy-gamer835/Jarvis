import asyncio
import os
import tempfile
import uuid

import edge_tts
import pygame

VOICE = "en-US-GuyNeural"

pygame.mixer.init()


async def _generate_speech(text, filename):
    communicate = edge_tts.Communicate(text=text, voice=VOICE)
    await communicate.save(filename)


def speak(text):
    print("JARVIS:", text)

    # Create a unique file every time
    filename = os.path.join(
        tempfile.gettempdir(),
        f"jarvis_{uuid.uuid4().hex}.mp3"
    )

    asyncio.run(_generate_speech(text, filename))

    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.mixer.music.unload()

    try:
        os.remove(filename)
    except PermissionError:
        pass