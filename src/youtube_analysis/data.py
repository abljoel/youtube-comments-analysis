"""
YouTube API Module

This module provides a function to interact with the YouTube API for fetching comments
from a specified video. It uses the 'googleapiclient.discovery' library for building
the API service.

Functions:
    - fetch_youtube_comments: Fetches YouTube comments for a given video.

Note:
    To use the functions in this module, ensure you have the necessary API credentials,
    including a valid API key.

Example:
    # Import the module
    import data

    # Call the fetch_youtube_comments function
    comments = data.fetch_youtube_comments(
        target='snippet',
        video='your_video_id',
        results=10,
        service='youtube',
        version='v3',
        key='your_api_key'
    )
"""

import googleapiclient.discovery


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
