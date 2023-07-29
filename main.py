import argparse
import subprocess
import requests
from bs4 import BeautifulSoup

def get_link_from_arg():
    parser = argparse.ArgumentParser()
    parser.add_argument('--link', required=True, help="MkZ episode link.")
    return parser.parse_args().link

def get_page(link):
    response = requests.get(link)
    response.raise_for_status()
    return BeautifulSoup(response.content, "html.parser")

def get_iframes(page):
    divs_with_iframes = page.find_all("div", class_="GTTabs_divs")
    return [iframe.find("iframe")['data-src'] for iframe in divs_with_iframes if iframe.find("iframe")]

def get_source_names(page):
    sources = page.find_all("div", class_="GTTabs_divs")
    return [name.find("span").text.strip() for name in sources]

def main():
    print("Welcome to MkzPlayer V0.0.4")
    print("Usage: python main.py --link [link]")
    print("Ex: python main.py --link https://manga-kids.com/anime-ro-sub/mushoku-tensei-ii-isekai-ittara-honki-dasu-tradus-subtitrat-in-romana-ro-sub/mushoku-tensei-ii-isekai-ittara-honki-dasu-episodul-02-rosub")
    print("Source will be automatically detected")
    print("If mpv is in $PATH, this should work on Windows, too. But, I use arch, btw")
    print("Supported sources: Sendvid, Mp4Upload. If the episode doesn't have one of these, you are out of luck, my friend...")

if __name__ == "__main__":
    main()
    sources = get_iframes(get_page(get_link_from_arg()))

    if not sources:
        print("No supported source available")
    else:
        for source in sources:
            try:
                output = subprocess.run(["mpv", source], capture_output=True, check=True, text=True)
            except subprocess.CalledProcessError:
                if source.startswith("//sendvid.com"):
                    output = subprocess.run(["mpv", f'https:{source}'], capture_output=True, check=True, text=True)
                else:
                    print(f"Source {source} is not supported.")

            if output.returncode == 0:
                exit()

