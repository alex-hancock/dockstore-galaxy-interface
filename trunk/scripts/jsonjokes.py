('{ "bam_input": { "class": "File", "path": "' + str(sys.argv[1]) + 
'" }, "bamstats_report": { "class": "File", "path": "' + str(sys.argv[2])+ '"} }')






('{  "reads": [{  "path":"' + sys.argv[1] + 
 '",  "class":"File"  },  {"path":"' + sys.argv[2] + 
 '",  "class":"File"}  ],  "reference_gz_amb": {"path":'
 '"http://s3.amazonaws.com/pan-cancer-data/pan-cancer-reference/genome.fa.gz.64.amb"'
 ',"class": "File"  },  "reference_gz_sa": {  "path": '
 '"http://s3.amazonaws.com/pan-cancer-data/pan-cancer-reference/genome.fa.gz.64.sa",'
 '"class": "File"},  "reference_gz_pac": { "path": '
 '"http://s3.amazonaws.com/pan-cancer-data/pan-cancer-reference/genome.fa.gz.64.pac",'
 '"class": "File"  },  "reference_gz_ann": {    "path": '
 '"http://s3.amazonaws.com/pan-cancer-data/pan-cancer-reference/genome.fa.gz.64.ann",'
 '"class": "File"  },  "reference_gz_bwt": {    "path": '
 '"http://s3.amazonaws.com/pan-cancer-data/pan-cancer-reference/genome.fa.gz.64.bwt",'
 '"class": "File"  },  "reference_gz_fai": {    "path": '
 '"http://s3.amazonaws.com/pan-cancer-data/pan-cancer-reference/genome.fa.gz.fai",'
 '"class": "File"},  "reference_gz": {    "path": '
 '"http://s3.amazonaws.com/pan-cancer-data/pan-cancer-reference/genome.fa.gz",'
 '"class": "File"  },  "merged_output_unmapped_bai": {"path": "'
  
  + sys.argv[3] +
   
  '","class": "File"  },  "merged_output_bam": {    "path": "'
  
  + sys.argv[4] + 
  
  '","class": "File"  },  "merged_output_unmapped_bam": {    "path":"' 
  
  + sys.argv[5] + 
   
  '","class": "File"  },  "merged_output_bai": {    "path": "'
  
  + sys.argv[6] +
   
  '","class": "File"  }}')