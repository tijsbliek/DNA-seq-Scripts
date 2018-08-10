import sys

lijst = " ".join(sys.argv)
lijst = lijst.split("-")
f = (lijst[0].strip().split(" ")[-1]).strip()
if lijst[1] == "help" or lijst[1] == "h":
    print "This script converts a Bedtools genomecov txt into a gtf file\n\
tijs bliek (bliek@uva.nl)\n\n\
usage: python genomeCov_to_gtf.py [filename] [options]\n\n\
options:\n\
filename\t\tname and path of file to be converted, should be a bedtools genomecov .txt file\n\
\t\t\tthis text file should include regions of zero coverage; genomecov -bga.\n\n\
-coverage=[INT]\t\tmin level of coverage for it to produce a feature (default = 10)\n\
-gapsize=[INT]\t\tmaximum length of gap between two features for them to be fused to one (default = 100)\n\
-maxlength=[INT]\tmaximum length of a feature for it to be writen to gtf-file (default = 2000)\n\
-minlength=[INT]\tminimum length of a feature for it to be writen to gtf-file (default = 100)\n\n " 
    sys.exit()

args = {}
if len(lijst) > 1:
    lijst = lijst[1:]
    for i in lijst:
        i = i.split("=")
        args[i[0].strip()] = int(i[1].strip())
def GtG(inputFile, coverage = 10, gapsize = 100, maxlength = 2000, minlength = 100):
    cov = open(inputFile, "r")
    features = open((inputFile.split(".")[0] + ".gtf"), "w")
    new = False
    gap = True
    count = 0
    stop = 0
    chrom = "0"
    start = 0
    for line in cov:
        line = line.split("\t")
        if int(line[3]) >= coverage:
            if gap == True:
                if int(line[1]) - eind > gapsize:
                    if stop - start < maxlength and stop - start > minlength:
                        regel = "\t".join([chrom, "genomecov", 'feature', str(start), str(eind),"+","."\
                        "gene_id \"flank_"+str(count)+"\"; feature_id \"flank_"+str(count)+"\""])
                        features.write((regel+"\n"))
                        count += 1
                    new = False
                else:
                    gap = False
            if new == False:
                start = int(line[1])
                new = True
                gap = False
            if new == True:
                stop = int(line[2])
                chrom = line[0]
        else:
            eind = stop
            gap = True
    cov.close()
    features.close()
    return(count)

if "coverage" in args:
    a = args["coverage"]
else: a = 10
if "gapsize" in args:
    b = args["gapsize"]
else: b = 100
if "maxlength" in args:
    c = args["maxlength"]
else: c = 2000
if "minlength" in args:
    d = args["minlength"]
else: d = 100
print "name of input file:",f,"\nname of output file: ",f.split(".")[0] + ".gtf\
\nminimum depth of coverage:", a ,\
"\nmaximum length of gaps within a feature:",b,\
"\nminimum and maximum length of features:",c, " and ",d,\
"\nnumber of found features:", GtG(f,a,b,c,d)
