def load_profanity_list(profanity_file):
    """Load profanity words from a file into a set."""
    with open(profanity_file, 'r') as file:
        return set(word.strip().lower() for word in file.readlines())

def find_profanities(transcribed_data, profanity_file='../data/profanity.txt'):
    print("Loading Profanity List...")
    profanities = load_profanity_list(profanity_file)

    matches = []

    print("Finding profanities...")
    for item in transcribed_data:
        word = item['text'].strip().lower()  
        timestamp = item['timestamp']
        
        if word in profanities:
            matches.append({'word': word, 'timestamp': timestamp})

    return matches