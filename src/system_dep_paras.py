"""
Constants defined here must be adjusted depending on the system you run the codes.
The values taken here is proper for system with 96 CPU cores and ~400 GB RAM storage
  when running over full data sets.

Please be aware that full data sets are not provided due to file size limit of GitHub.
We provided the source of data sets on the article.
"""

"""
Minimum and maximum number of workers should be adjusted depending on
    1. the number of cores your CPU has
    2. available RAM storage.

If you found your run terminated without any error messages,
  it's probably due to lack of RAM storage.
Please reduce MIN_WORKERS and MAX_WORKERS in such cases.
"""

MAX_WORKERS = 50
MIN_WORKERS = 10
