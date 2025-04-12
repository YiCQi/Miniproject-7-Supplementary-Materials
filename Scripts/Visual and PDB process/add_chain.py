def process_pdb(input_file, output_file):
    with open(input_file, 'r') as f_in, open(output_file, 'w') as f_out:
        line_count = 0
        seen_residues = set()  # 用于记录已经处理过的残基号
        first_pass_25_57 = True  # 标记是否第一次遇到25-57
        
        for line in f_in:
            line_count += 1
            if line_count < 5:  # 前4行直接写入
                f_out.write(line)
                continue
            
            if not line.startswith(('ATOM', 'HETATM')):
                continue  # 跳过非ATOM/HETATM行
                
            if len(line) < 26:  # 确保行足够长（第4列在17-20字符位置）
                f_out.write(line)
                continue
                
            # 获取第4列（残基名称，如SOL/NA）
            res_name = line[17:20].strip()
            if res_name in ('SOL', 'NA'):  # 如果是水分子或钠离子，直接跳过
                continue
                
            # 获取残基序号（第5列，22-26字符位置）
            try:
                res_num = int(line[22:26].strip())
            except ValueError:
                f_out.write(line)
                continue
                
            # 分配链ID
            if 25 <= res_num <= 57:
                if first_pass_25_57:  # 第一次出现25-57，分配A
                    chain_id = 'A'
                else:  # 第二次出现25-57，分配B
                    chain_id = 'B'
            elif 2 <= res_num <= 416 or res_num == 417:  # 其他情况分配A
                chain_id = 'A'
            else:
                chain_id = ' '  # 其他情况不分配链
                
            # 检查是否已经处理过25-57的所有残基
            if 25 <= res_num <= 57 and res_num not in seen_residues:
                seen_residues.add(res_num)
                # 如果25-57全部出现过，则标记first_pass_25_57为False
                if seen_residues.issuperset(range(25, 58)):
                    first_pass_25_57 = False
                
            # 修改链ID并写入
            new_line = line[:21] + chain_id + line[22:]
            f_out.write(new_line)
# 使用示例：处理输入的PDB文件和输出文件  

process_pdb('280K_50ns_converted.pdb', '280_3fie.pdb')
process_pdb('300K_50ns_converted.pdb', '300_3fie.pdb')
process_pdb('320K_50ns_converted.pdb', '320_3fie.pdb')  