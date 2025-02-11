import gzip
import pickle
import glob
import os
import numpy

dataset=["DYJetsToLL_LHEFilterPtZ-100To250_MatchEWPDG20_TuneCP5_13TeV-amcatnloFXFX-pythia8","DYJetsToLL_LHEFilterPtZ-250To400_MatchEWPDG20_TuneCP5_13TeV-amcatnloFXFX-pythia8","DYJetsToLL_LHEFilterPtZ-400To650_MatchEWPDG20_TuneCP5_13TeV-amcatnloFXFX-pythia8","DYJetsToLL_LHEFilterPtZ-50To100_MatchEWPDG20_TuneCP5_13TeV-amcatnloFXFX-pythia8","DYJetsToLL_LHEFilterPtZ-650ToInf_MatchEWPDG20_TuneCP5_13TeV-amcatnloFXFX-pythia8","DYJetsToTauTau_M-50_AtLeastOneEorMuDecay_TuneCP5_13TeV-powhegMiNNLO-pythia8-photos","EWKZ2Jets_ZToLL_M-50_TuneCP5_withDipoleRecoil_13TeV-madgraph-pythia8"]
# for i in dataset /eos/user/h/hgao/ZZTo2L2Nu/PKL/2016_1214_SR_addDD.pkl.gz

with gzip.open(f"/eos/user/h/hgao/ZZTo2L2Nu/PKL/2016_1214_SR_addDD.pkl.gz", 'rb') as f:
    file_data = pickle.load(f) 
    # print(i)
print(file_data["DYJetsToLL_LHEFilterPtZ-100To250_MatchEWPDG20_TuneCP5_13TeV-amcatnloFXFX-pythia8"]['hist']['gnn_score'][{'channel': "vbs-SR"}])
print(file_data['DoubleEG']['hist']['gnn_score'][{'channel': "vbs-SR",'systematic': 'nominal'}].values().sum())
print(file_data['DoubleMuon']['hist']['gnn_score'][{'channel': "vbs-SR",'systematic': 'nominal'}].values().sum())
# print(file_data['SingleElectron']['hist']['gnn_score'][{'channel': "vbs-SR",'systematic': 'nominal'}].values().sum())
# print(file_data['SingleMuon']['hist']['gnn_score'][{'channel': "vbs-SR",'systematic': 'nominal'}].values().sum())
print(file_data['MuonEG']['hist']['gnn_score'][{'channel': "vbs-SR",'systematic': 'nominal'}].values().sum())
#     print("no data driven",file_data[i]['hist']['met_pt'][{'channel': "vbs-DY",'systematic': 'nominal'}].values().sum())
#     with gzip.open(f"/eos/user/h/hgao/ZZTo2L2Nu/PKL/2016APV_addDD_1203_DY.pkl.gz", 'rb') as f:
#         file_data = pickle.load(f) 
#     print(file_data[i]['hist']['met_pt'])
#     print("add data driven",file_data[i]['hist']['met_pt'][{'channel': "vbs-DY",'systematic': 'nominal'}].values().sum())

import hist
import numpy as np
with gzip.open(f"/eos/user/h/hgao/ZZTo2L2Nu/PKL/2016APV_1203_ratio.pkl.gz", 'rb') as f:
    file_data = pickle.load(f) 
histos = file_data["DYJetsToLL_LHEFilterPtZ-100To250_MatchEWPDG20_TuneCP5_13TeV-amcatnloFXFX-pythia8"]['hist']['met_pt']
# 获取所有的 channel 和 systematic
channels = ['vbs-DDDY60150', 'vbs-DDDY150300', 'vbs-DDDY300inf']
systematics = histos.axes['systematic']  # 假设 'systematic' 是一个维度名称

# 初始化一个用于存储结果的数组
combined_bins = None

# 遍历每个 systematic 并合并 channel
for systematic in systematics:
    # 对当前 systematic 的不同 channel 投影到 'met_pt'
    channel_hist_list = [
        hist[{'channel': channel, 'systematic': systematic}] for channel in channels
    ]
    
    # 按 bin 相加
    channel_sum = sum(channel_hist.values() for channel_hist in channel_hist_list)
    
    # 累加不同 systematics 的结果
    if combined_bins is None:
        combined_bins = channel_sum
    else:
        combined_bins += channel_sum
combined_hist = hist(hist.axes['met_pt'], hist.storage.Weight())
combined_hist[:] = combined_bins
output_file = "/eos/user/h/hgao/ZZTo2L2Nu/PKL/combined_histogram.pkl.gz"

# 将结果存为 gzip 压缩的 pickle 文件
with gzip.open(output_file, "wb") as f:
    pickle.dump(combined_hist, f)
    
print(f"Histogram saved as {output_file}")
# combined_bins 是最终合并的 bin 值

# eras = ["2016","2016APV","2018","2017"]
# for era in eras:
#     with open(f"/afs/cern.ch/user/h/hgao/SMQawa/src/qawa/data/ddr/DDMC_Ratio_SR_{era}_hgao.pkl", 'rb') as f:
#         file_data = pickle.load(f) 
#     print(era)
#     print(file_data,"\n")
# eras = ["2016","2016APV","2018","2017"]
# for era in eras:
#     with open(f"/afs/cern.ch/user/h/hgao/SMQawa/src/qawa/data/ddr/DDMC_Ratio_SR_{era}_hgao.pkl", 'rb') as f:
#         file_data = pickle.load(f) 
#     print(era)
#     print(file_data,"\n")
# mc_2016= {
#     "60-150": [47113.584386, 55615.614501, 19741.569918, 4216.718701, 821.822684, 206.676482, 23.631351, 3.627953],
#     "150-300": [7126.641261, 9056.377428, 3494.639734, 816.547522, 159.83908, 34.367858, 3.476017, 1.374981],
#     "300-800": [567.139019, 786.555342, 351.297253, 100.729025, 22.687338, 6.502101, 0.670733, 0.305393]
# }
# mc_2016APV= {
#     "60-150": [54258.421612, 64168.603852, 22913.03406, 4998.008992, 1011.544512, 241.637017, 28.975618, 4.937205],
#     "150-300": [7830.442055, 9840.113485, 3770.625049, 878.655774, 184.784061, 29.647966, 4.914723, 1.587663],
#     "300-800": [394.543698, 544.364319, 243.494125, 75.035643, 19.618289, 5.052331, 0.500514, 0.493962]
# }
# result_dict={}
# for key in mc_2016:
#     result_dict[key] = [
#         val_dd + val_mc if val_mc != 0 else None  
#         for val_dd, val_mc in zip(mc_2016[key], mc_2016APV[key])
#     ]
    
# print(result_dict)
