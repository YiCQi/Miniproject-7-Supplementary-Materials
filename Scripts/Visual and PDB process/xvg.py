import matplotlib.pyplot as plt
import numpy as np

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

def plot_xvg(xvg_file, output_pdf):
    """绘制XVG数据并保存为PDF"""
    time, rmsd, metadata = read_xvg(xvg_file)
    
    plt.figure(figsize=(8, 6))
    plt.plot(time, rmsd, color=(0.2, 0.4, 0.8), linewidth=2)
    
    plt.title(f"{metadata['title']}\n{metadata['subtitle']}", fontsize=12)
    plt.xlabel(metadata['xlabel'], fontsize=12)
    plt.ylabel(metadata['ylabel'], fontsize=12)
    
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    
    plt.savefig(output_pdf, format='pdf')
    print(f"Plot saved to {output_pdf}")
    plt.close()

targets = ['potential',
           'density_280', 'density_300', 'density_320',
           'pressure_280', 'pressure_300', 'pressure_320',
           'temperature_280', 'temperature_300', 'temperature_320',]

for target in targets:
    xvg_file = f'/home/lamp/workspace/qyc/miniproject/data/final_process/{target}.xvg'
    output_pdf = f'/home/lamp/workspace/qyc/miniproject/data/final_outputs/{target}_plot.pdf'

    plot_xvg(xvg_file, output_pdf)