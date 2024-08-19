import asyncio
from tqdm import tqdm
import enlighten

manager = enlighten.get_manager()
DOWNLOAD_TIME = 5
EXTRACTING_TIME = 10


async def pull_image(image_id: int):
    # download
    for i in tqdm(
        range(DOWNLOAD_TIME), desc=f"downloading {image_id=}", position=1, leave=False
    ):
        await asyncio.sleep(1)

    for i in tqdm(
        range(EXTRACTING_TIME), desc=f"extracting {image_id=}", position=1, leave=False
    ):
        await asyncio.sleep(1)


NUM_IMAGES = 3


async def pull_images():
    for i in tqdm(range(NUM_IMAGES), desc=f"pulling {NUM_IMAGES} images", position=0):
        await pull_image(i)


asyncio.run(pull_images())
