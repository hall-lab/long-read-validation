Long-read validation
====================

Long-read validation of BEDPE structural variation

## Table of Contents
1. [Quick start](#quick-start)
2. [Usage](#usage)

## Quick start

Dependencies: [bedtools](https://github.com/arq5x/bedtools2)

Clone the git repository
```
git clone git@github.com:hall-lab/long-read-validation.git
```

Download Illumina Moleculo and PacBio split reads from NA12878
```
wget http://colbychiang.com/hall/long-read-validation/NA12878.moleculo.splitreads.excldups.breakpoint.bedpe.gz
wget http://colbychiang.com/hall/long-read-validation/NA12878.pacbio.splitreads.excldups.breakpoint.bedpe.gz
```

Run the validation script. Note that column 11 of the BEDPE file must contain the type of SV (DEL, DUP, INV, or INT)

This appends two columns to the BEDPE file:

* Number of supporting Moleculo split reads
* Number of supporting PacBio split reads

```
longReadValidate \
    -i example/NA12878.sv.bedpe \
    -m NA12878.moleculo.splitreads.excldups.breakpoint.bedpe.gz \
    -p NA12878.pacbio.splitreads.excldups.breakpoint.bedpe.gz \
    -s 5 \
    > NA12878.sv.val.bedpe
```

For [Layer _et al._](http://genomebiology.com/2014/15/6/R84) we required at least 1 Moleculo split read or at least 2
PacBio split reads, with slop of 5.
```
cat NA12878.sv.val.bedpe | awk '$(NF-1)>=1 || $NF>=2' | wc -l
# 2508
```

## Usage

```
usage: ./longReadValidate OPTIONS

OPTIONS:
    -h      Show this message
    -i      BEDPE input file name
    -s      slop (default: 0)
    -m      Moleculo file
    -p      PacBio file
    -k      keep temporary files
```

## Appendix
#### Generate validation BEDPE files from PacBio and Moleculo long-read BAM files

The following commands demonstrate how NA12878.moleculo.splitreads.excldups.breakpoint.bedpe.gz and NA12878.pacbio.splitreads.excldups.breakpoint.bedpe.gz were constructed from long-read BAM files.
```
# ===============================================
# 0. Requirements
# https://github.com/hall-lab/sv-tools/blob/master/splitterToBreakpoint
# https://github.com/hall-lab/sv-tools/blob/master/splitReadSamToBedpe


# ===============================================
# 1. PacBio

pwd
# /mnt/hall13_local/cc2qe/na12878_pacbio

# a. Download the data
~cc2qe/.aspera/connect/bin/ascp -i ~cc2qe/.aspera/connect/etc/asperaweb_id_dsa.putty -QTr -l 1000M anonftp@ftp-trace.ncbi.nlm.nih.gov:/1000genomes/ftp/technical/working/20131209_na12878_pacbio/Schadt/alignment/NA12878.pacbio_fr_MountSinai.bwa-sw.20140211.bam .
~cc2qe/.aspera/connect/bin/ascp -i ~cc2qe/.aspera/connect/etc/asperaweb_id_dsa.putty -QTr -l 1000M anonftp@ftp-trace.ncbi.nlm.nih.gov:/1000genomes/ftp/technical/working/20131209_na12878_pacbio/Schadt/alignment/NA12878.pacbio_fr_MountSinai.bwa-sw.20140211.bam.bai .

# b. Convert the bam file to fastq
samtools view -F 256 -u NA12878.pacbio_fr_MountSinai.bwa-sw.20140211.readsort.bam | bamToFastq -i - -fq /dev/stdout | gzip -c > NA12878.pacbio_fr_MountSinai.bwa-sw.20140211.fq.gz

# c. Align with pacbio (55.5 hours)
time bwa-0.7.10 mem \
    -x pacbio \
    -t 24 \
    -M \
    -R "@RG\tID:NA12878\tSM:NA12878" \
    /shared/genomes/b37/full/human_g1k_v37.fasta \
    NA12878.pacbio_fr_MountSinai.bwa-sw.20140211.fq.gz \
    | samblaster -s splitters.sam \
    | sambamba view -S -f bam /dev/stdin \
    > NA12878.pacbio.realign.bam
# real    3329m25.715s
# user    76145m20.379s
# sys     499m22.800s

# get stats on read length
# coverage depth: 79219315761/2867459933 = 27.627
# (2867459933 is non-gapped genome size)
sambamba view -F "not duplicate and not secondary_alignment"  NA12878.pacbio.realign.bam | awk '{ print length($10) }' | zstats > NA12878.pacbio.realign.bam.readlength.stats
cat NA12878.pacbio.realign.bam.readlength.stats
# num lines:    24850098
# num unique:   25830
# sum:      79219315761.0
# arith. mean:  3187.88745867
# geo. mean:    2252.60697049
# min:      50.0
# Q1:       1390.0
# median:       2355.0
# Q3:       4042.0
# max:      40986.0
# mode:     1628.0 (N=6850)
# anti-mode:    40986.0 (N=1)
# stdev:        2763.47786754
# variance: 7636809.92441

# d. Convert the split reads to bedpe format
# svtools commit: 73bd62d59deaecb03c0467e1031a02e31709a402
time sambamba view -h -F "not duplicate" NA12878.pacbio.realign.bam \
    | ~/code/svtools/splitReadSamToBedpe -i stdin \
    | gzip -c \
    > NA12878.pacbio.splitreads.excldups.bedpe.gz
# real    210m17.002s
# user    281m14.462s
# sys     6m2.616s

# e. Convert the split reads to breakpoint calls (slop of 0 on each side of break)
time zcat NA12878.pacbio.splitreads.excldups.bedpe.gz \
    | ~/code/svtools/splitterToBreakpoint -s 0 -i stdin -r 1000000 \
    | awk '{ if ($2<0) $2=0; if ($4<0) $4=0; print }' OFS="\t" \
    | awk '{ if ($1!=$4) { $18="DISTANT_INTER" } else { gsub("deletion","DEL",$18); gsub("duplication","DUP",$18); gsub("inversion","INV",$18); gsub("^local","LOCAL",$18); gsub("^distant","DISTANT",$18); } print }' OFS="\t" \
    | gzip -c > slop0/NA12878.pacbio.splitreads.excldups.breakpoint.bedpe.gz
# real    0m48.947s
# user    1m41.482s
# sys     0m2.929s

# ===============================================
# 2. Moleculo

pwd
# /mnt/hall13_local/cc2qe/na12878_moleculo

# a. Download moleculo data
~cc2qe/.aspera/connect/bin/ascp -i ~cc2qe/.aspera/connect/etc/asperaweb_id_dsa.putty -QTr -l 1000M anonftp@ftp-trace.ncbi.nlm.nih.gov:/1000genomes/ftp/technical/working/20131209_na12878_moleculo/alignment/NA12878.moleculo.bwa-mem.20140110.bam .
~cc2qe/.aspera/connect/bin/ascp -i ~cc2qe/.aspera/connect/etc/asperaweb_id_dsa.putty -QTr -l 1000M anonftp@ftp-trace.ncbi.nlm.nih.gov:/1000genomes/ftp/technical/working/20131209_na12878_moleculo/alignment/NA12878.moleculo.bwa-mem.20140110.bam.bai .

# get stats on read length
# coverage depth: 89375800009/2867459933 = 31.16898
# (2867459933 is non-gapped genome size)
sambamba view -F "not duplicate and not secondary_alignment" NA12878.moleculo.bwa-mem.20140110.bam | awk '{ print length($10) }' | zstats > NA12878.moleculo.bwa-mem.20140110.bam.readlength.stats
cat NA12878.moleculo.bwa-mem.20140110.bam.readlength.stats
# num lines:    22136936
# num unique:   13990
# sum:      89375800009.0
# arith. mean:  4037.40608045
# geo. mean:    3454.85517152
# min:      1500.0
# Q1:       2158.0
# median:       3227.0
# Q3:       5256.0
# max:      22319.0
# mode:     1501.0 (N=10577)
# anti-mode:    22319.0 (N=1)
# stdev:        2387.56588965
# variance: 5700470.87744

# b. Read sort the file
samba sort -m 32G --tmpdir=temp -n -p -t 24 -o NA12878.moleculo.bwa-mem.20140110.readsort.bam NA12878.moleculo.bwa-mem.20140110.bam

# c. Convert the split reads to bedpe format
sambamba view -h -F "not duplicate" NA12878.moleculo.bwa-mem.20140110.readsort.bam | ~/code/svtools/splitReadSamToBedpe -i stdin | bedtools sort | gzip -c > NA12878.moleculo.splitreads.excldups.bedpe.gz

# d. Convert to breakpoint calls (slop of 0 on each side of break)
mkdir -p slop0
zcat NA12878.moleculo.splitreads.excldups.bedpe.gz \
    | ~/code/svtools/splitterToBreakpoint -s 0 -i stdin -r 1000000 \
    | awk '{ if ($2<0) $2=0; if ($4<0) $4=0; print }' OFS="\t" \
    | awk '{ if ($1!=$4) { $18="DISTANT_INTER" } else { gsub("deletion","DEL",$18); gsub("duplication","DUP",$18); gsub("inversion","INV",$18); gsub("^local","LOCAL",$18); gsub("^distant","DISTANT",$18); } print }' OFS="\t" \
    | bgzip -c \
    > slop0/NA12878.moleculo.splitreads.excldups.breakpoint.bedpe.gz
```
