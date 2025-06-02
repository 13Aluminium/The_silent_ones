import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import re
from typing import Dict, List, Tuple
import string
import os

def load_data(file_path: str) -> List[Dict]:
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def normalize_text(text: str) -> str:
    """Lowercase, remove punctuation, and strip whitespace."""
    text = text.lower().strip()
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text

def are_sentences_identical(gujlish: str, english: str) -> bool:
    return normalize_text(gujlish) == normalize_text(english)

def analyze_conversations(data: List[Dict]) -> Dict:
    total_conversations = len(data)
    total_sentences = 0
    english_sentences = 0
    gujlish_sentences = 0
    topics = Counter()
    identical_sentences = 0

    eng_ratios = []
    guj_ratios = []

    for conversation in data:
        topics[conversation['topic']] += 1
        for message in conversation['conversations']:
            total_sentences += 1
            gujlish_text = message['gujlish']
            english_text = message['english']

            if are_sentences_identical(gujlish_text, english_text):
                identical_sentences += 1
                english_sentences += 1
            else:
                gujlish_sentences += 1

            # Optional: Calculate language mix ratio just for histogram
            words = gujlish_text.split()
            total_words = len(words)
            eng_words = len(re.findall(r'\b[a-zA-Z]+\b', gujlish_text))
            guj_words = total_words - eng_words
            if total_words > 0:
                eng_ratios.append(eng_words / total_words)
                guj_ratios.append(guj_words / total_words)

    avg_eng_ratio = sum(eng_ratios) / len(eng_ratios) if eng_ratios else 0
    avg_guj_ratio = sum(guj_ratios) / len(guj_ratios) if guj_ratios else 0

    return {
        'total_conversations': total_conversations,
        'total_sentences': total_sentences,
        'english_sentences': english_sentences,
        'gujlish_sentences': gujlish_sentences,
        'identical_sentences': identical_sentences,
        'topics': topics,
        'language_mix_stats': list(zip(eng_ratios, guj_ratios)),
        'avg_eng_ratio': avg_eng_ratio,
        'avg_guj_ratio': avg_guj_ratio
    }

def create_visualizations(stats: Dict):
    if not os.path.exists('analysis_plots'):
        os.makedirs('analysis_plots')

    # Sentence Type Distribution
    plt.figure(figsize=(8, 6))
    labels = ['English (Identical)', 'Gujlish (Different)']
    values = [stats['english_sentences'], stats['gujlish_sentences']]
    plt.bar(labels, values, color=['#66b3ff', '#ff9999'])
    plt.title('Sentence Type Distribution')
    plt.ylabel('Number of Sentences')
    plt.savefig('analysis_plots/sentence_distribution.png')
    plt.close()

    # Top Topics
    plt.figure(figsize=(12, 6))
    top_topics = dict(stats['topics'].most_common(10))
    plt.bar(top_topics.keys(), top_topics.values(), color='#ffcc99')
    plt.title('Top 10 Conversation Topics')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('analysis_plots/top_topics.png')
    plt.close()

    # Language Mix Distribution
    plt.figure(figsize=(10, 6))
    eng_ratios = [eng for eng, _ in stats['language_mix_stats']]
    plt.hist(eng_ratios, bins=20, alpha=0.7, label='English Ratio', color='#c2c2f0')
    plt.axvline(stats['avg_eng_ratio'], color='r', linestyle='dashed', linewidth=2, label='Avg English Ratio')
    plt.title('Distribution of English Word Ratio in Gujlish Text')
    plt.xlabel('English Word Ratio')
    plt.ylabel('Number of Sentences')
    plt.legend()
    plt.savefig('analysis_plots/language_mix_distribution.png')
    plt.close()

    # Identical Sentences Pie Chart
    plt.figure(figsize=(6, 6))
    identical = stats['identical_sentences']
    non_identical = stats['total_sentences'] - identical
    plt.pie(
        [identical, non_identical],
        labels=['Identical', 'Different'],
        autopct='%1.1f%%',
        startangle=90,
        colors=['#66b3ff', '#ff9999']
    )
    plt.title('Proportion of Identical Gujlish & English Sentences')
    plt.savefig('analysis_plots/identical_sentences_pie.png')
    plt.close()

def main():
    data = load_data('gujlishConversationalDataset.json')
    stats = analyze_conversations(data)

    print("\n=== Dataset Analysis Results ===")
    print(f"Total Conversations: {stats['total_conversations']}")
    print(f"Total Sentences: {stats['total_sentences']}")
    
    print("\nSentence Type Distribution (Based on Key Comparison):")
    print(f"English Sentences (gujlish == english): {stats['english_sentences']} ({stats['english_sentences']/stats['total_sentences']*100:.2f}%)")
    print(f"Gujlish Sentences (gujlish != english): {stats['gujlish_sentences']} ({stats['gujlish_sentences']/stats['total_sentences']*100:.2f}%)")

    print("\nLanguage Mix Statistics (from Gujlish text only):")
    print(f"Average English Word Ratio: {stats['avg_eng_ratio']*100:.2f}%")
    print(f"Average Gujlish Word Ratio: {stats['avg_guj_ratio']*100:.2f}%")

    print("\nTop 5 Conversation Topics:")
    for topic, count in stats['topics'].most_common(5):
        print(f"- {topic}: {count} conversations")

    print(f"\nIdentical Gujlish-English Sentences: {stats['identical_sentences']}")

    create_visualizations(stats)
    print("\n✅ Visualizations saved in 'analysis_plots' directory.")

if __name__ == "__main__":
    main()
