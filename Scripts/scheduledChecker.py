#!/usr/bin/env python
"""check samples periodically
"""

import time
import traceback
import schedule

from makeBackgroundSummary import main as bkgsummaryjob

def job_bkgsummary():
    try:
        bkgsummaryjob()
    except Exception:
        print('*'*60)
        print(traceback.format_exc())
        print('*'*60)

if __name__ == "__main__":
    schedule.every(4).hours.do(job_bkgsummary)

    while True:
        schedule.run_pending()
        time.sleep(1)