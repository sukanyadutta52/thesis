"""
Enhanced Emotion and Manipulation Analysis Script
Master's Thesis: Psychological Manipulation in Marketing Discourse
Author: [Your Name]
Date: January 2025

This script implements the emotion-based manipulation detection framework
based on the research synthesis and coding scheme.
"""

import json
import os
import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import pandas as pd
import numpy as np
from collections import Counter, defaultdict
import matplotlib.pyplot as plt
import seaborn as sns
from textblob import TextBlob
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords

# Try to import transformer models (optional for advanced analysis)
try:
    from transformers import pipeline
    from sentence_transformers import SentenceTransformer
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    print("Transformers not available. Using basic analysis only.")

# Configuration
PROJECT_ROOT = Path("D:/Thesis")
DATA_DIR = PROJECT_ROOT / "docs" / "materials"
CODING_SCHEME_PATH = PROJECT_ROOT / "analysis" / "coding_scheme.json"
RESULTS_DIR = PROJECT_ROOT / "analysis" / "results"
RESULTS_DIR.mkdir(exist_ok=True, parents=True)

# Download required NLTK data
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('vader_lexicon', quiet=True)
from nltk.sentiment.vader import SentimentIntensityAnalyzer

class EmotionManipulationAnalyzer:
    """
    Advanced analyzer for emotion-based manipulation strategies in marketing discourse
    """
    
    def __init__(self, sector: str):
        """
        Initialize analyzer with coding scheme and sector-specific settings
        
        Args:
            sector: One of 'Fashion', 'Fitness', 'Skincare_Cosmetics'
        """
        self.sector = sector
        self.data_path = DATA_DIR / sector
        self.texts = {}
        
        # Load coding scheme
        with open(CODING_SCHEME_PATH, 'r', encoding='utf-8') as f:
            self.coding_scheme = json.load(f)
        
        # Initialize sentiment analyzer
        self.sia = SentimentIntensityAnalyzer()
        self.stop_words = set(stopwords.words('english'))
        
        # Initialize transformer models if available
        if TRANSFORMERS_AVAILABLE:
            print("Loading transformer models...")
            self.emotion_classifier = pipeline(
                "text-classification", 
                model="j-hartmann/emotion-english-distilroberta-base",
                return_all_scores=True
            )
            self.sentence_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Extract manipulation categories and emotions
        self.manipulation_categories = self.coding_scheme['manipulation_categories']
        self.emotion_categories = self.coding_scheme['emotion_categories']
        self.sector_patterns = self.coding_scheme['sector_specific_patterns'].get(
            sector.lower().replace('_cosmetics', ''), {}
        )
        
    def load_texts(self):
        """Load all text files from the sector directory"""
        for file_path in self.data_path.glob("*.txt"):
            brand_name = file_path.stem
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                self.texts[brand_name] = f.read()
        print(f"Loaded {len(self.texts)} brands from {self.sector} sector")
        
    def detect_manipulation_strategies(self, text: str) -> Dict[str, Dict]:
        """
        Detect manipulation strategies based on coding scheme
        
        Returns:
            Dictionary with detailed manipulation analysis
        """
        text_lower = text.lower()
        results = {}
        
        for category, details in self.manipulation_categories.items():
            keywords = details['keywords']
            weight = details['intensity_weight']
            
            # Count keyword occurrences
            matches = []
            for keyword in keywords:
                if keyword in text_lower:
                    # Find all occurrences with context
                    pattern = re.compile(
                        r'.{0,30}' + re.escape(keyword) + r'.{0,30}',
                        re.IGNORECASE
                    )
                    contexts = pattern.findall(text)
                    matches.extend([(keyword, context) for context in contexts])
            
            results[category] = {
                'count': len(matches),
                'unique_keywords': len(set([m[0] for m in matches])),
                'intensity_weight': weight,
                'weighted_score': len(matches) * weight,
                'examples': matches[:3] if matches else []  # Store first 3 examples
            }
            
        return results
    
    def analyze_emotions(self, text: str) -> Dict[str, any]:
        """
        Comprehensive emotion analysis using multiple methods
        
        Returns:
            Dictionary with emotion scores and classifications
        """
        results = {
            'vader_sentiment': {},
            'textblob_sentiment': {},
            'emotion_keywords': {},
            'transformer_emotions': {}
        }
        
        # VADER sentiment analysis
        vader_scores = self.sia.polarity_scores(text)
        results['vader_sentiment'] = vader_scores
        
        # TextBlob sentiment
        blob = TextBlob(text)
        results['textblob_sentiment'] = {
            'polarity': blob.sentiment.polarity,
            'subjectivity': blob.sentiment.subjectivity
        }
        
        # Emotion keyword detection based on coding scheme
        text_lower = text.lower()
        for emotion, details in self.emotion_categories.items():
            markers = details['linguistic_markers']
            intensity_indicators = details['intensity_indicators']
            
            marker_count = sum(1 for marker in markers if marker in text_lower)
            intensity_count = sum(1 for indicator in intensity_indicators if indicator in text_lower)
            
            results['emotion_keywords'][emotion] = {
                'marker_count': marker_count,
                'intensity_count': intensity_count,
                'total_score': marker_count + (intensity_count * 1.5)  # Weight intensity higher
            }
        
        # Transformer-based emotion classification if available
        if TRANSFORMERS_AVAILABLE:
            # Split text into chunks if too long
            max_length = 512
            chunks = [text[i:i+max_length] for i in range(0, len(text), max_length)]
            
            all_emotions = defaultdict(list)
            for chunk in chunks[:5]:  # Analyze first 5 chunks max
                emotions = self.emotion_classifier(chunk)[0]
                for emotion_dict in emotions:
                    all_emotions[emotion_dict['label']].append(emotion_dict['score'])
            
            # Average scores across chunks
            results['transformer_emotions'] = {
                emotion: np.mean(scores) 
                for emotion, scores in all_emotions.items()
            }
        
        return results
    
    def calculate_manipulation_intensity(self, manipulation_results: Dict) -> float:
        """
        Calculate overall manipulation intensity score
        
        Returns:
            Normalized intensity score (0-1)
        """
        total_weighted_score = sum(
            cat['weighted_score'] for cat in manipulation_results.values()
        )
        
        # Normalize based on text length (rough approximation)
        max_expected_score = 50  # Adjust based on empirical observation
        intensity = min(total_weighted_score / max_expected_score, 1.0)
        
        return intensity
    
    def identify_sector_patterns(self, text: str) -> Dict[str, int]:
        """
        Identify sector-specific patterns
        
        Returns:
            Count of sector-specific markers
        """
        if not self.sector_patterns:
            return {}
        
        text_lower = text.lower()
        unique_markers = self.sector_patterns.get('unique_markers', [])
        
        marker_counts = {}
        for marker in unique_markers:
            marker_counts[marker] = text_lower.count(marker)
            
        return marker_counts
    
    def analyze_brand_comprehensive(self, brand_name: str) -> Dict:
        """
        Comprehensive analysis of a single brand's marketing discourse
        
        Returns:
            Complete analysis results for the brand
        """
        if brand_name not in self.texts:
            raise ValueError(f"Brand {brand_name} not found")
            
        text = self.texts[brand_name]
        
        # Core analyses
        manipulation_strategies = self.detect_manipulation_strategies(text)
        emotion_analysis = self.analyze_emotions(text)
        manipulation_intensity = self.calculate_manipulation_intensity(manipulation_strategies)
        sector_patterns = self.identify_sector_patterns(text)
        
        # Linguistic features
        sentences = sent_tokenize(text)
        words = word_tokenize(text.lower())
        
        # Compile results
        analysis = {
            'brand': brand_name,
            'sector': self.sector,
            'text_statistics': {
                'total_words': len(words),
                'total_sentences': len(sentences),
                'avg_sentence_length': len(words) / len(sentences) if sentences else 0
            },
            'manipulation_strategies': manipulation_strategies,
            'emotion_analysis': emotion_analysis,
            'manipulation_intensity': manipulation_intensity,
            'sector_specific_patterns': sector_patterns,
            'dominant_strategy': max(
                manipulation_strategies.keys(),
                key=lambda k: manipulation_strategies[k]['weighted_score']
            ),
            'dominant_emotion': max(
                emotion_analysis['emotion_keywords'].keys(),
                key=lambda k: emotion_analysis['emotion_keywords'][k]['total_score']
            ) if emotion_analysis['emotion_keywords'] else None
        }
        
        return analysis
    
    def analyze_all_brands(self) -> pd.DataFrame:
        """
        Analyze all brands and compile results into DataFrame
        
        Returns:
            DataFrame with comprehensive analysis results
        """
        all_results = []
        
        for brand_name in self.texts:
            try:
                print(f"Analyzing {brand_name}...")
                analysis = self.analyze_brand_comprehensive(brand_name)
                
                # Flatten results for DataFrame
                flat_result = {
                    'brand': brand_name,
                    'sector': self.sector,
                    'word_count': analysis['text_statistics']['total_words'],
                    'sentence_count': analysis['text_statistics']['total_sentences'],
                    'avg_sentence_length': analysis['text_statistics']['avg_sentence_length'],
                    'manipulation_intensity': analysis['manipulation_intensity'],
                    'dominant_strategy': analysis['dominant_strategy'],
                    'dominant_emotion': analysis['dominant_emotion']
                }
                
                # Add manipulation strategy counts
                for strategy, details in analysis['manipulation_strategies'].items():
                    flat_result[f'strat_{strategy}'] = details['count']
                    flat_result[f'strat_{strategy}_weighted'] = details['weighted_score']
                
                # Add emotion scores
                for emotion, scores in analysis['emotion_analysis']['emotion_keywords'].items():
                    flat_result[f'emotion_{emotion}'] = scores['total_score']
                
                # Add sentiment scores
                flat_result['vader_compound'] = analysis['emotion_analysis']['vader_sentiment']['compound']
                flat_result['textblob_polarity'] = analysis['emotion_analysis']['textblob_sentiment']['polarity']
                flat_result['textblob_subjectivity'] = analysis['emotion_analysis']['textblob_sentiment']['subjectivity']
                
                all_results.append(flat_result)
                
            except Exception as e:
                print(f"Error analyzing {brand_name}: {e}")
                
        return pd.DataFrame(all_results)
    
    def visualize_manipulation_profile(self, df: pd.DataFrame):
        """
        Create comprehensive visualizations of manipulation profiles
        """
        fig = plt.figure(figsize=(20, 12))
        
        # 1. Manipulation Strategy Heatmap
        ax1 = plt.subplot(2, 3, 1)
        strategy_cols = [col for col in df.columns if col.startswith('strat_') and not col.endswith('_weighted')]
        strategy_data = df.set_index('brand')[strategy_cols]
        strategy_data.columns = [col.replace('strat_', '') for col in strategy_data.columns]
        
        sns.heatmap(strategy_data.T, annot=True, fmt='.0f', cmap='YlOrRd', ax=ax1, cbar_kws={'label': 'Count'})
        ax1.set_title(f'Manipulation Strategies - {self.sector}', fontsize=12, fontweight='bold')
        ax1.set_xlabel('Brand')
        ax1.set_ylabel('Strategy')
        
        # 2. Emotion Distribution
        ax2 = plt.subplot(2, 3, 2)
        emotion_cols = [col for col in df.columns if col.startswith('emotion_')]
        emotion_data = df[emotion_cols].mean()
        emotion_data.index = [idx.replace('emotion_', '') for idx in emotion_data.index]
        
        emotion_data.plot(kind='bar', ax=ax2, color='steelblue')
        ax2.set_title(f'Average Emotion Scores - {self.sector}', fontsize=12, fontweight='bold')
        ax2.set_xlabel('Emotion')
        ax2.set_ylabel('Average Score')
        ax2.tick_params(axis='x', rotation=45)
        
        # 3. Manipulation Intensity by Brand
        ax3 = plt.subplot(2, 3, 3)
        intensity_data = df.set_index('brand')['manipulation_intensity'].sort_values(ascending=False)
        
        colors = ['red' if x > 0.66 else 'orange' if x > 0.33 else 'green' for x in intensity_data.values]
        intensity_data.plot(kind='barh', ax=ax3, color=colors)
        ax3.set_title(f'Manipulation Intensity - {self.sector}', fontsize=12, fontweight='bold')
        ax3.set_xlabel('Intensity Score')
        ax3.set_ylabel('Brand')
        
        # 4. Sentiment Distribution
        ax4 = plt.subplot(2, 3, 4)
        df[['vader_compound', 'textblob_polarity']].boxplot(ax=ax4)
        ax4.set_title(f'Sentiment Distribution - {self.sector}', fontsize=12, fontweight='bold')
        ax4.set_ylabel('Sentiment Score')
        
        # 5. Strategy vs Emotion Correlation
        ax5 = plt.subplot(2, 3, 5)
        dominant_strategies = df['dominant_strategy'].value_counts()
        dominant_strategies.plot(kind='pie', ax=ax5, autopct='%1.1f%%')
        ax5.set_title(f'Dominant Strategies - {self.sector}', fontsize=12, fontweight='bold')
        ax5.set_ylabel('')
        
        # 6. Text Complexity
        ax6 = plt.subplot(2, 3, 6)
        df.plot.scatter(x='word_count', y='avg_sentence_length', ax=ax6, s=50)
        for idx, row in df.iterrows():
            ax6.annotate(row['brand'], (row['word_count'], row['avg_sentence_length']),
                        fontsize=8, alpha=0.7)
        ax6.set_title(f'Text Complexity - {self.sector}', fontsize=12, fontweight='bold')
        ax6.set_xlabel('Word Count')
        ax6.set_ylabel('Avg Sentence Length')
        
        plt.suptitle(f'Manipulation Analysis Dashboard - {self.sector} Sector', 
                     fontsize=16, fontweight='bold', y=1.02)
        plt.tight_layout()
        
        # Save figure
        output_path = RESULTS_DIR / f'{self.sector}_manipulation_dashboard.png'
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.show()
        
        print(f"Dashboard saved to {output_path}")
    
    def generate_detailed_report(self, df: pd.DataFrame) -> str:
        """
        Generate a detailed analytical report
        """
        report = f"""
# Emotion-Based Manipulation Analysis Report
## Sector: {self.sector}
## Analysis Date: {pd.Timestamp.now().strftime('%Y-%m-%d')}

---

## Executive Summary

### Corpus Statistics
- **Total Brands Analyzed:** {len(df)}
- **Average Text Length:** {df['word_count'].mean():.0f} words
- **Average Sentences:** {df['sentence_count'].mean():.0f}
- **Average Sentence Complexity:** {df['avg_sentence_length'].mean():.1f} words/sentence

### Manipulation Intensity
- **High Intensity (>0.66):** {len(df[df['manipulation_intensity'] > 0.66])} brands
- **Medium Intensity (0.33-0.66):** {len(df[(df['manipulation_intensity'] > 0.33) & (df['manipulation_intensity'] <= 0.66)])} brands
- **Low Intensity (<0.33):** {len(df[df['manipulation_intensity'] <= 0.33])} brands
- **Average Intensity:** {df['manipulation_intensity'].mean():.3f}

---

## Top Manipulation Strategies

### Most Frequently Used Strategies
"""
        # Calculate strategy usage
        strategy_cols = [col for col in df.columns if col.startswith('strat_') and not col.endswith('_weighted')]
        strategy_sums = df[strategy_cols].sum().sort_values(ascending=False)
        
        for i, (strategy, count) in enumerate(strategy_sums.head(5).items(), 1):
            strategy_name = strategy.replace('strat_', '')
            avg_per_brand = count / len(df)
            report += f"{i}. **{strategy_name.replace('_', ' ').title()}**: {count:.0f} total occurrences ({avg_per_brand:.1f} per brand)\n"
        
        report += """
### Dominant Strategies by Brand
"""
        dominant_counts = df['dominant_strategy'].value_counts()
        for strategy, count in dominant_counts.items():
            report += f"- **{strategy.replace('_', ' ').title()}**: {count} brands\n"
        
        report += """
---

## Emotion Analysis

### Primary Emotions Detected
"""
        emotion_cols = [col for col in df.columns if col.startswith('emotion_')]
        emotion_means = df[emotion_cols].mean().sort_values(ascending=False)
        
        for emotion, score in emotion_means.head(5).items():
            emotion_name = emotion.replace('emotion_', '')
            report += f"- **{emotion_name.title()}**: Average score {score:.2f}\n"
        
        report += """
### Sentiment Analysis
"""
        report += f"- **Average VADER Compound Score:** {df['vader_compound'].mean():.3f}\n"
        report += f"- **Average TextBlob Polarity:** {df['textblob_polarity'].mean():.3f}\n"
        report += f"- **Average TextBlob Subjectivity:** {df['textblob_subjectivity'].mean():.3f}\n"
        
        report += """
---

## Brand-Specific Insights

### Top 3 Most Manipulative Brands
"""
        top_manipulative = df.nlargest(3, 'manipulation_intensity')
        for idx, (_, row) in enumerate(top_manipulative.iterrows(), 1):
            report += f"""
{idx}. **{row['brand']}**
   - Manipulation Intensity: {row['manipulation_intensity']:.3f}
   - Dominant Strategy: {row['dominant_strategy'].replace('_', ' ').title()}
   - Dominant Emotion: {row['dominant_emotion'].title() if row['dominant_emotion'] else 'N/A'}
"""
        
        report += """
### Most Ethical Brands (Lowest Manipulation)
"""
        least_manipulative = df.nsmallest(3, 'manipulation_intensity')
        for idx, (_, row) in enumerate(least_manipulative.iterrows(), 1):
            report += f"""
{idx}. **{row['brand']}**
   - Manipulation Intensity: {row['manipulation_intensity']:.3f}
   - Dominant Strategy: {row['dominant_strategy'].replace('_', ' ').title()}
   - Dominant Emotion: {row['dominant_emotion'].title() if row['dominant_emotion'] else 'N/A'}
"""
        
        report += """
---

## Sector-Specific Patterns

"""
        if self.sector_patterns:
            report += f"### Expected Patterns for {self.sector}\n"
            report += f"- **Dominant Strategies:** {', '.join(self.sector_patterns.get('dominant_strategies', []))}\n"
            report += f"- **Common Emotions:** {', '.join(self.sector_patterns.get('common_emotions', []))}\n"
        
        report += """
---

## Recommendations

### For Consumers
1. Be aware of common manipulation strategies in this sector
2. Recognize emotional triggers in marketing messages
3. Practice critical evaluation of product claims

### For Regulators
1. Monitor high-intensity manipulation brands
2. Develop guidelines for ethical marketing practices
3. Require transparency in emotional manipulation tactics

### For Brands
1. Consider ethical alternatives to manipulation
2. Focus on genuine value communication
3. Build trust through transparency

---

*This report was generated using automated discourse analysis techniques. 
Results should be validated through manual review for critical applications.*
"""
        
        # Save report
        report_path = RESULTS_DIR / f'{self.sector}_detailed_report.md'
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"Detailed report saved to {report_path}")
        return report


def main():
    """
    Main execution pipeline for emotion-based manipulation analysis
    """
    sectors = ['Fashion', 'Fitness', 'Skincare_Cosmetics']
    all_sector_results = []
    
    for sector in sectors:
        print(f"\n{'='*60}")
        print(f"Analyzing {sector} Sector")
        print('='*60)
        
        # Initialize analyzer
        analyzer = EmotionManipulationAnalyzer(sector)
        
        # Check if data exists
        if not analyzer.data_path.exists():
            print(f"Warning: Data directory {analyzer.data_path} does not exist")
            continue
        
        # Load and analyze
        analyzer.load_texts()
        
        if analyzer.texts:
            # Perform analysis
            df = analyzer.analyze_all_brands()
            
            # Save raw results
            output_file = RESULTS_DIR / f'{sector}_emotion_manipulation_results.csv'
            df.to_csv(output_file, index=False)
            print(f"Results saved to {output_file}")
            
            # Generate visualizations
            analyzer.visualize_manipulation_profile(df)
            
            # Generate detailed report
            analyzer.generate_detailed_report(df)
            
            # Store for cross-sector analysis
            all_sector_results.append(df)
    
    # Cross-sector comparison
    if all_sector_results:
        print(f"\n{'='*60}")
        print("Generating Cross-Sector Comparison")
        print('='*60)
        
        combined_df = pd.concat(all_sector_results, ignore_index=True)
        
        # Create cross-sector visualization
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # Manipulation intensity by sector
        ax1 = axes[0, 0]
        combined_df.boxplot(column='manipulation_intensity', by='sector', ax=ax1)
        ax1.set_title('Manipulation Intensity Across Sectors')
        ax1.set_xlabel('Sector')
        ax1.set_ylabel('Intensity Score')
        plt.sca(ax1)
        plt.xticks(rotation=45)
        
        # Dominant strategies by sector
        ax2 = axes[0, 1]
        strategy_sector = combined_df.groupby(['sector', 'dominant_strategy']).size().unstack(fill_value=0)
        strategy_sector.T.plot(kind='bar', stacked=True, ax=ax2)
        ax2.set_title('Dominant Strategies by Sector')
        ax2.set_xlabel('Strategy')
        ax2.set_ylabel('Count')
        ax2.legend(title='Sector')
        plt.sca(ax2)
        plt.xticks(rotation=45)
        
        # Emotion distribution by sector
        ax3 = axes[1, 0]
        emotion_cols = [col for col in combined_df.columns if col.startswith('emotion_')]
        emotion_by_sector = combined_df.groupby('sector')[emotion_cols].mean()
        emotion_by_sector.T.plot(kind='bar', ax=ax3)
        ax3.set_title('Average Emotion Scores by Sector')
        ax3.set_xlabel('Emotion')
        ax3.set_ylabel('Average Score')
        ax3.legend(title='Sector')
        plt.sca(ax3)
        plt.xticks(rotation=45)
        
        # Sentiment comparison
        ax4 = axes[1, 1]
        sentiment_by_sector = combined_df.groupby('sector')[['vader_compound', 'textblob_polarity']].mean()
        sentiment_by_sector.plot(kind='bar', ax=ax4)
        ax4.set_title('Average Sentiment by Sector')
        ax4.set_xlabel('Sector')
        ax4.set_ylabel('Sentiment Score')
        ax4.legend(['VADER Compound', 'TextBlob Polarity'])
        plt.sca(ax4)
        plt.xticks(rotation=45)
        
        plt.suptitle('Cross-Sector Manipulation Analysis', fontsize=16, fontweight='bold')
        plt.tight_layout()
        
        # Save cross-sector visualization
        cross_sector_path = RESULTS_DIR / 'cross_sector_comparison.png'
        plt.savefig(cross_sector_path, dpi=300, bbox_inches='tight')
        plt.show()
        
        # Save combined results
        combined_df.to_csv(RESULTS_DIR / 'all_sectors_emotion_manipulation.csv', index=False)
        print(f"Cross-sector analysis complete. Results saved to {RESULTS_DIR}")


if __name__ == "__main__":
    main()