# source ~/.zshrc
# conda activate logevaluate

cd evaluation
for technique in AEL Drain IPLoM LenMa LFA LogCluster LogMine Logram LogSig MoLFI SHISO SLCT Spell Tipping
do
    echo ${technique}
    python ${technique}_eval.py -otc
done
