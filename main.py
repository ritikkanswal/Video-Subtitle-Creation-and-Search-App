import subprocess
import tempfile

# Run CCExtractor command and capture output
result = subprocess.run(['ccextractor', '-out=srt', 'demo.mp4'], capture_output=True, text=True)

# Check if the CCExtractor command was successful
if result.returncode == 0:
    # Extracted subtitles are stored in the result.stdout
    subtitles = result.stdout
    # print(subtitles)
    print(subtitles)
else:
    # CCExtractor command failed, print the error message
    print(result.stderr)


# def parse_srt_file(file_path, table_name):
#     # Create a DynamoDB client
#     # dynamodb = boto3.client('dynamodb')

#     # Open the SRT file for reading
#     with open(file_path, 'r') as file:
#         subtitles = file.read()

#     # Split the subtitles into individual subtitle blocks
#     subtitle_blocks = subtitles.strip().split('\n\n')

#     # Iterate over each subtitle block
#     for block in subtitle_blocks:
#         # Split the block into lines
#         lines = block.strip().split('\n')
#         print(lines)
#         # Extract the subtitle index, timestamps, and text
#         index = lines[0]
#         timestamps = lines[1].split(' --> ')
#         start_time = timestamps[0]
#         end_time = timestamps[1]
#         text = ' '.join(lines[2:])

#         # Create an item for the subtitle in the DynamoDB table
#         item = {
#             'SubtitleIndex': {'N': str(index)},
#             'StartTime': {'S': start_time},
#             'EndTime': {'S': end_time},
#             'Text': {'S': text}
#         }
#         print(item)

#         # Put the item into the DynamoDB table
#         response = dynamodb.put_item(
#             TableName=table_name,
#             Item=item
#         )

#         # Print the response (optional)
#         print(response)

# # Example usage
# srt_file_path = 'demo.srt'
# dynamodb_table_name = 'subtitle_data'
# parse_srt_file(srt_file_path, dynamodb_table_name)