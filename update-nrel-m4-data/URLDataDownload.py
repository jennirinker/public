def listURLTable(URL):
    """ List of elements from a table located online at specified URL.

        Args:
            URL (string): address to webpage with table
         
        Returns:
            listTable (list): list of table contents at URL
    """
    import requests                 # testing URLs
    from bs4 import BeautifulSoup   # web scraping

    # check URL
    result = requests.get(URL);

    # if request successful
    if result.status_code < 400:

        # initialize list of table contents
        listTable = [];

        # get table and extract rows
        URLdata = result.content;           # webpage contents
        soup = BeautifulSoup(URLdata);      # organize content
        table = soup.find('table');         # find table
        rows = table.find_all('tr');        # separate rows

        # loop through rows, cleaning and appending data to list
        for row in rows:
            cols = row.find_all('td');      # column in row
            cols = [ele.text.strip() for \
                    ele in cols];           # extract text
            if cols:
                newRow = [str(ele) for \
                    ele in cols if ele];    # remove empty, unicode -> str
                listTable.append(newRow)    # append to list

        return listTable

    # halt if URL request failed
    else:
        print 'Error: URL request failed. for ' + \
              URL;
        return []

def updateDirectory(baseURL,basedir):
    """ Update a directory at basedir so that the folders and .mat files match 
        that at the specified URL in baseURL. Returns a list of files with 
        issues loading the URL path.

        Args:
            baseURL (string): top-level URL to update
            basedir (string): corresponding top-level local directory to update
        
        Returns:
            errList (list): list of files with errors, if any
    """
    import os                       # testing existence of files
    from datetime import datetime   # checking mod dates
    import requests                 # testing URLs
    import urllib                   # downloading files

    print 'Entering ' + basedir;

    # format of date string on M4 website
    datestrfmt = '%d-%b-%Y %H:%M';

    # initialize error list
    errList = [];

    # get list of table elements on URL
    tableList = listURLTable(baseURL);

    # loop through rows in the table
    for row in tableList:
        
        ele = row[0];           # first column

        # if element is a folder
        if ('/' in ele):

            # create the URL/paths for subfolder
            foldname = ele.strip('/');
            foldURL  = '/'.join([baseURL,foldname]);
            foldpath = '\\'.join([basedir,foldname]);

            # make the local folder if it doesn't exist            
            if not os.path.isdir(foldpath):
                os.mkdir(foldpath);
                
            # recursivley update the subfolder, save any errors
            errList_new = updateDirectory(foldURL,foldpath);
            errList.extend(errList_new);

        # if element is a .mat file
        elif ('.mat' in ele):
            filename = ele;

            # create the URL/paths for specific file
            fileURL  = '/'.join([baseURL,filename]);
            filepath = '\\'.join([basedir,filename]);

            # if local file doesn't exist, download it
            if not os.path.exists(filepath):

                # check URL
                if (requests.get(fileURL).status_code < 400):

                    # download file
                    webFile = urllib.urlopen(fileURL);
                    with open(filepath,'wb') as locfile:
                        locfile.write(webFile.read());
                    webFile.close()

                # save error list if issue
                else:
                    print 'Error downloading {}'.format(filepath);
                    errList.extend([fileURL])

            # if the local file does exist
            else:
                
                # get the date last modified
                URLdatestr = row[1];
                URLmoddate = datetime.strptime(URLdatestr,datestrfmt)
                locmoddate = datetime.fromtimestamp( \
                    os.path.getmtime(filepath));

                # download it if the URL is newer than the local version
                if URLmoddate > locmoddate:

                    # check URL
                    if (requests.get(fileURL).status_code < 400):

                        # download file
                        webFile = urllib.urlopen(fileURL);
                        with open(filepath,'wb') as locfile:
                            locfile.write(webFile.read());
                        webFile.close()

                    # save error list if issue
                    else:
                        print 'Error downloading {}'.format(filepath);
                        errList.extend([fileURL])

    print '  Files at ' + basedir + ' are up to date.';

    return errList

