"""
Quick Analysis Script for Thesis Data
Generates initial insights from brand marketing texts
"""

import json
import re
from pathlib import Path
from collections import Counter, defaultdict
import os

# Configuration
PROJECT_ROOT = Path("D:/Thesis")
DATA_DIR = PROJECT_ROOT / "docs" / "materials"
CODING_SCHEME_PATH = PROJECT_ROOT / "analysis" / "coding_scheme.json"
RESULTS_DIR = PROJECT_ROOT / "analysis" / "results"
RESULTS_DIR.mkdir(exist_ok=True, parents=True)

# Load coding scheme
with open(CODING_SCHEME_PATH, 'r', encoding='utf-8') as f:
    coding_scheme = json.load(f)

def analyze_sector(sector_name):
    """Analyze all brands in a sector"""
    sector_path = DATA_DIR / sector_name
    if not sector_path.exists():
        print(f"Sector {sector_name} not found")
        return None
    
    print(f"\nAnalyzing {sector_name} Sector")
    print("="*50)
    
    results = {}
    manipulation_categories = coding_scheme['manipulation_categories']
    emotion_categories = coding_scheme['emotion_categories']
    
    # Process each brand
    for file_path in sector_path.glob("*.txt"):
        brand_name = file_path.stem
        
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            text = f.read().lower()
        
        # Count manipulation strategies
        brand_manipulation = {}
        for category, details in manipulation_categories.items():
            keywords = details['keywords']
            count = sum(1 for keyword in keywords if keyword in text)
            brand_manipulation[category] = count
        
        # Count emotion markers
        brand_emotions = {}
        for emotion, details in emotion_categories.items():
            markers = details['linguistic_markers']
            count = sum(1 for marker in markers if marker in text)
            brand_emotions[emotion] = count
        
        results[brand_name] = {
            'text_length': len(text),
            'manipulation': brand_manipulation,
            'emotions': brand_emotions,
            'top_manipulation': max(brand_manipulation, key=brand_manipulation.get),
            'top_emotion': max(brand_emotions, key=brand_emotions.get) if any(brand_emotions.values()) else 'neutral'
        }
    
    return results

def generate_sector_report(sector_name, results):
    """Generate a report for sector analysis"""
    if not results:
        return
    
    report = f"\n{sector_name} SECTOR ANALYSIS\n"
    report += "="*60 + "\n\n"
    
    # Summary statistics
    report += f"Brands analyzed: {len(results)}\n"
    report += f"Average text length: {sum(r['text_length'] for r in results.values()) / len(results):.0f} characters\n\n"
    
    # Top manipulation strategies
    all_manipulations = defaultdict(int)
    for brand_data in results.values():
        for strategy, count in brand_data['manipulation'].items():
            all_manipulations[strategy] += count
    
    report += "TOP MANIPULATION STRATEGIES:\n"
    for strategy, count in sorted(all_manipulations.items(), key=lambda x: x[1], reverse=True)[:5]:
        report += f"  - {strategy.replace('_', ' ').title()}: {count} occurrences\n"
    
    # Top emotions
    all_emotions = defaultdict(int)
    for brand_data in results.values():
        for emotion, count in brand_data['emotions'].items():
            all_emotions[emotion] += count
    
    report += "\nTOP EMOTIONS DETECTED:\n"
    for emotion, count in sorted(all_emotions.items(), key=lambda x: x[1], reverse=True)[:5]:
        report += f"  - {emotion.title()}: {count} markers\n"
    
    # Brand profiles
    report += "\nBRAND PROFILES:\n"
    for brand, data in sorted(results.items()):
        report += f"\n{brand.upper()}:\n"
        report += f"  Text length: {data['text_length']} chars\n"
        report += f"  Dominant strategy: {data['top_manipulation'].replace('_', ' ').title()}\n"
        report += f"  Dominant emotion: {data['top_emotion'].title()}\n"
        
        # Top 3 manipulation tactics for this brand
        top_tactics = sorted(data['manipulation'].items(), key=lambda x: x[1], reverse=True)[:3]
        report += "  Top tactics:\n"
        for tactic, count in top_tactics:
            if count > 0:
                report += f"    - {tactic.replace('_', ' ').title()}: {count}\n"
    
    return report

def main():
    """Main analysis pipeline"""
    sectors = ['Fashion', 'Fitness', 'Skincare_Cosmetics']
    all_reports = []
    
    for sector in sectors:
        results = analyze_sector(sector)
        if results:
            report = generate_sector_report(sector, results)
            all_reports.append(report)
            print(report)
            
            # Save sector results
            output_file = RESULTS_DIR / f"{sector}_quick_analysis.txt"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"Report saved to {output_file}")
    
    # Save combined report
    if all_reports:
        combined_report = "\nCOMBINED ANALYSIS REPORT\n" + "="*60 + "\n"
        combined_report += "\n".join(all_reports)
        
        combined_file = RESULTS_DIR / "all_sectors_quick_analysis.txt"
        with open(combined_file, 'w', encoding='utf-8') as f:
            f.write(combined_report)
        print(f"\nCombined report saved to {combined_file}")
    
    print("\nAnalysis complete!")

if __name__ == "__main__":
    main()