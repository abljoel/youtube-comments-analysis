"""Data Collection Module"""
import logging
import os
from dotenv import load_dotenv
import pandas as pd
import googleapiclient.errors
import googleapiclient.discovery
import click


logging.basicConfig(level=logging.INFO)
load_dotenv(".env")

try:
    YOUTUBE_API_KEY = os.environ["YOUTUBE_API_KEY"]
except:
    raise Exception("Create an .env file on the project root with the YOUTUBE_API_KEY")


def fetch_youtube_comments(target, video, results, service, version, key):
    """Returns raw comments from Youtube video with Youtube API"""
    youtube = googleapiclient.discovery.build(service, version, developerKey=key)

    request = youtube.commentThreads().list(
        part=target, videoId=video, maxResults=results
    )

    response = request.execute()
    comments = []
    while response:
        for item in response["items"]:
            comment = item["snippet"]["topLevelComment"]["snippet"]
            comments.append(
                [
                    comment["authorDisplayName"],
                    comment["publishedAt"],
                    comment["updatedAt"],
                    comment["likeCount"],
                    comment["textDisplay"],
                ]
            )
        # Check if there are more comments and continue iterating
        if "nextPageToken" in response:
            response = (
                youtube.commentThreads()
                .list(
                    part=target,
                    videoId=video,
                    textFormat="plainText",
                    pageToken=response["nextPageToken"],
                )
                .execute()
            )
        else:
            break

    return comments


def fetch_batch_data_from_video(vid, limit=3000):
    """Returns a dataframe of Youtube data"""
    api_service_name = "youtube"
    api_version = "v3"
    api_key = YOUTUBE_API_KEY
    col_names = ["author", "published_at", "updated_at", "likes", "text"]

    try:
        ytb_df = pd.DataFrame(
            fetch_youtube_comments(
                "snippet", vid, limit, api_service_name, api_version, api_key
            ),
            columns=col_names,
        )
        logging.info("Successfully fetched YouTube comments data.")
    except googleapiclient.errors.HttpError as e:
        logging.error(
            "Error %s occurred while fetching data:\n%s", e.resp.status, e.content
        )
        ytb_df = pd.DataFrame(columns=col_names)

    return ytb_df


@click.command()
@click.option(
    "--video_id",
    type=str,
    help="YouTube video ID for comments extraction",
    required=True,
)
@click.option(
    "--output_file",
    type=str,
    help="Output file path for storing comments data",
    required=True,
)
def main(video_id, output_file):
    """
    Collect YouTube comments data.

    Parameters:
    - video_id (str): YouTube video ID for comments extraction.
    - output_file (str): Output file path for storing comments data.
    """
    try:
        ytb_df = fetch_batch_data_from_video(video_id)
        ytb_df.to_csv(output_file)
        logging.info("Successfully saved YouTube comments data to %s.", output_file)
    except Exception as e:
        logging.exception("An error occurred during data collection: %s", e)


if __name__ == "__main__":
    main()
