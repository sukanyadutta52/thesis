"""
Corpus Analysis Script for Marketing Discourse
Master's Thesis: Psychological Manipulation in Marketing Discourse
Author: [Your Name]
Date: January 2025
"""

import os
import pandas as pd
import numpy as np
from pathlib import Path
import nltk
# import spacy  # Optional - commented out for now
from collections import Counter, defaultdict
from textblob import TextBlob
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import re
from typing import List, Dict, Tuple
import json

# Configuration
PROJECT_ROOT = Path("D:/Thesis")
DATA_DIR = PROJECT_ROOT / "docs" / "materials"
RESULTS_DIR = PROJECT_ROOT / "analysis" / "results"
RESULTS_DIR.mkdir(exist_ok=True)

# Initialize spaCy model (download with: python -m spacy download en_core_web_lg)
# nlp = spacy.load("en_core_web_lg")  # Commented out - spacy optional

# Download required NLTK data
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('vader_lexicon', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)

from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize, sent_tokenize

# Set style for visualizations
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)

class MarketingDiscourseAnalyzer:
    """
    Analyzer for marketing discourse focusing on psychological manipulation strategies
    """
    
    def __init__(self, sector: str):
        """
        Initialize analyzer for specific sector
        
        Args:
            sector: One of 'Fashion', 'Fitness', 'Skincare_Cosmetics'
        """
        self.sector = sector
        self.data_path = DATA_DIR / sector
        self.texts = {}
        self.stop_words = set(stopwords.words('english'))
        self.sia = SentimentIntensityAnalyzer()
        
        # Manipulation indicators (can be expanded based on literature)
        self.manipulation_lexicon = {
            'urgency': ['now', 'today', 'limited', 'hurry', 'quick', 'fast', 'immediately', 
                       'last chance', 'ending soon', 'don\'t miss'],
            'scarcity': ['exclusive', 'limited edition', 'rare', 'unique', 'only', 'few left',
                        'selling out', 'almost gone'],
            'authority': ['expert', 'proven', 'scientific', 'clinical', 'dermatologist',
                         'recommended', 'certified', 'award-winning'],
            'social_proof': ['bestseller', 'popular', 'trending', 'everyone', 'thousands',
                           'loved by', 'favorite', 'must-have'],
            'emotion_fear': ['worried', 'concerned', 'damage', 'protect', 'prevent', 'risk',
                            'danger', 'harmful', 'threat'],
            'emotion_aspiration': ['dream', 'perfect', 'ideal', 'transform', 'achieve',
                                 'success', 'luxury', 'elite', 'prestige'],
            'inadequacy': ['problem', 'issue', 'concern', 'flaw', 'imperfection', 'aging',
                          'wrinkles', 'tired', 'dull']
        }
        
    def load_texts(self):
        """Load all text files from the sector directory"""
        for file_path in self.data_path.glob("*.txt"):
            brand_name = file_path.stem
            with open(file_path, 'r', encoding='utf-8') as f:
                self.texts[brand_name] = f.read()
        print(f"Loaded {len(self.texts)} brands from {self.sector} sector")
        
    def preprocess_text(self, text: str) -> List[str]:
        """Basic text preprocessing"""
        # Convert to lowercase
        text = text.lower()
        # Remove special characters but keep spaces
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
        # Tokenize
        tokens = word_tokenize(text)
        # Remove stopwords
        tokens = [token for token in tokens if token not in self.stop_words and len(token) > 2]
        return tokens
    
    def analyze_manipulation_strategies(self, text: str) -> Dict[str, int]:
        """
        Identify manipulation strategies in text
        
        Returns:
            Dictionary with counts of each manipulation strategy
        """
        text_lower = text.lower()
        strategy_counts = {}
        
        for strategy, keywords in self.manipulation_lexicon.items():
            count = sum(1 for keyword in keywords if keyword in text_lower)
            strategy_counts[strategy] = count
            
        return strategy_counts
    
    def sentiment_analysis(self, text: str) -> Dict[str, float]:
        """
        Perform sentiment analysis on text
        
        Returns:
            Dictionary with sentiment scores
        """
        # Using VADER sentiment analyzer
        scores = self.sia.polarity_scores(text)
        
        # Using TextBlob for additional perspective
        blob = TextBlob(text)
        scores['textblob_polarity'] = blob.sentiment.polarity
        scores['textblob_subjectivity'] = blob.sentiment.subjectivity
        
        return scores
    
    def extract_linguistic_features(self, text: str) -> Dict[str, any]:
        """
        Extract various linguistic features from text
        """
        features = {}
        
        try:
            # Basic statistics
            sentences = sent_tokenize(text)
            words = word_tokenize(text)
        except:
            # Fallback if tokenization fails
            sentences = text.split('. ')
            words = text.split()
        
        features['sentence_count'] = len(sentences)
        features['word_count'] = len(words)
        features['avg_sentence_length'] = len(words) / len(sentences) if sentences else 0
        
        # POS tagging for linguistic complexity
        try:
            pos_tags = nltk.pos_tag(words)
            pos_counts = Counter(tag for word, tag in pos_tags)
        except:
            pos_counts = Counter()  # Empty counter if POS tagging fails
        
        features['adjective_count'] = pos_counts.get('JJ', 0) + pos_counts.get('JJR', 0) + pos_counts.get('JJS', 0)
        features['adverb_count'] = pos_counts.get('RB', 0) + pos_counts.get('RBR', 0) + pos_counts.get('RBS', 0)
        features['verb_count'] = sum(count for tag, count in pos_counts.items() if tag.startswith('VB'))
        
        # Exclamation and question marks (emotional intensity)
        features['exclamation_count'] = text.count('!')
        features['question_count'] = text.count('?')
        
        # Personal pronouns (engagement)
        personal_pronouns = ['you', 'your', 'we', 'our', 'us']
        features['personal_pronoun_count'] = sum(1 for word in words if word.lower() in personal_pronouns)
        
        return features
    
    def analyze_brand(self, brand_name: str) -> Dict:
        """
        Comprehensive analysis of a single brand's marketing discourse
        """
        if brand_name not in self.texts:
            raise ValueError(f"Brand {brand_name} not found in loaded texts")
            
        text = self.texts[brand_name]
        
        analysis = {
            'brand': brand_name,
            'sector': self.sector,
            'manipulation_strategies': self.analyze_manipulation_strategies(text),
            'sentiment': self.sentiment_analysis(text),
            'linguistic_features': self.extract_linguistic_features(text)
        }
        
        return analysis
    
    def analyze_all_brands(self) -> pd.DataFrame:
        """
        Analyze all brands in the sector and return results as DataFrame
        """
        results = []
        
        for brand_name in self.texts:
            try:
                analysis = self.analyze_brand(brand_name)
                # Flatten the nested dictionaries for DataFrame
                flat_result = {'brand': brand_name, 'sector': self.sector}
                
                # Add manipulation strategies
                for strategy, count in analysis['manipulation_strategies'].items():
                    flat_result[f'manipulation_{strategy}'] = count
                
                # Add sentiment scores
                for metric, score in analysis['sentiment'].items():
                    flat_result[f'sentiment_{metric}'] = score
                
                # Add linguistic features
                for feature, value in analysis['linguistic_features'].items():
                    flat_result[f'linguistic_{feature}'] = value
                
                results.append(flat_result)
                
            except Exception as e:
                print(f"Error analyzing {brand_name}: {e}")
                
        return pd.DataFrame(results)
    
    def visualize_manipulation_strategies(self, df: pd.DataFrame):
        """
        Create visualizations for manipulation strategies
        """
        # Check if DataFrame is empty
        if df.empty:
            print(f"No data to visualize for {self.sector}")
            return
            
        # Get manipulation columns
        manipulation_cols = [col for col in df.columns if col.startswith('manipulation_')]
        
        if not manipulation_cols:
            print(f"No manipulation columns found for {self.sector}")
            return
        
        # Calculate average use of each strategy
        strategy_means = df[manipulation_cols].mean().sort_values(ascending=False)
        strategy_means.index = [col.replace('manipulation_', '') for col in strategy_means.index]
        
        # Create bar plot
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Average strategy use
        strategy_means.plot(kind='bar', ax=ax1, color='steelblue')
        ax1.set_title(f'Average Manipulation Strategy Use - {self.sector}')
        ax1.set_xlabel('Strategy')
        ax1.set_ylabel('Average Count')
        ax1.tick_params(axis='x', rotation=45)
        
        # Heatmap of strategies by brand
        pivot_data = df.set_index('brand')[manipulation_cols]
        pivot_data.columns = [col.replace('manipulation_', '') for col in pivot_data.columns]
        
        sns.heatmap(pivot_data.T, annot=True, fmt='.0f', cmap='YlOrRd', ax=ax2)
        ax2.set_title(f'Manipulation Strategies by Brand - {self.sector}')
        ax2.set_xlabel('Brand')
        ax2.set_ylabel('Strategy')
        
        plt.tight_layout()
        plt.savefig(RESULTS_DIR / f'{self.sector}_manipulation_strategies.png', dpi=300, bbox_inches='tight')
        plt.show()
        
    def generate_report(self, df: pd.DataFrame):
        """
        Generate a comprehensive report for the sector
        """
        report = f"""
# Marketing Discourse Analysis Report
## Sector: {self.sector}
## Date: {pd.Timestamp.now().strftime('%Y-%m-%d')}

### Summary Statistics
- Total brands analyzed: {len(df)}
- Average word count: {df['linguistic_word_count'].mean():.0f}
- Average sentences: {df['linguistic_sentence_count'].mean():.0f}

### Manipulation Strategies (Average Occurrences)
"""
        manipulation_cols = [col for col in df.columns if col.startswith('manipulation_')]
        for col in manipulation_cols:
            strategy = col.replace('manipulation_', '')
            avg = df[col].mean()
            report += f"- {strategy.title()}: {avg:.2f}\n"
        
        report += f"""
### Sentiment Analysis (Average Scores)
- Positive: {df['sentiment_pos'].mean():.3f}
- Negative: {df['sentiment_neg'].mean():.3f}
- Neutral: {df['sentiment_neu'].mean():.3f}
- Compound: {df['sentiment_compound'].mean():.3f}

### Top 3 Brands by Manipulation Intensity
"""
        df['total_manipulation'] = df[manipulation_cols].sum(axis=1)
        top_brands = df.nlargest(3, 'total_manipulation')[['brand', 'total_manipulation']]
        for _, row in top_brands.iterrows():
            report += f"- {row['brand']}: {row['total_manipulation']:.0f} manipulation indicators\n"
        
        # Save report
        report_path = RESULTS_DIR / f'{self.sector}_analysis_report.md'
        with open(report_path, 'w') as f:
            f.write(report)
        
        print(f"Report saved to {report_path}")
        return report


def main():
    """
    Main analysis pipeline
    """
    sectors = ['Fashion', 'Fitness', 'Skincare_Cosmetics']
    all_results = []
    
    for sector in sectors:
        print(f"\n{'='*50}")
        print(f"Analyzing {sector} Sector")
        print('='*50)
        
        analyzer = MarketingDiscourseAnalyzer(sector)
        
        # Check if data exists
        if not analyzer.data_path.exists():
            print(f"Warning: Data directory {analyzer.data_path} does not exist")
            continue
            
        # Load and analyze
        analyzer.load_texts()
        
        if analyzer.texts:
            df = analyzer.analyze_all_brands()
            all_results.append(df)
            
            # Save sector results
            df.to_csv(RESULTS_DIR / f'{sector}_analysis_results.csv', index=False)
            
            # Generate visualizations
            analyzer.visualize_manipulation_strategies(df)
            
            # Generate report
            analyzer.generate_report(df)
    
    # Combine all sectors for cross-sector analysis
    if all_results:
        combined_df = pd.concat(all_results, ignore_index=True)
        combined_df.to_csv(RESULTS_DIR / 'all_sectors_combined.csv', index=False)
        print(f"\n{'='*50}")
        print("Cross-sector analysis data saved")
        print(f"Total brands analyzed: {len(combined_df)}")
        

if __name__ == "__main__":
    main()