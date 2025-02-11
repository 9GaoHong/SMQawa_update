import gzip 
import pickle
import argparse
import collections
import functools
import itertools
import os
import subprocess
from tqdm import tqdm
import numpy as np
from glob import glob
def main(args):
    base_dir = '/afs/cern.ch/user/h/hgao/SMQawa'
    eras = ["2016","2016APV","2018","2017"]
    for era in eras:
        era_dir = os.path.join(base_dir, f"{era}-SR-v2")
        print(f"=== {era_dir} ===")
        
        for subdir, _, _ in os.walk(era_dir):
            file_list = glob(os.path.join(subdir, "*.pkl.gz"))
            input_file = os.path.join(subdir, "inputfiles.dat")
            file_count = len(file_list)
            if os.path.isfile(input_file):
                with open(input_file, 'r') as f:
                    lines = f.readlines()
                    if len(lines) != file_count:
                        actual_files = set(os.path.basename(path) for path in file_list)
                        expected_files = set(f"histogram_{i}.pkl.gz" for i in range(len(lines)))
                        
                        missing_files = expected_files - actual_files
                        extra_files = actual_files - expected_files
                        print(f"文件 {input_file} \n 行数: {len(lines)}, 文件数量{file_count} ")
                        if missing_files:
                            # print(f"缺失的文件: {sorted(missing_files)}\n")
                            miss_file_path = os.path.join(subdir, "inputfiles_miss.dat")
                            with open(miss_file_path, 'w') as fout:
                                for mf in sorted(missing_files):
                                    index_str = mf.replace("histogram_", "").replace(".pkl.gz", "")
                                    index = int(index_str)
                                    # fout.write(lines[index])
                                    # print(lines[index])
                                    fout.write(f"{index_str} {lines[index]}")
                            if args.submit:
                                condor_sub_path = os.path.join(subdir, "condor.sub")
                                with open(condor_sub_path, 'r') as f_sub:
                                    content = f_sub.read()
                                content = content.replace("inputfiles.dat", "inputfiles_miss.dat")
                                content = content.replace("(ProcId)", "(Index)")
                                content = content.replace("queue jobfn from", "queue Index, jobfn from")
                                with open(condor_sub_path, 'w') as f_sub:
                                    f_sub.write(content)
                                    
                                condor_sub_fullpath = os.path.join(subdir, "condor.sub")
                                print(f">>> 提交子任务: condor_submit {condor_sub_fullpath}")
                                result = subprocess.run(
                                    ["condor_submit", condor_sub_fullpath],
                                    capture_output=True,
                                    text=True
                                )
                                if result.returncode == 0:
                                    print(f"提交成功: {result.stdout}")
                                else:
                                    print(f"提交失败: {result.stderr}")
                            else:
                                pass
                        
            else:
                pass
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="处理 SMQawa 目录下的 histogram 文件，并检查缺失情况后提交 Condor 子任务"
    )
    parser.add_argument(
        "--submit",
        action="store_true",
        help="如果设置此标志则提交 Condor 子任务，否则只打印提交信息"
    )
    args = parser.parse_args()
    main(args)