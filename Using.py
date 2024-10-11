from Functions import Run
from imports import web_url


def main(search_text):
    Run(web_url=web_url, search_text=search_text)


if __name__ == '__main__':
    search_text = input("Lütfen aramak istediğiniz kurumun detsisNo'sunu girin: ")
    main(search_text)