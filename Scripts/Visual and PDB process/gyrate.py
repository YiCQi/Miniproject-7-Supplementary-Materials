import matplotlib.pyplot as plt
import numpy as np
import os

def read_and_average_gyrate(filename, window=10):
    """读取XVG文件并每window行计算均值，返回平均后的数据和元数据"""
    time = []
    gyrate = []
    metadata = {
        'title': '',
        'xlabel': '',
        'ylabel': '',
        'subtitle': ''
    }
    
    with open(filename, 'r') as f:
        # 首先收集所有原始数据
        raw_time = []
        raw_gyrate = []
        
        for line in f:
            line = line.strip()
            # 处理元数据
            if line.startswith('@'):
                if 'title' in line:
                    metadata['title'] = line.split('"')[1]
                elif 'xaxis' in line and 'label' in line:
                    metadata['xlabel'] = line.split('"')[1]
                elif 'yaxis' in line and 'label' in line:
                    metadata['ylabel'] = line.split('"')[1]
                elif 'subtitle' in line:
                    metadata['subtitle'] = line.split('"')[1]
            elif line and not line.startswith('#') and not line.startswith('@'):
                # 处理数据行
                parts = line.split()
                if len(parts) >= 2:
                    try:
                        raw_time.append(float(parts[0]))
                        raw_gyrate.append(float(parts[1]))
                    except ValueError:
                        continue
    
    # 计算移动平均值，每window个点取平均
    for i in range(0, len(raw_time), window):
        time_window = raw_time[i:i+window]
        gyrate_window = raw_gyrate[i:i+window]
        
        if time_window:  # 确保窗口不为空
            avg_time = np.mean(time_window)
            avg_gyrate = np.mean(gyrate_window)
            time.append(avg_time)
            gyrate.append(avg_gyrate)
    
    return np.array(time), np.array(gyrate), metadata

def plot_averaged_gyrate(targets, output_pdf, plot_title, ylabel):
    """绘制不同温度下平均后的Gyrate数据并保存为PDF"""
    plt.figure(figsize=(8, 6))
    
    # 使用更学术化的颜色
    colors = ['#9A4942', '#ECAC27', '#6DA7CA']
    labels = ['280K', '300K', '320K']
    
    # 先读取所有数据以确定统一的坐标轴范围
    all_data = []
    all_times = []
    for target in targets:
        xvg_file = f'/home/lamp/workspace/qyc/miniproject/data/final_process/{target}.xvg'
        time, data, _ = read_and_average_gyrate(xvg_file, window=10)
        all_data.append(data)
        all_times.append(time)
    
    # 确定统一的Y轴范围
    y_min = min([np.min(data) for data in all_data]) * 0.98
    y_max = max([np.max(data) for data in all_data]) * 1.02
    
    # 绘制数据
    for idx, target in enumerate(targets):
        time, data, metadata = read_and_average_gyrate(f'/home/lamp/workspace/qyc/miniproject/data/final_process/{target}.xvg', window=10)
        
        # 绘制数据，线条细一些
        plt.plot(time, data, color=colors[idx], linewidth=1, label=labels[idx])
    
    plt.title(f"{plot_title}\n{metadata['subtitle']}", fontsize=14, weight='bold')
    plt.xlabel(metadata['xlabel'], fontsize=12)
    plt.ylabel(ylabel, fontsize=12)
    plt.legend(title='Temperature', fontsize=10, frameon=False)
    
    # 设置坐标轴范围（保持与原始数据相同的范围）
    plt.ylim(y_min, y_max)
    
    # 设置坐标轴的颜色和线条
    plt.gca().spines['top'].set_linewidth(0.5)
    plt.gca().spines['right'].set_linewidth(0.5)
    plt.gca().spines['left'].set_linewidth(0.5)
    plt.gca().spines['bottom'].set_linewidth(0.5)
    plt.gca().tick_params(axis='both', which='both', length=5, width=0.5, direction='in', top='on', right='on')

    # 设置网格线样式
    plt.grid(True, linestyle='--', color='grey', alpha=0.6)
    plt.tight_layout()
    
    # 确保输出目录存在
    output_dir = os.path.dirname(output_pdf)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    plt.savefig(output_pdf, format='pdf')
    print(f"Averaged gyrate plot saved to {output_pdf}")
    plt.close()

# 定义目标文件列表
# gyrate_targets = [
#     '280K_50ns_gyrate', 
#     '300K_50ns_gyrate', 
#     '320K_50ns_gyrate'
# ]
gyrate_targets = [
    'hbond_280K', 
    'hbond_300K',
    'hbond_320K'
]

# 输出文件路径
# output_pdf_gyrate_avg = '/home/lamp/workspace/qyc/miniproject/data/outputs/gyrate_averaged_comparison_plot1.pdf'
output_pdf_gyrate_avg = '/home/lamp/workspace/qyc/miniproject/data/outputs/hbond_comparison.pdf'

# 绘制并保存平均后的gyrate图像
# plot_averaged_gyrate(gyrate_targets, output_pdf_gyrate_avg, 'Radius of Gyration', 'Radius of Gyration (nm)')
plot_averaged_gyrate(gyrate_targets, output_pdf_gyrate_avg, 'Hydrogen Bond Analysis', 'Number of Hydrogen Bonds')