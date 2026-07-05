import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Set Chinese font
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei', 'Microsoft YaHei', 'Arial']
plt.rcParams['axes.unicode_minus'] = False

output_dir = os.path.join(os.path.dirname(__file__), 'charts')
os.makedirs(output_dir, exist_ok=True)

print("=== Generating High-Resolution Administrative Law Diagrams ===")

# Chart 1: Legal Source Pyramid
def generate_legal_pyramid():
    fig, ax = plt.subplots(figsize=(8, 6), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    layers = [
        ("一、憲法 (最高位階 / 國家根本大法)", 8.5, 9.5, "#4f46e5", "#ffffff"),
        ("二、法律 (立法院三讀通過 / 總統公布)", 6.5, 8.2, "#2563eb", "#ffffff"),
        ("三、行政命令 (法規命令 & 行政規則)", 4.5, 6.2, "#0284c7", "#ffffff"),
        ("四、自治條例與自治規則 (地方自治團體)", 2.5, 4.2, "#0d9488", "#ffffff"),
        ("五、一般法律原則 (習慣法 / 法理 / 憲判字)", 0.5, 2.2, "#059669", "#ffffff")
    ]
    
    for i, (text, y_bottom, y_top, color, text_color) in enumerate(layers):
        width_bottom = 2 + (i + 1) * 1.5
        width_top = 2 + i * 1.5
        x_left_bottom = 5 - width_bottom / 2
        x_left_top = 5 - width_top / 2
        
        polygon = patches.Polygon([
            (x_left_bottom, y_bottom),
            (5 + width_bottom / 2, y_bottom),
            (5 + width_top / 2, y_top),
            (x_left_top, y_top)
        ], closed=True, facecolor=color, edgecolor='#ffffff', linewidth=2, alpha=0.95)
        ax.add_patch(polygon)
        
        y_center = (y_bottom + y_top) / 2
        ax.text(5, y_center, text, color=text_color, fontsize=12, fontweight='bold', ha='center', va='center')
        
    ax.set_title("【行政法成文法源位階金字塔與效力體系】", fontsize=15, fontweight='bold', pad=20, color='#1e293b')
    plt.tight_layout()
    path = os.path.join(output_dir, 'chart_legal_pyramid.png')
    plt.savefig(path, bbox_inches='tight')
    plt.close()
    print("[OK] Generated:", path)

# Chart 2: Tiered Legal Reservation (Interpretation No. 443)
def generate_legal_reservation():
    fig, ax = plt.subplots(figsize=(9, 6), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    tiers = [
        ("1. 憲法保留 (絕對國會立法院親自制定)", "人身自由、提審保障 (憲法第8條)", "#dc2626"),
        ("2. 絕對法律保留 (剝奪生命或限制身體自由)", "刑罰、金錢沒收、強制管束處分", "#ea580c"),
        ("3. 相對法律保留 (侵害重大權利 / 財產權)", "稅捐課徵、行政罰裁罰、營業限制", "#d97706"),
        ("4. 執行性與細節性規定 (行政機關得訂定規則)", "給付行政、表冊填報、程序技術規範", "#16a34a")
    ]
    
    for i, (title, detail, color) in enumerate(tiers):
        y = 8 - i * 2.2
        rect = patches.FancyBboxPatch((0.5, y), 9, 1.8, boxstyle="round,pad=0.3",
                                     facecolor=color, edgecolor="none", alpha=0.9)
        ax.add_patch(rect)
        ax.text(1.0, y + 1.1, title, color="#ffffff", fontsize=12, fontweight='bold')
        ax.text(1.0, y + 0.4, f"實務範圍與個案範例：{detail}", color="#f8fafc", fontsize=10.5)
        
    ax.set_title("【司法院釋字第 443 號解釋：層次化法律保留原則體系圖】", fontsize=15, fontweight='bold', pad=20, color='#1e293b')
    plt.tight_layout()
    path = os.path.join(output_dir, 'chart_legal_reservation.png')
    plt.savefig(path, bbox_inches='tight')
    plt.close()
    print("[OK] Generated:", path)

# Chart 3: Proportionality Principle
def generate_proportionality():
    fig, ax = plt.subplots(figsize=(9, 5.5), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8)
    ax.axis('off')
    
    boxes = [
        ("一、適當性原則\n(適合性)", "行政手段必須能「有助於」\n行政目的之達成", 1.0, "#2563eb"),
        ("二、必要性原則\n(最小侵害性)", "在所有能達成目的手段中\n選擇對人民「侵害最小者」", 4.0, "#0284c7"),
        ("三、狹義比例原則\n(過磅衡量)", "手段所造成之損害\n不得顯失均衡(目的vs侵害)", 7.0, "#059669")
    ]
    
    for title, desc, x, color in boxes:
        rect = patches.FancyBboxPatch((x, 1.5), 2.5, 4.5, boxstyle="round,pad=0.3",
                                     facecolor=color, edgecolor="none", alpha=0.95)
        ax.add_patch(rect)
        ax.text(x + 1.25, 5.0, title, color="#ffffff", fontsize=11.5, fontweight='bold', ha='center', va='center')
        ax.text(x + 1.25, 3.0, desc, color="#ffffff", fontsize=10, ha='center', va='center', multialignment='center')
        
    ax.annotate("", xy=(3.8, 3.75), xytext=(3.5, 3.75), arrowprops=dict(arrowstyle="->", lw=3, color="#64748b"))
    ax.annotate("", xy=(6.8, 3.75), xytext=(6.5, 3.75), arrowprops=dict(arrowstyle="->", lw=3, color="#64748b"))
    
    ax.set_title("【行政程序法第 7 條：比例原則三大子原則過磅審查流程】", fontsize=15, fontweight='bold', pad=20, color='#1e293b')
    plt.tight_layout()
    path = os.path.join(output_dir, 'chart_proportionality.png')
    plt.savefig(path, bbox_inches='tight')
    plt.close()
    print("[OK] Generated:", path)

# Chart 4: Administrative Act 6 Elements
def generate_administrative_action():
    fig, ax = plt.subplots(figsize=(9, 6), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8)
    ax.axis('off')
    
    elements = [
        ("1. 行政機關", "出於代表公權力之政府組織或受託行使公權力者", "#4f46e5"),
        ("2. 公法事件", "基於公法法規行使職權（非民法私經濟行為）", "#2563eb"),
        ("3. 單方行為", "機關單方面作決定（無需相對人同意，非行政契約）", "#0284c7"),
        ("4. 具體處置", "針對特定人或特定可得確定事件（非一般抽象法規）", "#0d9488"),
        ("5. 對外直接", "直接對內部體系以外之人民產生法效（非內部指令）", "#059669"),
        ("6. 產生法律效果", "設定、變更或廢止權利義務關係（非純粹事實行為）", "#d97706")
    ]
    
    for i, (title, desc, color) in enumerate(elements):
        col = i % 2
        row = i // 2
        x = 0.5 + col * 4.6
        y = 5.2 - row * 2.3
        
        rect = patches.FancyBboxPatch((x, y), 4.3, 1.8, boxstyle="round,pad=0.3",
                                     facecolor=color, edgecolor="none", alpha=0.9)
        ax.add_patch(rect)
        ax.text(x + 0.3, y + 1.2, title, color="#ffffff", fontsize=12, fontweight='bold')
        ax.text(x + 0.3, y + 0.5, desc, color="#f8fafc", fontsize=9.5)
        
    ax.set_title("【行政程序法第 92 條：行政處分黃金六大構成要件判斷圖】", fontsize=15, fontweight='bold', pad=20, color='#1e293b')
    plt.tight_layout()
    path = os.path.join(output_dir, 'chart_administrative_action.png')
    plt.savefig(path, bbox_inches='tight')
    plt.close()
    print("[OK] Generated:", path)

# Chart 5: Administrative Remedy System
def generate_administrative_remedy():
    fig, ax = plt.subplots(figsize=(9, 6), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8)
    ax.axis('off')
    
    steps = [
        ("一、行政處分送達", "人民接獲違法或不當處分", 1.0, 6.0, "#64748b"),
        ("二、提起訴願 (訴願法)", "處分送達 30 日不變期間內向原處分機關之上級機關提起", 1.0, 4.0, "#d97706"),
        ("三、地方行政訴訟庭", "高等行政訴訟庭 (地方庭) 進行第一審裁判", 1.0, 2.0, "#2563eb"),
        ("四、最高行政法院", "終審法院進行第二審法律審判決 (救濟確定)", 1.0, 0.0, "#4f46e5")
    ]
    
    for title, desc, x, y, color in steps:
        rect = patches.FancyBboxPatch((x, y), 8.0, 1.4, boxstyle="round,pad=0.3",
                                     facecolor=color, edgecolor="none", alpha=0.9)
        ax.add_patch(rect)
        ax.text(x + 0.4, y + 0.85, title, color="#ffffff", fontsize=12, fontweight='bold')
        ax.text(x + 0.4, y + 0.35, f"-> {desc}", color="#f8fafc", fontsize=10)
        
    ax.set_title("【臺灣行政救濟體系：訴願前置與行政訴訟三級二審流程】", fontsize=15, fontweight='bold', pad=20, color='#1e293b')
    plt.tight_layout()
    path = os.path.join(output_dir, 'chart_administrative_remedy.png')
    plt.savefig(path, bbox_inches='tight')
    plt.close()
    print("[OK] Generated:", path)

if __name__ == '__main__':
    generate_legal_pyramid()
    generate_legal_reservation()
    generate_proportionality()
    generate_administrative_action()
    generate_administrative_remedy()
    print("=== All 5 high-resolution administrative law charts successfully generated! ===")
