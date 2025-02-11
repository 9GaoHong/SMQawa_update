# python brewer-htcondor-skim-tmp.py -i data/datasetUL2018-mc-skim.txt -t vbs --isMC=1 --era=2018
# python brewer-htcondor-skim-tmp.py -i data/datasetUL2018-data-skim.txt -t vbs --isMC=0 --era=2018
# python brewer-htcondor-skim-tmp.py -i data/datasetUL2017-mc-skim.txt -t vbs --isMC=1 --era=2017
# python brewer-htcondor-skim-tmp.py -i data/datasetUL2017-data-skim.txt -t vbs --isMC=0 --era=2017
# python brewer-htcondor-skim-tmp.py -i data/datasetUL2016-mc-skim.txt -t vbs --isMC=1 --era=2016
# python brewer-htcondor-skim-tmp.py -i data/datasetUL2016-data-skim.txt -t vbs --isMC=0 --era=2016
# python brewer-htcondor-skim-tmp.py -i data/datasetUL2016APV-mc-skim.txt -t vbs --isMC=1 --era=2016APV
# python brewer-htcondor-skim-tmp.py -i data/datasetUL2016APV-data-skim.txt -t vbs --isMC=0 --era=2016APV

# python brewer-htcondor-skim-tmp-yx.py -i data/datasetUL2018-mc-skim-ratio.txt -t vbs --isMC=1 --era=2016APV
# python brewer-htcondor-skim-tmp-yx.py -i data/datasetUL2018-mc-skim-ratio.txt -t vbs --isMC=1 --era=2016
# python brewer-htcondor-skim-tmp-yx.py -i data/datasetUL2018-mc-skim-ratio.txt -t vbs --isMC=1 --era=2017
# python brewer-htcondor-skim-tmp-yx.py -i data/datasetUL2018-mc-skim-ratio.txt -t vbs --isMC=1 --era=2018
# rm -rf 201*
python brewer-htcondor-skim-tmp-yx.py -i data/datasetUL2016APV-data-skim.txt -t vbs --isMC=0 --era=2016APV --dd=MC
python brewer-htcondor-skim-tmp-yx.py -i data/datasetUL2016-data-skim.txt -t vbs --isMC=0 --era=2016 --dd=MC
python brewer-htcondor-skim-tmp-yx.py -i data/datasetUL2017-data-skim.txt -t vbs --isMC=0 --era=2017 --dd=MC
python brewer-htcondor-skim-tmp-yx.py -i data/datasetUL2018-data-skim.txt -t vbs --isMC=0 --era=2018 --dd=MC
python brewer-htcondor-skim-tmp-yx.py -i data/datasetUL2016APV-mc-skim.txt -t vbs --isMC=1 --era=2016APV --dd=MC
python brewer-htcondor-skim-tmp-yx.py -i data/datasetUL2016-mc-skim.txt -t vbs --isMC=1 --era=2016 --dd=MC
python brewer-htcondor-skim-tmp-yx.py -i data/datasetUL2017-mc-skim.txt -t vbs --isMC=1 --era=2017 --dd=MC
python brewer-htcondor-skim-tmp-yx.py -i data/datasetUL2018-mc-skim.txt -t vbs --isMC=1 --era=2018 --dd=MC


# python brewer-htcondor-skim-tmp-yx-nojetcut.py -i data/datasetUL2018-mc-skim-VBS.txt -t vbs --isMC=1 --era=2016APV --dd=MC
# python brewer-htcondor-skim-tmp-yx-nojetcut.py -i data/datasetUL2018-mc-skim-VBS.txt -t vbs --isMC=1 --era=2016 --dd=MC
# python brewer-htcondor-skim-tmp-yx-nojetcut.py -i data/datasetUL2018-mc-skim-VBS.txt -t vbs --isMC=1 --era=2017 --dd=MC
# python brewer-htcondor-skim-tmp-yx-nojetcut.py -i data/datasetUL2018-mc-skim-VBS.txt -t vbs --isMC=1 --era=2018 --dd=MC
# python brewer-htcondor-skim-tmp-yx.py -i data/datasetUL2018-mc-skim-ratio.txt -t vbs --isMC=1 --era=2016APV --dd=MC
# python brewer-htcondor-skim-tmp-yx.py -i data/datasetUL2018-mc-skim-ratio.txt -t vbs --isMC=1 --era=2016 --dd=MC
# python brewer-htcondor-skim-tmp-yx.py -i data/datasetUL2018-mc-skim-ratio.txt -t vbs --isMC=1 --era=2017 --dd=MC
# python brewer-htcondor-skim-tmp-yx.py -i data/datasetUL2018-mc-skim-ratio.txt -t vbs --isMC=1 --era=2018 --dd=MC

# python brewer-htcondor-skim.py -i data/datasetUL2016APV-data-skim.txt -t vbs --isMC=0 --era=2016APV --dd DYSR
# python brewer-htcondor-skim.py -i data/datasetUL2016APV-mc-skim.txt -t vbs --isMC=1 --era=2016APV --dd DYSR
# python brewer-htcondor-skim.py -i data/datasetUL2016-data-skim.txt -t vbs --isMC=0 --era=2016 --dd DYSR
# python brewer-htcondor-skim.py -i data/datasetUL2016-mc-skim.txt -t vbs --isMC=1 --era=2016 --dd DYSR
# python brewer-htcondor-skim.py -i data/datasetUL2017-data-skim.txt -t vbs --isMC=0 --era=2017 --dd DYSR
# python brewer-htcondor-skim.py -i data/datasetUL2017-mc-skim.txt -t vbs --isMC=1 --era=2017 --dd DYSR
# python brewer-htcondor-skim.py -i data/datasetUL2018-data-skim.txt -t vbs --isMC=0 --era=2018 --dd DYSR
# python brewer-htcondor-skim.py -i data/datasetUL2018-mc-skim.txt -t vbs --isMC=1 --era=2018 --dd DYSR
#rm 2018_event/* -rf
#python brewer-htcondor-2018-v2-event.py -i data/hope.txt -t vbs --isMC=1 --era=2018
#python brewer-htcondor-2018-v2-data-event.py -i data/hope_data.txt -t vbs --isMC=0 --era=2018
# python brewer-htcondor-skim.py -i data/datasetUL2017-mc-skim-zz2l2nu.txt -t vbs --isMC=1 --era=2017 --dd DYSR
# python brewer-htcondor-skim.py -i data/datasetUL2018-mc-add.txt -t vbs --isMC=1 --era=2018 --dd DYSR