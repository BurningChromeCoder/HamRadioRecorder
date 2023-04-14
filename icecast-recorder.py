import os
import sys
import traceback
from urllib.request import Request, urlopen
from time import time
from datetime import timedelta
import time
from datetime import datetime


if len(sys.argv) != 3:
    print("Usage: icecast_recorder.py <url> <duration in seconds>")
    sys.exit(1)

stream = urlopen(Request(sys.argv[1], headers={"Icy-MetaData": "1"}), timeout=8)
headers = dict((k.lower(), v) for k, v in stream.getheaders())

if "icy-metaint" in headers:
    meta_interval = int(headers["icy-metaint"])
else:
    print("!ERROR!\n"
          "Server did not return Icy-Metaint\n"
          "Are you sure the server is Icecast compatible?")
    sys.exit(2)

# Print server information
if "icy-name" in headers:
    print(headers["icy-name"])
if "icy-url" in headers:
    print("URL: ", headers["icy-url"])
if "icy-genre" in headers:
    print("Genre: ", headers["icy-genre"])
if "icy-br" in headers:
    print("Bitrate: ", headers["icy-br"], "kb/s")
print("--------------------------------------------")

filename = f"Programa-Contactos_{datetime.now().strftime('%Y-%m-%d-%H-%M')}.mp3"
file = open(filename, "wb")
start_time = datetime.now()
counter = 0
total_time = int(sys.argv[2])
progress_bar_length = 50
progress_bar_current = 0

try:
    # Music download loop
    while True:
        metadata = None
        # See shoutcast-metadata.jpg for stream struct
        # Save music chunk
        file.write(stream.read(meta_interval))
        # Get number of blocks with meta information
        blocks = int.from_bytes(stream.read(1), byteorder='big')
        if blocks > 0:
            # Read meta information. Each block == 16 bytes
            raw_data = stream.read(blocks * 16).decode("UTF-8")
            try:
                metadata = {}
                # Parse Key1='Val1';Key2='Val2';
                for pair in raw_data.split(';'):
                    tmp = pair.split('=')
                    if len(tmp) > 1:
                        metadata[tmp[0]] = tmp[1].strip("'")
            except Exception as e:
                pass

        # Processing track change
        if metadata is not None:
            time_offset = datetime.now() - start_time
            if "StreamTitle" in metadata:
                stream_title = metadata["StreamTitle"].replace('/', '_')
                file.close()
                print(str(time_offset) + "   " + stream_title)
                filename = f"Programa-Contactos_{datetime.now().strftime('%Y-%m-%d-%H-%M')}.mp4"
                file = open(filename, "wb")
                counter += 1

            else:
                raise Exception("No StreamTitle in meta:", meta_data)

        # Update progress bar
        progress = min(int((datetime.now() - start_time).total_seconds() / total_time * 100), 100)
        if progress > progress_bar_current:
            progress_bar_current = progress
            progress_bar = "#" * (progress_bar_length * progress // 100)
            progress_bar += " " * (progress_bar_length - len(progress_bar))
            print(f"[{progress_bar}] {progress}%")

        # Print elapsed time every second
        time_elapsed = datetime.now() - start_time
        while time_elapsed < timedelta(seconds=1):
            time.sleep(0.1)
            time_elapsed = datetime.now() - start_time
        print(str(time_elapsed)[:-7], end="\r")

        

        # Stop recording after specified duration
        if time_elapsed.total_seconds() >= total_time:
            break
except KeyboardInterrupt: # Ctrl+C
    stream.close()
    
# Close the file
file.close()
