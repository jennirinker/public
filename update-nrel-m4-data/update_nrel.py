
if (__name__ == '__main__'):
    """ Do when called as script from command line.    
    """
    from URLDataDownload import updateDirectory

    # 20-Hz base URL and directory
    #   *** NO TRAILING SLASHES ***
    baseURL = 'http://wind.nrel.gov/MetData/' + \
        '135mData/M4Twr/20Hz/mat';
    basedir = 'G:\\data\\nrel-20Hz';

    # 10-min base URL and directory
    #   *** NO TRAILING SLASHES ***
##    baseURL = 'http://wind.nrel.gov/MetData/' + \
##        '135mData/M4Twr/10min/mat';
##    basedir = 'G:\\data\\nrel-10min';

    # update the directory, return list of err'd files
    errList = updateDirectory(baseURL,basedir);

    # print a comment if any errors
    if errList:
        print '\n{} file(s) '.format(len(errList)) \
            + 'with errors saved in errList.';

    # and that's it!
    print '\nScript complete.\n';

    
