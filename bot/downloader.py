import random
import subprocess
import time


def download_torrent(url, title):
    # Construct the aria2c command with additional options
    output_file = "./torrents"  # Output file path
    command = ['aria2c', '-s', '64', '-x', '16',
               '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
               '--seed-time=0', '--seed-ratio=0.0', '--allow-overwrite=true',
               '--optimize-concurrent-downloads', '--auto-file-renaming=false', f'-d {output_file}', url]

    # Start the download process
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)

    # Continuously read the output and yield progress updates
    start_time = int(time.time())
    for line in process.stdout:
        ctime = int(time.time())
        if line == "(OK):download completed.\n":
            return line
        if line.startswith('['):
            if not (ctime - start_time) % 10:
                details = line.replace('[', '').replace(']', '').split()
                choice = random.randint(15, 25)
                dd = f'🎬{title[:choice]}...\n📼 Progress: {details[1]}\n⬇️ {details[-2]}\n⏳ {details[-1]}'
                yield dd

    # Wait for the download proces+s to finish
    process.wait()


# if __name__ == "__main__":
#     magnet_link = "magnet:?xt=urn:btih:5E09365E169A0D45FD33F5439A2C14854EDDEDCF&dn=PureTaboo+23+06+27+Leana+Lovings+XXX+480p+MP4-XXX+%5BXC%5D&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969%2Fannounce&tr=udp%3A%2F%2Fexodus.desync.com%3A6969%2Fannounce&tr=udp%3A%2F%2Fopen.stealth.si%3A80%2Fannounce&tr=udp%3A%2F%2Ftracker.moeking.me%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A1337%2Fannounce&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce&tr=udp%3A%2F%2Fopentor.org%3A2710%2Fannounce&tr=udp%3A%2F%2Ftracker.tiny-vps.com%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.torrent.eu.org%3A451%2Fannounce&tr=udp%3A%2F%2Fexplodie.org%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce&tr=http%3A%2F%2Ftracker.openbittorrent.com%3A80%2Fannounce&tr=udp%3A%2F%2Fopentracker.i2p.rocks%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.internetwarriors.net%3A1337%2Fannounce&tr=udp%3A%2F%2Ftracker.leechers-paradise.org%3A6969%2Fannounce&tr=udp%3A%2F%2Fcoppersurfer.tk%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.zer0day.to%3A1337%2Fannounce"
#     destination_folder = "/torrents"
#
#     for progress in download_torrent(magnet_link, "testtt uhi jjjskk"):
#         print(progress)
