#!/usr/bin/env python
"""check samples periodically
"""

import time
import schedule

from makeBackgroundSummary import main as bkgsummaryjob

if __name__ == "__main__":
    schedule.every(4).hours.do(bkgsummaryjob)

    while True:
        schedule.run_pending()
        time.sleep(1)