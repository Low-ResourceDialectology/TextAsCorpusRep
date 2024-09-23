import os
import re
from collections import Counter
import statistics
import json
import jieba  # Import jieba for Chinese word segmentation

def is_chinese(text):
    """Check if the text contains Chinese characters."""
    return any('\u4e00' <= char <= '\u9fff' for char in text)

def get_word_count(text, is_chinese_text=False):
    """Count words, using jieba for Chinese if necessary."""
    if is_chinese_text:
        words = jieba.lcut(text)
    else:
        words = text.split()
    return len(words)

def get_unique_words(text, is_chinese_text=False):
    """Get unique words, using jieba for Chinese if necessary."""
    if is_chinese_text:
        words = jieba.lcut(text)
    else:
        words = text.lower().split()
    return set(words)

def get_sentence_length(text, is_chinese_text=False):
    """Get sentence length in words, using jieba for Chinese if necessary."""
    if is_chinese_text:
        words = jieba.lcut(text)
    else:
        words = text.split()
    return len(words)

def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    word_counts = []
    sentence_lengths = []
    all_words = []
    all_sentences = []
    min_sentence = None
    max_sentence = None
    
    for line in lines:
        line = line.strip()
        if line:
            is_chinese_text = is_chinese(line)
            word_count = get_word_count(line, is_chinese_text)
            sentence_length = get_sentence_length(line, is_chinese_text)
            
            word_counts.append(word_count)
            sentence_lengths.append(sentence_length)
            
            all_sentences.append(line)

            # Use jieba for Chinese word segmentation, split for others
            if is_chinese_text:
                all_words.extend(jieba.lcut(line))
            else:
                all_words.extend(line.lower().split())
            
            # Track the shortest and longest sentences
            if min_sentence is None or sentence_length < len(min_sentence.split()):
                min_sentence = line
            if max_sentence is None or sentence_length > len(max_sentence.split()):
                max_sentence = line

    
    return {
        'line_count': len(lines),
        'total_words': sum(word_counts),
        'unique_words': set(all_words),
        'unique_sentences': set(all_sentences),
        'sentence_length': {
            'min': min(sentence_lengths),
            'max': max(sentence_lengths),
            'mean': statistics.mean(sentence_lengths),
            'shortest_sentence': min_sentence,
            'longest_sentence': max_sentence
        },
        'word_frequency': Counter(all_words)
    }

def process_language(language_dir):
    # Dictionaries for words, sentences, and word frequency
    word_stats = {
        'total_files': 0,
        'total_words': 0,
        'unique_words': set(),  # Keep as a set to merge across files
        'files': {}
    }
    
    sentence_stats = {
        'total_lines': 0,
        'unique_sentences': set(),
        'sentence_lengths': [],
        'shortest_sentence': None,
        'longest_sentence': None,
        'files': {}
    }
    
    word_freq = Counter()
    
    for root, dirs, files in os.walk(language_dir):
        for file in files:
            if file.endswith('.txt'):
                file_path = os.path.join(root, file)
                file_stats = process_file(file_path)
                
                # Word stats at the file level
                word_stats['files'][file] = {
                    'total_words': file_stats['total_words'],
                    'unique_words': len(file_stats['unique_words'])
                }
                
                # Sentence stats at the file level
                sentence_stats['files'][file] = {
                    'line_count': file_stats['line_count'],
                    'unique_sentences': len(file_stats['unique_sentences']),
                    'sentence_length': file_stats['sentence_length'],
                }
                
                # Update overall word stats
                word_stats['total_files'] += 1
                word_stats['total_words'] += file_stats['total_words']
                word_stats['unique_words'].update(file_stats['unique_words'])
                
                # Update overall sentence stats
                sentence_stats['total_lines'] += file_stats['line_count']
                sentence_stats['sentence_lengths'].extend([
                    file_stats['sentence_length']['min'],
                    file_stats['sentence_length']['max']
                ])
                sentence_stats['unique_sentences'].update(file_stats['unique_sentences'])
                
                # Track the shortest and longest sentences across all files
                if (sentence_stats['shortest_sentence'] is None or 
                    len(file_stats['sentence_length']['shortest_sentence'].split()) < len(sentence_stats['shortest_sentence'].split())):
                    sentence_stats['shortest_sentence'] = file_stats['sentence_length']['shortest_sentence']
                
                if (sentence_stats['longest_sentence'] is None or 
                    len(file_stats['sentence_length']['longest_sentence'].split()) > len(sentence_stats['longest_sentence'].split())):
                    sentence_stats['longest_sentence'] = file_stats['sentence_length']['longest_sentence']
                
                # Word frequency
                word_freq.update(file_stats['word_frequency'])
    
    # Final calculations for unique words and sentence stats
    word_stats['unique_words'] = len(word_stats['unique_words'])  # Convert set to count of unique words
    sentence_stats['unique_sentences'] = len(sentence_stats['unique_sentences'])
    sentence_stats['sentence_length'] = {
        'min': min(sentence_stats['sentence_lengths']),
        'max': max(sentence_stats['sentence_lengths']),
        'mean': statistics.mean(sentence_stats['sentence_lengths']),
        'shortest_sentence': sentence_stats['shortest_sentence'],
        'longest_sentence': sentence_stats['longest_sentence']
    }
    
    # Sort word frequency in decreasing order and return as a dictionary
    sorted_word_freq = dict(word_freq.most_common())
    
    return word_stats, sentence_stats, sorted_word_freq


def main():
    corpus_dir = './../corpus'
    output_dir = './../corpus_information'
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for language in os.listdir(corpus_dir):
        
        language_output_dir = os.path.join(output_dir, language)
        if not os.path.exists(language_output_dir):
            os.makedirs(language_output_dir)
    
        language_dir = os.path.join(corpus_dir, language)
        if os.path.isdir(language_dir):
            print(f"Processing {language}...")
            
            # Process language and get the separated stats
            word_stats, sentence_stats, sorted_word_freq = process_language(language_dir)
            
            # Output file paths
            word_output_file = os.path.join(language_output_dir, f"words_info.json")
            sentence_output_file = os.path.join(language_output_dir, f"sentences_info.json")
            freq_output_file = os.path.join(language_output_dir, f"word_freq.json")
            
            # Write word stats to file
            with open(word_output_file, 'w', encoding='utf-8') as f:
                json.dump(word_stats, f, ensure_ascii=False, indent=2)
            #print(f"Word statistics for {language} saved to {word_output_file}")
            
            # Write sentence stats to file
            with open(sentence_output_file, 'w', encoding='utf-8') as f:
                json.dump(sentence_stats, f, ensure_ascii=False, indent=2)
            #print(f"Sentence statistics for {language} saved to {sentence_output_file}")
            
            # Write sorted word frequency to file
            with open(freq_output_file, 'w', encoding='utf-8') as f:
                json.dump(sorted_word_freq, f, ensure_ascii=False, indent=2)
            #print(f"Word frequency for {language} saved to {freq_output_file}")

if __name__ == "__main__":
    main()