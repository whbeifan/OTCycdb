# OTCycdb
Oxytetracycline biosynthesis and degradation database
<img width="1420" height="1101" src="https://github.com/whbeifan/OTCycdb/blob/main/OTCyc.png" />

## Reference pathway
[1] [https://kegg.jp/pathway/map00253](https://kegg.jp/pathway/map00253)

[2] [https://kegg.jp/module/M00780](https://kegg.jp/module/M00780)

[3] [https://kegg.jp/entry/DG00397](https://kegg.jp/entry/DG00397)

[4] [https://kegg.jp/entry/K19542](https://kegg.jp/entry/K19542) #四环素和土霉素耐药基因

## 中国大陆访问KEGG数据的方法
Windows系统的HOSTS文件路径：C:\Windows\System32\drivers\etc\HOSTS 或 C:\Windows\System32\drivers\etc\hosts

linux系统的HOSTS文件路径：/etc/hosts

在HOSTS文件中写入如下信息即可：
```
133.103.200.21	www.kegg.jp
133.103.200.21	kegg.jp
133.103.200.20	www.genome.jp
133.103.200.20	genome.jp
133.103.200.27	rest.kegg.jp
133.103.200.27	www.rest.kegg.jp
```

## Annotation
kofamscan annotation:
```
/work/software/kofamscan/v1.3.0/bin/exec_annotation -o meta.unigene.OTCdb.temp --profile /Work/db/OTCdb/db \
  --ko-list /Work/database/kegg/2025/ko_list \
  --cpu 10 --e-value 1e-05 --format detail-tsv meta.uniprotein.fasta
rm -rf tmp
python /Work/db/OTCdb/get_kofamscan2best.py meta.unigene.OTCdb.temp >meta.unigene.OTCdb.out
```
diamond annotation:
```
diamond blastp --query meta.uniprotein.fasta --db /Work/db/OTCdb/OTCyc.dmnd \
  --outfmt 6 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore qlen slen stitle \
  --max-target-seqs 5 --evalue 1e-05 --threads 10 --out meta.uniprotein.OTCyc.m6
#下面是筛选覆盖度大于30%，相似度大于90%的注释结果（分析的是可以适当放宽松一些）
python /Work/db/OTCdb/blast_filter.py meta.uniprotein.OTCyc.m6 \
  --outfmt std qlen slen stitle --out qseqid sseqid pident length qlen slen qstart qend sstart send stitle evalue bitscore \
  --min_qcov 30 --min_scov 30 --min_pident 90 --evalue 1e-05 --best >meta.uniprotein.OTCyc.tsv
```
