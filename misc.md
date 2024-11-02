

# SNIA related
according to SNIA v2.0.1, document link: [tbd]

## flow: SNIA IOPs test

according to section 7.2 psedo code



### params mapping: 

R/W Mix: ```100/0, 95/5, 65/35, 50/50, 35/65, 5/95, 0/100```

bs(block size:KiB): ```0.5,4,8,16,32,64,128,1024```

### extra notes
```For PTS-E, WCD and AR=100:```PTS-E: eSSD, disable write cache, apply AR = 100

```For PTS-C, WCE and AR=75```:
PTS-C: cSSD, enable write cache, apply AR = 75
