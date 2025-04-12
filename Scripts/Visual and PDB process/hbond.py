import matplotlib.pyplot as plt
import numpy as np

# 设置字体和样式
plt.style.use('default')  # 使用默认样式确保白色背景
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.linewidth'] = 1.2

# 数据准备
temperatures = ['280K', '300K', '320K']
colors = ['#9A4942', '#ECAC27', '#6DA7CA']
data = {
    'Group1': [18, 26, 21],
    'Group2': [19, 26, 21]
}

# 创建图形（强制白色背景）
fig, ax = plt.subplots(figsize=(6, 5), dpi=300, facecolor='white')
fig.patch.set_facecolor('white')

# 设置柱状图位置和宽度
x = np.arange(len(temperatures))
width = 0.35

# 绘制柱状图
rects1 = ax.bar(x - width/2, data['Group1'], width, 
                color=colors, edgecolor='black', linewidth=0.8, 
                label='Measurement 1', zorder=3)
rects2 = ax.bar(x + width/2, data['Group2'], width, 
                color=colors, edgecolor='black', linewidth=0.8, 
                hatch='//', label='Measurement 2', zorder=3)

# 添加误差条
ax.errorbar(x - width/2, data['Group1'], yerr=0, fmt='none', 
            ecolor='black', capsize=3, capthick=0.8, elinewidth=0.8)
ax.errorbar(x + width/2, data['Group2'], yerr=0, fmt='none', 
            ecolor='black', capsize=3, capthick=0.8, elinewidth=0.8)

# 添加轴标签和标题
ax.set_ylabel('Number of Hydrogen Bonds', fontweight='bold')
ax.set_xlabel('Temperature', fontweight='bold')
ax.set_title('Protein-Protein Interface Hydrogen Bonds', 
             fontweight='bold', pad=15)

# 设置x轴刻度
ax.set_xticks(x)
ax.set_xticklabels(temperatures)

# 设置y轴范围
ax.set_ylim(0, 30)
ax.set_yticks(np.arange(0, 31, 5))

# 添加图例
ax.legend(frameon=True, loc='upper left', facecolor='white')

# 添加灰色虚线网格 (修改处)
ax.grid(axis='y', linestyle='--', color='#808080', alpha=0.5, zorder=0)

# 设置背景色 (明确设置)
ax.set_facecolor('white')

# 调整布局
plt.tight_layout()

# 保存图像
plt.savefig('hydrogen_bonds.png', bbox_inches='tight', dpi=300, facecolor='white')
plt.savefig('hydrogen_bonds.pdf', bbox_inches='tight', facecolor='white')

plt.show()