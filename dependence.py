#! /usr/bin/env python

import os, sys
from os import path


def get_options():
    import os, os.path
    from optparse import OptionParser
 
    usage = "usage: %prog [options] \n"
    parser = OptionParser(usage=usage)

    parser.add_option("-v","--verbose", dest="verbose", default=False,action="store_true", help="Verbose output  ")
    parser.add_option("-p","--path", dest="path", type="string", default="./", help="path of  files to be analyzed ")

    (options, args) = parser.parse_args()
    return options, args


def main():
    """
    Read in data file and replicate it 
    """
    #        
    # Read options 
    #
    options, args = get_options()
    # Read in all files in bib_path directory 
    files = [f for f in os.listdir(options.path) if path.isfile(f)]
    mod_list = []
    f_list = []
    class_list = []
    # Loop over bib files 
    for f in files:
        print f
        col = f.split(".")
        if( len(col) > 1 ):

            if( col[1] == "py" ):
                # If .py open file 
                F = open(f,'r')
                lines = F.readlines()
                F.close
                f_list.append(col[0])
                for l in lines:
                    l_col = l.split()
                    if( len(l_col) ):
                        if( l_col[0] == "import"  ):
                            for mod_wc in l_col[1::]:
                                mod = mod_wc.split(",")
                                mod = mod[0].lstrip(' ').rstrip()
                                if( mod == "as" ):
                                    break 
                                if( mod not in mod_list ):
                                    mod_list.append(mod)
                                    if( options.verbose):
                                        print mod, "< added from >",l ," < in >",f
                        if( l_col[0] == "class"  ):
                            class_i = l_col[1].split(":")
                            class_i = class_i[0].lstrip(' ').rstrip()
                            class_list.append(class_i)
    log_line = ""
    print " imported exernal modules: "
    for mod in sorted(mod_list):
        if( mod not in f_list ):
            print "- {}".format(mod)
        else:
            log_line += "{} is in path /n".format(mod)
    print " defined classes:"
    for class_i in sorted(class_list):
        print " Class ",class_i
        
if __name__=="__main__":
    main()
