import requests
from bs4 import BeautifulSoup
import string
import csv
# from tqdm import tqdm
# from tqdm import trange
import time 
from threading import Thread
from multiprocessing.pool import ThreadPool as Pool
import os 

no_of_cores = os.cpu_count()

def get_like_dislike_data_with_retries(word_page_link, char, max_retries=5):
    for _ in range(max_retries):
        try:
            return get_like_dislike_data(word_page_link)
        except:
            with open(f"data/error_log_{char}.txt", "a") as myfile:
                myfile.write("Error in get_like_dislike_data_with_retries for link " + word_page_link + "\n")
            time.sleep(600)
    return None, None

def get_like_dislike_data(word_page_link):
    page = requests.get(word_page_link)
    soup  = BeautifulSoup(page.content, "html.parser")
    all_results = soup.find_all(class_ = "definition bg-white mb-4 shadow-light dark:bg-yankees dark:text-white rounded-md overflow-hidden")
    defids = []
    for i in range(len(all_results)):
        defids.append(all_results[i]["data-defid"])
    base_like_dislike_url = "https://api.urbandictionary.com/v0/uncacheable?ids="
    for i in defids:
        base_like_dislike_url += i + ","
    base_like_dislike_url = base_like_dislike_url[:-1]
    like_dislike_data = requests.get(base_like_dislike_url)
    like_dislike_data = like_dislike_data.json()
    likes = []
    dislikes = []
    for i in like_dislike_data["thumbs"]:
        likes.append(i["up"])
        dislikes.append(i["down"])
    return likes, dislikes

def get_soup_for_a_char_for_a_given_page_num_with_retries(URL_for_a_char_for_a_given_page_num, char, max_retries=5):
    for _ in range(max_retries):
        try:
            return get_soup_for_a_char_for_a_given_page_num(URL_for_a_char_for_a_given_page_num)
        except:
            with open(f"data/error_log_{char}.txt", "a", encoding="utf-8") as myfile:
                myfile.write("Error in get_soup_for_a_char_for_a_given_page_num_with_retries for link " + URL_for_a_char_for_a_given_page_num + "\n")
            time.sleep(600)
    return None

def get_soup_for_a_char_for_a_given_page_num(link):
    page_for_a_char_for_a_given_page_num = requests.get(link)
    soup_for_a_char_for_a_given_page_num  = BeautifulSoup(page_for_a_char_for_a_given_page_num.content, "html.parser")
    return soup_for_a_char_for_a_given_page_num

def get_soup_for_a_char_with_retries(link, char, max_retries=5):
    for _ in range(max_retries):
        try:
            return get_soup_for_a_char(link)
        except:
            with open(f"data/error_log_{char}.txt", "a", encoding="utf-8") as myfile:
                myfile.write("Error in get_soup_for_a_char_with_retries for link " + link + "\n")
            time.sleep(600)
    return None

def get_soup_for_a_char(link):
    page_for_a_char = requests.get(link)
    soup_for_a_char  = BeautifulSoup(page_for_a_char.content, "html.parser")
    return soup_for_a_char

def get_soup_for_word_with_retries(link, char, max_retries=5):
    for _ in range(max_retries):
        try:
            return get_soup_for_word(link)
        except:
            with open(f"data/error_log_{char}.txt", "a", encoding="utf-8") as myfile:
                myfile.write("Error in get_soup_for_word_with_retries for link " + link + "\n")
            time.sleep(600)
    return None

def get_soup_for_word(link):
    page_for_word = requests.get(link)
    soup_for_word  = BeautifulSoup(page_for_word.content, "html.parser")
    return soup_for_word

def get_soup_word_for_page_num_with_retries(link, char, max_retries=5):
    for _ in range(max_retries):
        try:
            return get_soup_word_for_page_num(link)
        except:
            with open(f"data/error_log_{char}.txt", "a", encoding="utf-8" ) as myfile:
                myfile.write("Error in get_soup_word_for_page_num_with_retries for link " + link + "\n")
            time.sleep(600)
    return None


    
def get_soup_word_for_page_num(link):
    page_word_for_page_num = requests.get(link)
    soup_word_for_page_num  = BeautifulSoup(page_word_for_page_num.content, "html.parser")
    return soup_word_for_page_num


def scrape_all_of_urban_dictionary(char):
    with open(f'data/data_{char}.csv', 'w', encoding='utf-8') as csvfile:
        fieldnames = ['title', 'meaning', 'example', 'contributor', 'like', 'dislike']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        # Get all Upper Case English characters
        with open(f"data/error_log_{char}.txt", "w", encoding="utf-8") as myfile:
            myfile.write("")
        BASE_URL = "https://www.urbandictionary.com/"
        ls_chars = [char]
        all_titles = []
        all_word_meanings = []
        all_examples = []
        all_contributor_details = []
        all_likes = []
        all_dislikes = []
        for char in (ls_chars):
            URL = f"https://www.urbandictionary.com/browse.php?character={char}"
            print(URL)
            soup_for_a_char = get_soup_for_a_char_with_retries(URL, char)
            if soup_for_a_char is None:
                continue
            last_page_for_a_char  = int(soup_for_a_char.find_all("a", class_="px-3 py-1 rounded-full hover:bg-denim hover:text-white text-light-charcoal")[-1]['href'].split('=')[-1])
            for page_num_for_a_char in range(1, last_page_for_a_char + 1):
                URL_for_a_char_for_a_given_page_num = f"https://www.urbandictionary.com/browse.php?character={char}&page={page_num_for_a_char}"
                print(URL_for_a_char_for_a_given_page_num)
                soup_for_a_char_for_a_given_page_num = get_soup_for_a_char_for_a_given_page_num_with_retries(URL_for_a_char_for_a_given_page_num, char)
                if soup_for_a_char_for_a_given_page_num is None:
                    continue
                words_for_a_char_on_a_given_page_num = soup_for_a_char_for_a_given_page_num.find_all(class_="py-1 block text-denim dark:text-white break-all hover:text-limon-lime hover:underline")
                for word_element in (words_for_a_char_on_a_given_page_num):
                    link_for_words_for_a_char_on_a_given_page_num = word_element['href']
                    word_link_for_words_for_a_char_on_a_given_page_num = BASE_URL + link_for_words_for_a_char_on_a_given_page_num
                    print(word_link_for_words_for_a_char_on_a_given_page_num)

                    soup_for_word = get_soup_for_word_with_retries(word_link_for_words_for_a_char_on_a_given_page_num, char)
                    if soup_for_word is None:
                        continue

                    last_page_for_word = soup_for_word.find_all("a", class_="px-3 py-1 rounded-full hover:bg-denim hover:text-white text-light-charcoal")
                    if len(last_page_for_word) == 0:
                        last_page_for_word = 1
                    else:
                        last_page_for_word = int(last_page_for_word[-1]['href'].split('=')[-1])
                    for word_page_num in range(1, last_page_for_word+1):
                        word_page_link = word_link_for_words_for_a_char_on_a_given_page_num + f"&page={word_page_num}"
                        print(word_page_link)

                        soup_word_for_page_num = get_soup_word_for_page_num_with_retries(word_page_link, char)
                        if soup_word_for_page_num is None:
                            continue

                        likes, dislikes = get_like_dislike_data_with_retries(word_page_link, char)
                        if likes is None or dislikes is None:
                            continue

                        titles = soup_word_for_page_num.find_all(class_="word text-denim font-bold font-serif dark:text-fluorescent break-all text-3xl md:text-[2.75rem] md:leading-10") 
                        word_meanings = soup_word_for_page_num.find_all(class_="break-words meaning mb-4")
                        examples = soup_word_for_page_num.find_all(class_="break-words example italic mb-4")
                        contributor_details = soup_word_for_page_num.find_all(class_="contributor font-bold")
                        titles = [i.text for i in titles]
                        word_meanings = [i.text for i in word_meanings]
                        examples = [i.text for i in examples]
                        contributor_details = [i.text for i in contributor_details]
                        for i,j,k,l,m,n in zip(titles, word_meanings, examples, contributor_details, likes, dislikes):
                            try:
                                writer.writerow({'title': i, 'meaning': j, 'example': k, 'contributor': l, 'like': m, 'dislike': n})
                            except:
                                # Write Error to file
                                with open('error_log_{char}.txt', 'a', encoding='utf-8') as f:
                                    f.write(f"data/error while writing {i},{j},{k},{l},{m},{n}\n")
                                continue
                        all_titles.extend(titles)
                        all_word_meanings.extend(word_meanings)
                        all_examples.extend(examples)
                        all_contributor_details.extend(contributor_details)
                        all_likes.extend(likes)
                        all_dislikes.extend(dislikes)
        print(len(all_titles))
        print(len(all_word_meanings))
        print(len(all_examples))
        print(len(all_contributor_details))
        print(len(all_likes))
        print(len(all_dislikes))

start_time = time.time() 

ls_chars = list(string.ascii_uppercase + '*')

pool = Pool(os.cpu_count())

for i in ls_chars:
    pool.apply_async(scrape_all_of_urban_dictionary, (i,))
    
# scrape_all_of_urban_dictionary()
pool.close()
pool.join()

total_time = time.time() - start_time

# Write total time to a file

with open('total_time.txt', 'w') as f:
    f.write(str(total_time))
    f.close()

print(total_time)