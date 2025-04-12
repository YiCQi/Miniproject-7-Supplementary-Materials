import matplotlib.pyplot as plt
import numpy as np
import os

def read_xvg(filename):
    """读取XVG文件并返回数据和元数据"""
    time = []
    rmsd = []
    metadata = {
        'title': '',
        'xlabel': '',
        'ylabel': '',
        'subtitle': ''
    }
    
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            # 跳过注释行和空行
            if line.startswith('#') or line.startswith('@') and 'TYPE' in line:
                continue
            # 提取元数据
            if line.startswith('@'):
                if 'title' in line:
                    metadata['title'] = line.split('"')[1]
                elif 'xaxis' in line and 'label' in line:
                    metadata['xlabel'] = line.split('"')[1]
                elif 'yaxis' in line and 'label' in line:
                    metadata['ylabel'] = line.split('"')[1]
                elif 'subtitle' in line:
                    metadata['subtitle'] = line.split('"')[1]
            else:
                # 处理数据行
                parts = line.split()
                if len(parts) >= 2:
                    try:
                        time.append(float(parts[0]))
                        rmsd.append(float(parts[1]))
                    except ValueError:
                        continue
    
    return np.array(time), np.array(rmsd), metadata

def plot_comparison(targets, output_pdf, plot_title, ylabel):
    """绘制不同温度下的RMSD、RMSD_xtal 或 Gyrate数据并保存为PDF"""
    plt.figure(figsize=(8, 6))
    
    # 使用更学术化的颜色（选择matplotlib的默认调色板颜色）
    colors = ['#9A4942', '#ECAC27', '#6DA7CA']
    labels = ['280K', '300K', '320K']
    
    for idx, target in enumerate(targets):
        xvg_file = f'/home/lamp/workspace/qyc/miniproject/data/final_process/{target}.xvg'
        time, data, metadata = read_xvg(xvg_file)
        
        # 绘制数据，线条细一些
        plt.plot(time, data, color=colors[idx], linewidth=1, label=labels[idx])
    
    plt.title(f"{plot_title}\n{metadata['subtitle']}", fontsize=14, weight='bold')
    plt.xlabel(metadata['xlabel'], fontsize=12)
    plt.ylabel(ylabel, fontsize=12)
    plt.legend(title='Temperature', fontsize=10, frameon=False)  # 去掉图例的框

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
    print(f"Plot saved to {output_pdf}")
    plt.close()

# 定义目标文件列表（假设这三种温度对应的rmsd文件）
rmsd_targets = [
    '280K_50ns_rmsd', 
    '300K_50ns_rmsd', 
    '320K_50ns_rmsd'
]

rmsd_xtal_targets = [
    '280K_50ns_rmsd_xtal', 
    '300K_50ns_rmsd_xtal', 
    '320K_50ns_rmsd_xtal'
]

gyrate_targets = [
    '280K_50ns_gyrate', 
    '300K_50ns_gyrate', 
    '320K_50ns_gyrate'
]

# 输出文件路径
output_pdf_rmsd = '/home/lamp/workspace/qyc/miniproject/data/outputs/rmsd_comparison_plot.pdf'
output_pdf_rmsd_xtal = '/home/lamp/workspace/qyc/miniproject/data/outputs/rmsd_xtal_comparison_plot.pdf'
output_pdf_gyrate = '/home/lamp/workspace/qyc/miniproject/data/outputs/gyrate_comparison_plot.pdf'

# 绘制并保存图像
plot_comparison(rmsd_targets, output_pdf_rmsd, 'RMSD Comparison', 'RMSD')
plot_comparison(rmsd_xtal_targets, output_pdf_rmsd_xtal, 'RMSD Xtals Comparison', 'RMSD Xtals')
plot_comparison(gyrate_targets, output_pdf_gyrate, 'Gyrate Comparison', 'Gyrate')
