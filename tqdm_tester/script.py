from tqdm import tqdm
from time import sleep
import logging
from tqdm.contrib.logging import logging_redirect_tqdm

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

NUM = 1000

with logging_redirect_tqdm(), tqdm(total=NUM, desc="I am a progress bar") as pbar:
    for i in range(NUM):
        sleep(0.005)
        diplayed = pbar.update(1)
        if diplayed:
            logger.info("hey there %s, %s", i, f"{pbar}")
