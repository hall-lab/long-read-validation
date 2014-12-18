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
    > NA12878.sv.val.bedpe
```

For [Layer _et al._](http://genomebiology.com/2014/15/6/R84) we required at least 1 Moleculo split read or at least 2
PacBio split reads
```
cat NA12878.sv.val.bedpe | awk '$(NF-1)>=1 || $NF>=2' | wc -l
# 2414
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

