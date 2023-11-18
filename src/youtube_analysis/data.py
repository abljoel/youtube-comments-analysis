import googleapiclient.discovery


def fetch_youtube_comments(target, video, results, service, version, key):
    youtube = googleapiclient.discovery.build(
        service,
        version,
        developerKey=key
    )
    
    request = youtube.commentThreads().list(
        part=target,
        videoId=video,
        maxResults=results
    )
    
    response = request.execute()
    comments = []
    while response:  
        for item in response['items']:
            comment = item['snippet']['topLevelComment']['snippet']
            comments.append([
                comment['authorDisplayName'],
                comment['publishedAt'],
                comment['updatedAt'],
                comment['likeCount'],
                comment['textDisplay']
            ])
        # Check if there are more comments and continue iterating  
        if 'nextPageToken' in response:  
            response = youtube.commentThreads().list(  
                part=target,  
                videoId=video,  
                textFormat='plainText',  
                pageToken=response['nextPageToken']  
            ).execute()  
        else:  
            break
            
    return comments