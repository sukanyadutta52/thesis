"""
Generate Visualizations for Thesis
Quick script to create charts and graphs from analysis results
"""

import json
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import numpy as np

# Configuration
PROJECT_ROOT = Path("D:/Thesis")
RESULTS_DIR = PROJECT_ROOT / "analysis" / "results"
RESULTS_DIR.mkdir(exist_ok=True, parents=True)

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 11

# Data from quick analysis
fashion_data = {
    'strategies': {
        'Fear Triggers': 94,
        'Aspiration Appeals': 67,
        'Emotional Blackmail': 58,
        'Scientific Mimicry': 57,
        'Inadequacy Triggers': 48
    },
    'emotions': {
        'Fear': 59, 'Joy': 53, 'Guilt': 51, 'Pride': 46, 'Hope': 36
    },
    'brands': ['Armani', 'Balenciaga', 'Bottega Veneta', 'Celine', 'Chanel', 
               'Dior', 'Givenchy', 'Hugo Boss', 'Loewe', 'Prada', 'Valentino', 'YSL']
}

fitness_data = {
    'strategies': {
        'Aspiration Appeals': 91,
        'Fear Triggers': 61,
        'Scientific Mimicry': 60,
        'Emotional Blackmail': 55,
        'Social Proof': 46
    },
    'emotions': {
        'Pride': 62, 'Fear': 42, 'Guilt': 38, 'Joy': 38, 'Hope': 34
    },
    'brands': ['AlphAlete', 'Decathlon', 'Gymshark', 'Inov8', 'Merrell', 
               'Mizuno', 'Nike', 'On', 'Patagonia', 'Reebok', 'Rogue', 'Skechers']
}

skincare_data = {
    'strategies': {
        'Scientific Mimicry': 125,
        'Fear Triggers': 93,
        'Aspiration Appeals': 88,
        'Authority Appeals': 87,
        'Inadequacy Triggers': 65
    },
    'emotions': {
        'Fear': 52, 'Pride': 41, 'Hope': 40, 'Joy': 38, 'Shame': 37
    },
    'brands': ['CeraVe', 'Chanel', 'Estée Lauder', 'Eucerin', 'Garnier', 
               'La Mer', 'L\'Oréal', 'Nivea', 'Olay', 'Pixi', 'The Ordinary']
}

def create_strategy_comparison():
    """Create comparison of strategies across sectors"""
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    
    sectors = ['Fashion', 'Fitness', 'Skincare']
    data_sets = [fashion_data, fitness_data, skincare_data]
    colors = ['#e74c3c', '#3498db', '#2ecc71']
    
    for idx, (ax, sector, data, color) in enumerate(zip(axes, sectors, data_sets, colors)):
        strategies = list(data['strategies'].keys())
        values = list(data['strategies'].values())
        
        bars = ax.bar(range(len(strategies)), values, color=color, alpha=0.7)
        ax.set_xticks(range(len(strategies)))
        ax.set_xticklabels(strategies, rotation=45, ha='right')
        ax.set_ylabel('Frequency')
        ax.set_title(f'{sector} Sector - Top Manipulation Strategies', fontweight='bold')
        
        # Add value labels on bars
        for bar, val in zip(bars, values):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(val)}', ha='center', va='bottom')
    
    plt.suptitle('Manipulation Strategies Across Sectors', fontsize=16, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(RESULTS_DIR / 'strategies_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("Saved: strategies_comparison.png")

def create_emotion_wheel():
    """Create emotion distribution wheel"""
    fig, axes = plt.subplots(1, 3, figsize=(18, 6), subplot_kw=dict(projection='polar'))
    
    sectors = ['Fashion', 'Fitness', 'Skincare']
    data_sets = [fashion_data, fitness_data, skincare_data]
    colors_map = {
        'Fear': '#e74c3c', 'Joy': '#f39c12', 'Guilt': '#9b59b6',
        'Pride': '#3498db', 'Hope': '#2ecc71', 'Shame': '#95a5a6'
    }
    
    for ax, sector, data in zip(axes, sectors, data_sets):
        emotions = list(data['emotions'].keys())
        values = list(data['emotions'].values())
        
        # Calculate angles
        angles = np.linspace(0, 2 * np.pi, len(emotions), endpoint=False).tolist()
        values_plot = values + values[:1]  # Complete the circle
        angles += angles[:1]
        
        # Plot
        ax.plot(angles, values_plot, 'o-', linewidth=2, color='#3498db')
        ax.fill(angles, values_plot, alpha=0.25, color='#3498db')
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(emotions)
        ax.set_ylim(0, max(values) * 1.1)
        ax.set_title(f'{sector} Sector', fontweight='bold', pad=20)
        ax.grid(True)
    
    plt.suptitle('Emotion Distribution Across Sectors', fontsize=16, fontweight='bold', y=1.05)
    plt.tight_layout()
    plt.savefig(RESULTS_DIR / 'emotion_wheel.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("Saved: emotion_wheel.png")

def create_cross_sector_heatmap():
    """Create heatmap of all strategies across sectors"""
    import pandas as pd
    
    # Compile all strategies
    all_strategies = set()
    for data in [fashion_data, fitness_data, skincare_data]:
        all_strategies.update(data['strategies'].keys())
    
    # Create matrix
    sectors = ['Fashion', 'Fitness', 'Skincare']
    data_sets = [fashion_data, fitness_data, skincare_data]
    
    matrix = []
    for data in data_sets:
        row = [data['strategies'].get(strategy, 0) for strategy in sorted(all_strategies)]
        matrix.append(row)
    
    # Create heatmap
    fig, ax = plt.subplots(figsize=(12, 6))
    
    im = ax.imshow(matrix, cmap='YlOrRd', aspect='auto')
    
    # Set ticks
    ax.set_xticks(np.arange(len(all_strategies)))
    ax.set_yticks(np.arange(len(sectors)))
    ax.set_xticklabels(sorted(all_strategies), rotation=45, ha='right')
    ax.set_yticklabels(sectors)
    
    # Add colorbar
    plt.colorbar(im, ax=ax, label='Frequency')
    
    # Add text annotations
    for i in range(len(sectors)):
        for j in range(len(all_strategies)):
            text = ax.text(j, i, int(matrix[i][j]),
                          ha="center", va="center", color="black")
    
    ax.set_title('Manipulation Strategy Heatmap Across Sectors', fontweight='bold', pad=20)
    plt.tight_layout()
    plt.savefig(RESULTS_DIR / 'strategy_heatmap.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("Saved: strategy_heatmap.png")

def create_intensity_chart():
    """Create manipulation intensity comparison"""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Calculate total manipulation instances per sector
    sectors = ['Fashion', 'Fitness', 'Skincare']
    totals = [
        sum(fashion_data['strategies'].values()),
        sum(fitness_data['strategies'].values()),
        sum(skincare_data['strategies'].values())
    ]
    
    # Calculate average per brand
    brands_count = [12, 12, 11]
    averages = [t/b for t, b in zip(totals, brands_count)]
    
    x = np.arange(len(sectors))
    width = 0.35
    
    bars1 = ax.bar(x - width/2, totals, width, label='Total Instances', color='#3498db')
    bars2 = ax.bar(x + width/2, averages, width, label='Average per Brand', color='#e74c3c')
    
    ax.set_xlabel('Sector')
    ax.set_ylabel('Count')
    ax.set_title('Manipulation Intensity by Sector', fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(sectors)
    ax.legend()
    
    # Add value labels
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height:.0f}',
                       xy=(bar.get_x() + bar.get_width() / 2, height),
                       xytext=(0, 3),
                       textcoords="offset points",
                       ha='center', va='bottom')
    
    plt.tight_layout()
    plt.savefig(RESULTS_DIR / 'intensity_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("Saved: intensity_comparison.png")

def create_top_brands_chart():
    """Create chart of most manipulative brands"""
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Brand manipulation scores (from analysis)
    brand_scores = {
        'Nivea': 50,
        'Gymshark': 35,
        'Dior': 32,
        'CeraVe': 29,
        'Nike': 28,
        'Celine': 27,
        'Patagonia': 25,
        'The Ordinary': 24,
        'Bottega Veneta': 23,
        'Prada': 22,
        'Chanel (Fashion)': 21,
        'Valentino': 20
    }
    
    brands = list(brand_scores.keys())
    scores = list(brand_scores.values())
    
    # Color by sector
    colors = []
    for brand in brands:
        if brand in ['Nivea', 'CeraVe', 'The Ordinary']:
            colors.append('#2ecc71')  # Skincare
        elif brand in ['Gymshark', 'Nike', 'Patagonia']:
            colors.append('#3498db')  # Fitness
        else:
            colors.append('#e74c3c')  # Fashion
    
    bars = ax.barh(range(len(brands)), scores, color=colors)
    ax.set_yticks(range(len(brands)))
    ax.set_yticklabels(brands)
    ax.set_xlabel('Total Manipulation Instances')
    ax.set_title('Most Manipulative Brands Across All Sectors', fontweight='bold')
    
    # Add value labels
    for bar, score in zip(bars, scores):
        width = bar.get_width()
        ax.text(width, bar.get_y() + bar.get_height()/2.,
               f'{int(score)}', ha='left', va='center', fontweight='bold')
    
    # Add legend
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='#e74c3c', label='Fashion'),
        Patch(facecolor='#3498db', label='Fitness'),
        Patch(facecolor='#2ecc71', label='Skincare')
    ]
    ax.legend(handles=legend_elements, loc='lower right')
    
    plt.tight_layout()
    plt.savefig(RESULTS_DIR / 'top_brands.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("Saved: top_brands.png")

def main():
    """Generate all visualizations"""
    print("Generating visualizations for thesis...")
    print("="*50)
    
    create_strategy_comparison()
    create_emotion_wheel()
    create_cross_sector_heatmap()
    create_intensity_chart()
    create_top_brands_chart()
    
    print("="*50)
    print(f"All visualizations saved to {RESULTS_DIR}")
    print("\nYou can now include these in your LaTeX thesis using:")
    print("\\includegraphics[width=\\textwidth]{analysis/results/filename.png}")

if __name__ == "__main__":
    main()