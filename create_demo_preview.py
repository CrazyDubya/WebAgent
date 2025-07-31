"""
Generate a demo screenshot mockup to show the user what the interface looks like
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch
import numpy as np

# Create figure and axis
fig, ax = plt.subplots(1, 1, figsize=(16, 10))
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis('off')

# Background
background = FancyBboxPatch((0, 0), 100, 100, boxstyle="round,pad=0", 
                           facecolor='#f0f2f6', edgecolor='none')
ax.add_patch(background)

# Header section
header = FancyBboxPatch((5, 85), 90, 12, boxstyle="round,pad=1", 
                       facecolor='#667eea', edgecolor='none')
ax.add_patch(header)
ax.text(50, 91, '🌐 WebAgent Interactive Playground', 
        ha='center', va='center', fontsize=18, color='white', weight='bold')
ax.text(50, 87, 'Explore the Full Capabilities of WebAgent Framework', 
        ha='center', va='center', fontsize=12, color='white')

# Agent cards section
agents = [
    ('🕺 WebDancer', 'Native agentic search reasoning model'),
    ('⛵ WebSailor', 'Super-human reasoning for web navigation'),
    ('🚶 WebWalker', 'Systematic web traversal and benchmarking'),
    ('🎨 WebShaper', 'Data synthesis for information-seeking')
]

card_width = 20
card_height = 15
start_x = 10
start_y = 65

for i, (agent_name, description) in enumerate(agents):
    x = start_x + (i % 2) * 40
    y = start_y - (i // 2) * 20
    
    # Agent card
    card = FancyBboxPatch((x, y), card_width, card_height, 
                         boxstyle="round,pad=1", 
                         facecolor='white', edgecolor='#dee2e6', linewidth=2)
    ax.add_patch(card)
    
    # Agent title
    ax.text(x + card_width/2, y + card_height - 3, agent_name, 
            ha='center', va='center', fontsize=11, weight='bold')
    
    # Agent description
    ax.text(x + card_width/2, y + card_height/2, description, 
            ha='center', va='center', fontsize=8, wrap=True)
    
    # Performance bars (mock)
    bar_y = y + 2
    for j, (metric, value) in enumerate([('Accuracy', 95), ('Speed', 88), ('Complexity', 92)]):
        bar_x = x + 2 + j * 5
        bar_bg = FancyBboxPatch((bar_x, bar_y), 4, 1, 
                               facecolor='#e9ecef', edgecolor='none')
        ax.add_patch(bar_bg)
        
        bar_fill = FancyBboxPatch((bar_x, bar_y), 4 * value/100, 1, 
                                 facecolor='#007bff', edgecolor='none')
        ax.add_patch(bar_fill)

# Demo interface section
demo_section = FancyBboxPatch((5, 10), 60, 35, boxstyle="round,pad=1", 
                             facecolor='white', edgecolor='#dee2e6', linewidth=2)
ax.add_patch(demo_section)

ax.text(35, 40, '🎮 Interactive Demo', ha='center', va='center', 
        fontsize=14, weight='bold')

# Query input mockup
query_box = FancyBboxPatch((8, 30), 54, 5, boxstyle="round,pad=0.5", 
                          facecolor='#f8f9fa', edgecolor='#ced4da')
ax.add_patch(query_box)
ax.text(10, 32.5, '❓ Query: "Compare renewable energy technologies"', 
        ha='left', va='center', fontsize=10)

# Agent selection
ax.text(10, 26, '🤖 Selected Agents: WebDancer, WebSailor', 
        ha='left', va='center', fontsize=10)

# Results mockup
results_box = FancyBboxPatch((8, 15), 54, 10, boxstyle="round,pad=0.5", 
                           facecolor='#e7f3ff', edgecolor='#007bff')
ax.add_patch(results_box)
ax.text(35, 20, '📊 Agent Responses & Comparison', 
        ha='center', va='center', fontsize=12, weight='bold')
ax.text(10, 17, '• WebDancer: Autonomous search and synthesis...', 
        ha='left', va='center', fontsize=9)
ax.text(10, 16, '• WebSailor: Complex reasoning and analysis...', 
        ha='left', va='center', fontsize=9)

# Sidebar mockup
sidebar = FancyBboxPatch((70, 10), 25, 35, boxstyle="round,pad=1", 
                        facecolor='#f8f9fa', edgecolor='#dee2e6', linewidth=2)
ax.add_patch(sidebar)

ax.text(82.5, 40, '⚙️ Configuration', ha='center', va='center', 
        fontsize=12, weight='bold')

# Status indicators
status_items = [
    ('✅ All Agents Ready', '#28a745'),
    ('✅ Demo Mode Active', '#28a745'),
    ('⚠️ Mock Data Mode', '#ffc107')
]

for i, (status, color) in enumerate(status_items):
    ax.text(72, 35 - i*3, status, ha='left', va='center', 
            fontsize=9, color=color)

# Metrics
ax.text(82.5, 23, '📊 Live Metrics', ha='center', va='center', 
        fontsize=11, weight='bold')

metrics = [('Complexity: High', '8 Steps'), ('Domains: 3', '95% Confidence')]
for i, (metric, value) in enumerate(metrics):
    ax.text(72, 19 - i*2, f'{metric}', ha='left', va='center', fontsize=8)
    ax.text(92, 19 - i*2, f'{value}', ha='right', va='center', fontsize=8, weight='bold')

# Footer
ax.text(50, 3, '🚀 Launch with: python launch_demo.py playground', 
        ha='center', va='center', fontsize=12, 
        bbox=dict(boxstyle="round,pad=0.5", facecolor='#e7f3ff', edgecolor='#007bff'))

plt.title('WebAgent Interactive Playground - Demo Interface Preview', 
          fontsize=16, weight='bold', pad=20)

# Save the figure
plt.savefig('/home/runner/work/WebAgent/WebAgent/demo_preview.png', 
            dpi=150, bbox_inches='tight', facecolor='white')
plt.close()

print("Demo preview image created: demo_preview.png")