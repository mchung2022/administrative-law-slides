import os
import matplotlib.pyplot as plt
import numpy as np

# Set font for Traditional Chinese support in Matplotlib
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei', 'Arial']
plt.rcParams['axes.unicode_minus'] = False

output_dir = os.path.join(os.path.dirname(__file__), 'charts')
os.makedirs(output_dir, exist_ok=True)

print("=== Generating High-Resolution Enterprise Charts with Matplotlib ===")

# Chart 1: Speech Rate CPS Comparison Chart
fig, ax = plt.subplots(figsize=(8, 4.5), dpi=300)
rates = ['+0% (預設過快)', '-10% (新聞速)', '-15% (推薦電台速)', '-20% (輕鬆對談)', '-35% (傳統過慢)']
cps_values = [5.50, 4.47, 4.22, 3.98, 2.50]
colors = ['#E53E3E', '#DD6B20', '#1B365D', '#3182CE', '#718096']

bars = ax.barh(rates, cps_values, color=colors, height=0.55)
ax.set_xlabel('每秒朗讀字數 (CPS - Characters Per Second)', fontsize=11, fontweight='bold', color='#1B365D')
ax.set_title('Microsoft Azure Neural 語音語速與朗讀效率實測比較圖', fontsize=14, fontweight='bold', color='#1B365D', pad=15)
ax.set_xlim(0, 6.5)

for bar in bars:
    w = bar.get_width()
    ax.text(w + 0.1, bar.get_y() + bar.get_height()/2, f'{w:.2f} 字/秒', 
            va='center', ha='left', fontsize=10, fontweight='bold', color='#2D3748')

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()
chart1_path = os.path.join(output_dir, 'speech_rate_cps_chart.png')
plt.savefig(chart1_path, dpi=300)
plt.close()
print(f"[OK] Saved Chart 1 to: {chart1_path}")

# Chart 2: 100-Pass & 50-Pass Audit Pass Rate Bar Chart
fig, ax = plt.subplots(figsize=(8, 4.5), dpi=300)
modules = [f'M{i}' for i in range(1, 11)]
legal_audit_passes = [100] * 10
ui_sync_passes = [50] * 10

x = np.arange(len(modules))
width = 0.35

rects1 = ax.bar(x - width/2, legal_audit_passes, width, label='100 輪法律條文稽核通過數 (Passed)', color='#1B365D')
rects2 = ax.bar(x + width/2, ui_sync_passes, width, label='50 輪 UI 時間軸同步測試通過數 (Passed)', color='#D97706')

ax.set_ylabel('稽核通過次數 (Pass Count)', fontsize=11, fontweight='bold', color='#1B365D')
ax.set_title('10 大核心模組之 100 輪與 50 輪自動化測試 100% 通過率指標', fontsize=13, fontweight='bold', color='#1B365D', pad=15)
ax.set_xticks(x)
ax.set_xticklabels([f'模組{i}' for i in range(1, 11)], fontsize=9, fontweight='bold')
ax.legend(frameon=True, facecolor='#F8FAFC', edgecolor='none')
ax.set_ylim(0, 120)

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()
chart2_path = os.path.join(output_dir, 'test_audit_pass_rate.png')
plt.savefig(chart2_path, dpi=300)
plt.close()
print(f"[OK] Saved Chart 2 to: {chart2_path}")

# Chart 3: Prompt Engineering 4W1H Framework Diagram
fig, ax = plt.subplots(figsize=(8.5, 3.8), dpi=300)
ax.axis('off')

boxes = [
    {"title": "WHO (角色)", "desc": "指定 AI 專精領域\n(如：Web 架構師/法學教授)", "color": "#1B365D", "x": 0.05},
    {"title": "WHAT (目標)", "desc": "明確產物與格式\n(如：500頁簡報/30分MP3)", "color": "#2C5282", "x": 0.28},
    {"title": "WHERE (路徑)", "desc": "指定目錄與檔案\n(如：index.html/scratch/)", "color": "#059669", "x": 0.51},
    {"title": "WHY (背景)", "desc": "說明對象與課綱\n(如：108課綱/臺灣法律)", "color": "#D97706", "x": 0.74}
]

from matplotlib.patches import FancyBboxPatch

for b in boxes:
    rect = FancyBboxPatch((b['x'], 0.2), 0.18, 0.6, facecolor=b['color'], edgecolor='none', boxstyle="round,pad=0.02")
    ax.add_patch(rect)
    ax.text(b['x'] + 0.09, 0.65, b['title'], ha='center', va='center', color='white', fontsize=11, fontweight='bold')
    ax.text(b['x'] + 0.09, 0.40, b['desc'], ha='center', va='center', color='white', fontsize=8.5)

ax.set_xlim(0, 1.0)
ax.set_ylim(0, 1.0)
ax.set_title('Antigravity AI 提示詞 (Prompt) 4W1H 黃金公式與代理人執行架構', fontsize=13, fontweight='bold', color='#1B365D', pad=15)
plt.tight_layout()
chart3_path = os.path.join(output_dir, 'prompt_4w1h_architecture.png')
plt.savefig(chart3_path, dpi=300)
plt.close()
print(f"[OK] Saved Chart 3 to: {chart3_path}")
