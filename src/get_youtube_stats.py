#!/usr/bin/env python

import argparse
import pandas as pd
import yt_dlp

from pathlib import Path


URL = "https://www.youtube.com/c/OpenLifeSci"

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Get stats from YouTube channel into CSV files')
    parser.add_argument('-o', '--out', help="Path to output folder", required=True)
    args = parser.parse_args()

    ydl_opts = {}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(URL, download=False)
        # ydl.sanitize_info makes the info json-serializable
        channel_content = ydl.sanitize_info(info)

    # extract video information
    videos = []
    for v in channel_content['entries'][0]['entries']:
        videos.append({key:v[key] for key in ['title', 'duration', 'view_count', 'average_rating', 'upload_date']})
    
    # output to pandas
    df = pd.DataFrame(videos)
    csv_fp = Path(args.out) / Path('youtube_stats.csv')
    df.to_csv(csv_fp)
