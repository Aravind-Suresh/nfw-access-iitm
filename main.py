# @Author: aravind
# @Date:   2016-08-08T21:59:16+05:30
# @Last modified by:   aravind
# @Last modified time: 2016-08-08T22:43:07+05:30

from selenium import webdriver
import sys
import os
import getpass
import json

homePath = os.getenv('HOME')
basePath = homePath + os.sep + '.nfw'

if not os.path.exists(basePath):
    os.mkdir(basePath)

outFilePath = basePath + os.sep + 'cred.json'

# Chrome driver
chromeDriverPath = 'https://sites.google.com/a/chromium.org/chromedriver/downloads'

def writeCredentials(outFilePath, data):
    """
    Method to write credentials to data file
    """
    json.dump(data, open(outFilePath, 'w'))

def readCredentials(homePath, outFilePath):
    """
    Method to read credentials from data file.

    If data file doesn't exist, gets info & creates it.
    """
    cred = {}
    browserAttr = ['Chrome', 'Firefox']
    if not os.path.exists(outFilePath):
        print("============== NFW-IITM credentials [ LDAP ] ==============")
        cred['username'] = raw_input('LDAP Username: ')
        cred['password'] = getpass.getpass('LDAP Password: ')
        while True:
            c = int(raw_input('Preferred browser [' + ''.join((str(i+1) + '-' + b + ', ') for i,b in enumerate(browserAttr))[:-2] + ']: '))
            if c in [1, 2]:
                cred['browser'] = {}
                cred['browser']['name'] = browserAttr[c-1]
                if c == 1: # Chrome
                    while True:
                        try:
                            # Checks if /path/to/chromedriver exists in credentials
                            driverPath = cred['browser'].get('driverPath', None)
                            if driverPath is None:
                                driver = webdriver.Chrome()
                            else:
                                driver = webdriver.Chrome(driverPath)
                            break
                        except:
                            # Makes sure user downloads chromedriver & puts in appropriate location
                            print('Chrome driver needs to be installed. It can be installed from here: {}.'.format(chromeDriverPath))
                            print('NOTE: Chrome version must be >= 51.0.2704.0')
                            raw_input('Place it in {} & continue..'.format(basePath))
                            cred['browser']['driverPath'] = basePath + os.sep + 'chromedriver'
                            pass
                break
            else:
                print('Incorrect choice. Try again')
        writeCredentials(outFilePath, cred)
    else:
        cred = json.load(open(outFilePath, 'r'))
    return cred

def auth(driver, cred):
    """
    Method for automating login procedure
    """
    ele_un = driver.find_element_by_xpath("//input[@id='ft_un']")
    ele_un.send_keys(cred['username'])
    ele_pd = driver.find_element_by_xpath("//input[@id='ft_pd']")
    ele_pd.send_keys(cred['password'])
    driver.find_element_by_xpath("//input[@type='submit']").click()

def main():
    """
    The expected 'main()' function :)
    """
    cred = readCredentials(homePath, outFilePath)

    driver = webdriver.__getattribute__(cred['browser']['name'])()
    url = 'https://67.media.tumblr.com/tumblr_lmfix57faG1qhq4cpo1_400.gif'
    driver.get(url)

    auth(driver, cred)

if __name__ == '__main__':
    main()
