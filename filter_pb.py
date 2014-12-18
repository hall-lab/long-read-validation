#!/usr/bin/env python
import sys

def check_intersect(hits):
    
    intersects = 0
    
    for i in range(len(hits)):
        for j in range(i+1,len(hits)):
            hit_1 = hits[i]
            hit_2 = hits[j]
            
            l_start = max(hit_1[0],hit_2[0])
            l_end = min(hit_1[1],hit_2[1])

            r_start = max(hit_1[2],hit_2[2])
            r_end = min(hit_1[3],hit_2[3])

            if (l_end>=l_start) and (r_end>=r_end):
                intersects+=1
    return [len(hits),intersects]

DELLY_NAME = 24
PB_L_START = 1
PB_L_END = 2
PB_R_START = 4
PB_R_END = 5

last = []
last_pb_l_start = -1
last_pb_l_end = -1
last_pb_r_start = -1
last_pb_r_end = -1
pb_hits = []

for l in sys.stdin:
    curr=l.rstrip().split('\t')

    if len(last) > 0:
        if last[DELLY_NAME] == curr[DELLY_NAME]:
            pb_hits.append([int(curr[PB_L_START]), \
                            int(curr[PB_L_END]), \
                            int(curr[PB_R_START]), \
                            int(curr[PB_R_END])])
       

        else:
            r = check_intersect(pb_hits)
            if r[0] > 1 and r[1] > 0:
                for i in range(len(pb_hits)):
                    print '\t'.join(last)


            last = curr
            last_pb_l_start = int(curr[PB_L_START])
            last_pb_l_end = int(curr[PB_L_END])
            last_pb_r_start = int(curr[PB_R_START])
            last_pb_r_end = int(curr[PB_R_END])
            pb_hits = []
            pb_hits.append([int(curr[PB_L_START]), \
                            int(curr[PB_L_END]), \
                            int(curr[PB_R_START]), \
                            int(curr[PB_R_END])])
 
    else:
        last = curr
        last_pb_l_start = int(curr[PB_L_START])
        last_pb_l_end = int(curr[PB_L_END])
        last_pb_r_start = int(curr[PB_R_START])
        last_pb_r_end = int(curr[PB_R_END])
        pb_hits = []
        pb_hits.append([int(curr[PB_L_START]), \
                        int(curr[PB_L_END]), \
                        int(curr[PB_R_START]), \
                        int(curr[PB_R_END])])
 
r = check_intersect(pb_hits)
if r[0] > 1 and r[1] > 0:
    if r[0] > 1 and r[1] > 0:
        for i in range(len(pb_hits)):
            print '\t'.join(last)


