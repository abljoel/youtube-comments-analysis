"""
YouTube Comments Data Collection Script

This module provides functions for fetching and collecting YouTube comments data
from a specified video using the YouTube API. It uses the 'googleapiclient.discovery'
library for building the API service and 'pandas' for handling data.

Functions:
    - fetch_youtube_comments: Fetches YouTube comments for a given video.
    - fetch_batch_data_from_video: Returns a DataFrame of YouTube comments data.
    - main: Collects YouTube comments data and saves it to a specified output file.

Note:
    To use the functions in this module, ensure you have the necessary API credentials,
    including a valid YouTube API key, and have the required libraries installed 
    (e.g., 'pandas', 'google-api-python-client').

Usage:
    Run this module as a script to collect YouTube comments data from a specified video.
    Command Line Example:
        python data_collecton.py --video_id YOUR_VIDEO_ID --output_file OUTPUT_FILE_PATH
"""
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
    """
    Fetches YouTube comments for a given video.

    Args:
        target (str): The part parameter specifies a comma-separated list
                      of commentThread resource properties.
        video (str): The ID of the video for which the comments are fetched.
        results (int): The maximum number of comments to retrieve.
        service (str): The API service to use for fetching comments.
        version (str): The API version to use.
        key (str): The API key for authentication.

    Returns:
        list: A list containing information about each comment, including
              author name, publication date, update date, like count,
              and comment text.

    Raises:
        Any exceptions raised during the API request.

    Note:
        This function uses the YouTube API to fetch comments and may require
        appropriate API credentials.
    """
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
    """
    Returns a DataFrame of YouTube data.

    Args:
        vid (str): The YouTube video ID for which comments data is collected.
        limit (int, optional): The maximum number of comments to retrieve. Defaults to 3000.

    Returns:
        pandas.DataFrame: A DataFrame containing YouTube comments data with columns:
            - 'author': Author name of the comment.
            - 'published_at': Publication date of the comment.
            - 'updated_at': Update date of the comment.
            - 'likes': Number of likes on the comment.
            - 'text': Text content of the comment.

    Raises:
        googleapiclient.errors.HttpError: If an HTTP error occurs during the API request.

    Note:
        This function utilizes the 'fetch_youtube_comments' function to retrieve comments
        and creates a DataFrame with specified column names.
    """
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
