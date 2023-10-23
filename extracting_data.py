import os
import json
import nltk
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import Counter, defaultdict
from datetime import datetime
import pandas as pd

nltk.download('stopwords')
stop_words = stopwords.words('english')



def find_json_files(directory_path):
    json_files = []
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.json'):
                json_files.append(os.path.join(root, file))
    return json_files


def clean_text(text):
    
    text = re.sub(r"http\S+|www\S+|https\S+", '', text, flags=re.MULTILINE)
    
    text = re.sub(r'<.*?>', '', text)
    
    text = re.sub(r'[^A-Za-z\s]', '', text)
    
    text = text.strip()
    return text


def get_ids_and_bodies_from_json(json_data):
    ids = []
    bodies = []
    dates = []
    for item in json_data['response']['results']:
            if 'id' in item:
                ids.append(item['id'])
            if 'fields' in item and "body" in item['fields']:
                bodies.append(item['fields']['body'])
            if "webPublicationDate" in item:
                date = item["webPublicationDate"]
                dates.append(date)

    return ids, bodies, dates

def extract_ids_and_bodes(json_files):
    unique_ids = set()
    unique_bodies = set()
    
    for json_file in json_files:
        print(json_file)
        with open(json_file, 'r') as file:
            try:
                json_data = json.load(file)
                ids, bodies, _ = get_ids_and_bodies_from_json(json_data)
                unique_ids.update(ids)
                unique_bodies.update(bodies)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON from file {json_file}: {e}")
    return unique_ids, unique_bodies


def extract_body_with_date(json_files):
    data = {}
    for json_file in json_files:
        print(json_file)
        with open(json_file, 'r') as file:
            try:
                json_data = json.load(file)
                ids, bodies,dates = get_ids_and_bodies_from_json(json_data)
                for i in range(len(ids)):
                    data[ids[i]] = (bodies[i],dates[i])
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON from file {json_file}: {e}")
    return  data


def main():

    directory_path = 'data/guardian'
    json_files = find_json_files(directory_path)
    unique_ids, unique_bodies = extract_ids_and_bodes(json_files)
    texts = list(unique_bodies)
    cleaned_texts = [clean_text(text) for text in texts]

    tfidfvectorizer = TfidfVectorizer(analyzer='word', stop_words=stop_words)

    # Apply TF-IDF to your texts
    tfidf_wm = tfidfvectorizer.fit_transform(cleaned_texts)

    # Retrieve the token names
    token_names = tfidfvectorizer.get_feature_names_out()

    # Calculate the average TF-IDF values for each word across all documents
    avg_tfidf = tfidf_wm.mean(axis=0)
    avg_tfidf_dict = {token_names[i]: avg_tfidf[0, i] for i in range(len(token_names))}

    # Generate the word cloud based on TF-IDF values
    wordcloud = WordCloud(width=800, height=400, max_font_size=110).generate_from_frequencies(avg_tfidf_dict)

    plt.figure(figsize=(15, 8))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis('off')
    plt.savefig('wordcloud.png')
    plt.show()

    


if __name__ == "__main__":
    directory_path = 'data/guardian'
    json_files = find_json_files(directory_path)
    data = extract_body_with_date(json_files)
    for key in data:
        data[key] = (data[key][0].lower(), data[key][1]) 

    texts = [data[key][0] for key in data]
    times = [data[key][1] for key in data]
    times = [datetime.fromisoformat(dt_string.replace('Z', '+00:00')).strftime("%Y-%m-%d") for dt_string in times]

    

    n_grams = ["october_7", "7th_of_october", "october_7th", "7_october"]
    words_to_count = [ "occupation", "siege", "besieged"]



    preprocessed_texts = [re.sub(r'[^a-z0-9\s]', '', text.lower().replace('_', ' ')) for text in texts]

    # Initialize a defaultdict to store the count of each n-gram and word for each unique time
    frequency_dict = defaultdict(lambda: defaultdict(int))

    # Function to update the frequency dictionary
    def update_frequency_dict(time, words, n_grams):
        # Count words
        word_frequencies = Counter(words)
        for word in words_to_count:
            frequency_dict[time][word] += word_frequencies[word]
        
        # Count n-grams
        text = ' '.join(words)
        for n_gram in n_grams:
            frequency_dict[time][n_gram] += text.count(n_gram.replace('_', ' '))

    # Search and count n-grams and words in texts
    for text, time in zip(preprocessed_texts, times):
        words = text.split()
        update_frequency_dict(time, words, n_grams)

    # Convert defaultdict to regular dictionary for better readability
    frequency_dict = dict(frequency_dict)

    # Print the results
    for k in frequency_dict:
        frequency_dict[k]["oct7"] = sum([frequency_dict[k][n_gram] for n_gram in n_grams])
        [frequency_dict[k].pop(n_gram) for n_gram in n_grams]

    
    df = pd.DataFrame.from_dict(frequency_dict, orient='index').fillna(0)
    df.index = pd.to_datetime(df.index)

    # Sort DataFrame by date
    df.sort_index(inplace=True)

    # Plot the data
    plt.figure(figsize=(10, 5))
    for column in df.columns:
        plt.plot(df.index, df[column], marker='o', label=column)

    # Customize the plot
    plt.title('Word Frequency Timeline')
    plt.xlabel('Date')
    plt.ylabel('Frequency')
    plt.xticks(df.index, df.index.date, rotation=45)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()

    # Show the plot
    plt.tight_layout()
    plt.savefig("word_frequency_timeline.png")









    
