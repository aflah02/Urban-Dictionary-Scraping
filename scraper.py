import requests
from bs4 import BeautifulSoup
import string
import csv
from tqdm import tqdm
from tqdm import trange

with open('data.csv', 'w', encoding='utf-8') as csvfile:
    fieldnames = ['title', 'meaning', 'example', 'contributor']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    # Get all Upper Case English characters

    ls_chars = string.ascii_uppercase + '*'

    BASE_URL = "https://www.urbandictionary.com/"

    all_titles = []
    all_word_meanings = []
    all_examples = []
    all_contributor_details = []
    all_likes_dislikes = []
    visited = set()
    for char in (ls_chars):
        URL = f"https://www.urbandictionary.com/browse.php?character={char}"
        print(URL)
        page_for_a_char = requests.get(URL)
        soup_for_a_char  = BeautifulSoup(page_for_a_char.content, "html.parser")
        last_page_for_a_char  = int(soup_for_a_char.find_all("a", class_="px-3 py-1 rounded-full hover:bg-denim hover:text-white text-light-charcoal")[-1]['href'].split('=')[-1])
        for page_num_for_a_char in range(1, last_page_for_a_char + 1):
            URL_for_a_char_for_a_given_page_num = f"https://www.urbandictionary.com/browse.php?character={char}&page={page_num_for_a_char}"
            print(URL_for_a_char_for_a_given_page_num)
            page_for_a_char_for_a_given_page_num = requests.get(URL_for_a_char_for_a_given_page_num)
            soup_for_a_char_for_a_given_page_num = BeautifulSoup(page_for_a_char_for_a_given_page_num.content, "html.parser")
            words_for_a_char_on_a_given_page_num = soup_for_a_char_for_a_given_page_num.find_all(class_="py-1 block text-denim dark:text-white break-all hover:text-limon-lime hover:underline")
            for word_element in (words_for_a_char_on_a_given_page_num):
                link_for_words_for_a_char_on_a_given_page_num = word_element['href']
                word_link_for_words_for_a_char_on_a_given_page_num = BASE_URL + link_for_words_for_a_char_on_a_given_page_num
                print(word_link_for_words_for_a_char_on_a_given_page_num)
                page_for_word = requests.get(word_link_for_words_for_a_char_on_a_given_page_num)
                soup_for_word = BeautifulSoup(page_for_word.content, "html.parser")
                last_page_for_word = soup_for_word.find_all("a", class_="px-3 py-1 rounded-full hover:bg-denim hover:text-white text-light-charcoal")
                if len(last_page_for_word) == 0:
                    last_page_for_word = 1
                else:
                    last_page_for_word = int(last_page_for_word[-1]['href'].split('=')[-1])
                for word_page_num in range(1, last_page_for_word+1):
                    word_page_link = word_link_for_words_for_a_char_on_a_given_page_num + f"&page={word_page_num}"
                    print(word_page_link)
                    word_page_for_page_num = requests.get(word_page_link)
                    soup_word_for_page_num = BeautifulSoup(word_page_for_page_num.content, "html.parser")
                    titles = soup_word_for_page_num.find_all(class_="word text-denim font-bold font-serif dark:text-fluorescent break-all text-3xl md:text-[2.75rem] md:leading-10") 
                    word_meanings = soup_word_for_page_num.find_all(class_="break-words meaning mb-4")
                    examples = soup_word_for_page_num.find_all(class_="break-words example italic mb-4")
                    contributor_details = soup_word_for_page_num.find_all(class_="contributor font-bold")
                    likes_dislikes = soup_word_for_page_num.find_all(class_="text-xs font-bold ml-2")
                    titles = [i.text for i in titles]
                    word_meanings = [i.text for i in word_meanings]
                    examples = [i.text for i in examples]
                    contributor_details = [i.text for i in contributor_details]
                    likes_dislikes = [i.text for i in likes_dislikes]
                    for i,j,k,l in zip(titles, word_meanings, examples, contributor_details):
                        writer.writerow({'title': i, 'meaning': j, 'example': k, 'contributor': l})
                    all_titles.extend(titles)
                    all_word_meanings.extend(word_meanings)
                    all_examples.extend(examples)
                    all_contributor_details.extend(contributor_details)
                    all_likes_dislikes.extend(likes_dislikes)
    print(len(all_titles))
    print(len(all_word_meanings))
    print(len(all_examples))
    print(len(all_contributor_details))