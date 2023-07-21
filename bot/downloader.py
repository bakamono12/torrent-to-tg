import random
import subprocess


def download_torrent(url, title):
    # Construct the aria2c command with additional options
    command = ['aria2c', '-s', '64', '-x', '16',
               '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
               '--optimize-concurrent-downloads', '--auto-file-renaming=false', '-o', '--dir=./bot/torrents/',  url]

    # Start the download process
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)

    # Continuously read the output and yield progress updates
    for line in process.stdout:
        if line.startswith('['):
            details = line.replace('[', '').replace(']', '').split()
            choice = random.randint(15, 25)
            dd = f'🎬{title[:choice]}...\nProgress: {details[1]}\n↯↯: {details[3]}\n{details[-1]}'
            yield dd

    # Wait for the download process to finish
    process.wait()


# for progress in download_file(url, file_path):
#     print(progress)
link = "magnet:?xt=urn:btih:8690ACEB262802B0B9E27A2D18C5EDC1325D42D2&dn=Men+in+Black%3A+International+%282019%29+%5BWEBRip%5D+%5B1080p%5D+%5BYTS%5D+%5BYIFY%5D&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969%2Fannounce&tr=udp%3A%2F%2F9.rarbg.com%3A2710%2Fannounce&tr=udp%3A%2F%2Fp4p.arenabg.com%3A1337&tr=udp%3A%2F%2Ftracker.internetwarriors.net%3A1337&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce&tr=http%3A%2F%2Ftracker.openbittorrent.com%3A80%2Fannounce&tr=udp%3A%2F%2Fopentracker.i2p.rocks%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.internetwarriors.net%3A1337%2Fannounce&tr=udp%3A%2F%2Ftracker.leechers-paradise.org%3A6969%2Fannounce&tr=udp%3A%2F%2Fcoppersurfer.tk%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.zer0day.to%3A1337%2Fannounce"
# download_torrent(link, "test.mp4", "test")
for progress in download_torrent(link, "test"):
    print(progress)
