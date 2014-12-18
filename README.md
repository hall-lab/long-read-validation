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

Download PacBio and Illumina Moleculo split reads from NA12878
```
wget http://colbychiang.com/hall/long-read-validation/NA12878.pacbio.splitreads.excldups.breakpoint.bedpe.gz
wget http://colbychiang.com/hall/long-read-validation/NA12878.moleculo.splitreads.excldups.breakpoint.bedpe.gz
```

Run the validation script
```
longReadValidate \
    -i example/NA12878.sv.bedpe \
    -m NA12878.moleculo.splitreads.excldups.breakpoint.bedpe.gz \
    -p NA12878.pacbio.splitreads.excldups.breakpoint.bedpe.gz \
    > NA12878.sv.val.bedpe
```

Note that column 11 of the BEDPE file must contain the type of SV (DEL, DUP, INV, or INT)

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