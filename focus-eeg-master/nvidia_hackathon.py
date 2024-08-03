from openai import OpenAI
import numpy as np
import pandas as pd

client = OpenAI()

def transcript_to_dict(transcript_file_path, delimiter=' '):
    """
    Parses a transcript text file into a dictionary where each key is a timestamp
    and each value is the string of words spoken at that timestamp.

    Parameters:
    - transcript_file_path: str, the path to the transcript text file.
    - delimiter: str, the delimiter used to separate the timestamp from the words in the transcript.

    Returns:
    - A dictionary with timestamps as keys and strings of words as values.
    """
    transcript_dict = {}

    with open(transcript_file_path, 'r') as file:
        for line in file:
            # Split the line into timestamp and words using the delimiter
            parts = line.strip().split(delimiter, 1)
            if len(parts) == 2:
                timestamp, words = parts
                transcript_dict[timestamp] = words

    return transcript_dict

def transcript_to_string(transcript_file_path):
    """
    Reads a video transcript text file and returns the transcript as a single string.

    Parameters:
    - transcript_file_path: str, the path to the transcript text file.

    Returns:
    - A string containing the full transcript.
    """
    transcript = []

    with open(transcript_file_path, 'r') as file:
        for line in file:
            # Strip leading and trailing whitespace and newlines
            cleaned_line = line.strip()
            # Append the cleaned line to the transcript list
            transcript.append(cleaned_line)

    # Join all transcript parts into a single string, separated by spaces
    full_transcript = ' '.join(transcript)
    
    return full_transcript



def load_and_format_timeseries(csv_file_path, start_datetime='2023-01-01 00:00:00'):
    """
    Loads a CSV file containing time series data and formats it into a DataFrame with a datetime index.
    
    Parameters:
    - csv_file_path: str, path to the CSV file.
    - start_datetime: str, the starting datetime of the time series in ISO format (YYYY-MM-DD HH:MM:SS).
    
    Returns:
    - A pandas DataFrame with the time series data, indexed by datetime.
    """
    # Load the CSV file into a DataFrame
    df = pd.read_csv(csv_file_path)
    
    # Convert 'Time (Seconds)' to a datetime column based on the starting datetime
    start_time = pd.Timestamp(start_datetime)
    df['Datetime'] = start_time + pd.to_timedelta(df['Time (Seconds)'], unit='s')
    
    # Set the datetime as the DataFrame index and drop the original 'Time (Seconds)' column
    df.set_index('Datetime', inplace=True)
    df.drop('Time (Seconds)', axis=1, inplace=True)
    
    return df

def filter_transcript_based_on_focus(transcript_dict, focus_timeseries, threshold=0.6):
    """
    Filters the transcript based on focus levels below a given threshold and separates segments with a newline.

    Parameters:
    - transcript_dict: dict, transcript with timestamps as keys.
    - focus_timeseries: DataFrame, focus levels with 'Time' and 'Focus' columns.
    - threshold: float, focus level threshold.

    Returns:
    - A string containing concatenated segments of the transcript where focus is below the threshold,
      with each segment separated by a newline.
    """
    # Filter focus_timeseries based on the threshold
    low_focus_times = focus_timeseries[focus_timeseries['Focus'] < threshold]['Time']
    
    # Extract relevant segments from the transcript
    filtered_transcript = [transcript_dict[str(time)] for time in low_focus_times if str(time) in transcript_dict]
    
    # Concatenate the filtered segments into a single string, separated by newlines
    return '\n'.join(filtered_transcript)

def load_focus_timeseries(csv_file_path):
    """
    Loads a CSV file into a pandas DataFrame expected by the filter_transcript_based_on_focus function.
    
    Parameters:
    - csv_file_path: str, the path to the CSV file containing focus timeseries data.
    
    Returns:
    - A pandas DataFrame with columns 'Time' and 'Focus'.
    """
    # Load the CSV file
    df = pd.read_csv(csv_file_path)
    
    # Ensure that the DataFrame has the correct column names 'Time' and 'Focus'
    # This step assumes that your CSV has these columns named exactly as 'Time' and 'Focus'
    # If your CSV uses different column names, you might need to rename them here
    # For example, if your time column is named "timestamp", you could rename it:
    # df.rename(columns={'timestamp': 'Time'}, inplace=True)
    
    # It's also assumed that the 'Time' column format directly matches the format used in your transcript_dict keys
    # If not, you may need to convert or format the 'Time' column to match the transcript_dict key format
    
    return df

csv_file_path = 'path/to/your/focus_timeseries.csv'  # Replace with the actual path to your CSV file
focus_timeseries = load_focus_timeseries(csv_file_path)

transcript_dict = transcript_to_dict(transcript_file_path)
filtered_transcript = filter_transcript_based_on_focus(transcript_dict, focus_timeseries, threshold)

response = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {
      "role": "system",
      "content": f"Summarize the content in bulletpoint form, for a subject with no prior knowledge, in 
      the following text: {filtered_transcript}, where the sections separated by a newline are excerpts from the 
      video corresponding to excerpts that need to be summarised"

    },
  ],
  temperature=0.7,
  max_tokens=64,
  top_p=1
)