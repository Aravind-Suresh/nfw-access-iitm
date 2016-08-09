# @Author: aravind
# @Date:   2016-08-08T21:59:16+05:30
# @Last modified by:   aravind
# @Last modified time: 2016-08-08T22:43:07+05:30

from selenium import webdriver
import os
import getpass
import json

from selenium.common.exceptions import WebDriverException, NoSuchElementException

home_path = os.getenv('HOME')
base_path = home_path + os.sep + '.nfw'

try:
    input = raw_input
except NameError:
    pass

if not os.path.exists(base_path):
    os.mkdir(base_path)

out_file_path = base_path + os.sep + 'cred.json'

# Chrome driver
chrome_driver_path = 'https://sites.google.com/a/chromium.org/chromedriver/downloads'


def write_credentials(out_file_path, data):
    """
    Method to write credentials to data file
    """
    json.dump(data, open(out_file_path, 'w'))


def read_credentials(out_file_path):
    """
    Method to read credentials from data file.

    If data file doesn't exist, gets info & creates it.
    """
    cred = {}
    browser_attr = ['Chrome', 'Firefox']
    if not os.path.exists(out_file_path):
        print("============== NFW-IITM credentials [ LDAP ] ==============")
        cred['username'] = input('LDAP Username: ')
        cred['password'] = getpass.getpass('LDAP Password: ')
        while True:
            c = int(input(
                'Preferred browser [' + ''.join((str(i + 1) + '-' + b + ', ') for i, b in enumerate(browser_attr))[
                                        :-2] + ']: '))
            if c in [1, 2]:
                cred['browser'] = {}
                cred['browser']['name'] = browser_attr[c - 1]
                if c == 1:  # Chrome
                    while True:
                        try:
                            # Checks if /path/to/chromedriver exists in credentials
                            driver_path = cred['browser'].get('driverPath', base_path + os.sep + 'chromedriver')
                            webdriver.Chrome(driver_path)
                            cred['browser']['driverPath'] = base_path + os.sep + 'chromedriver'
                            break
                        except WebDriverException:
                            # Makes sure user downloads chromedriver & puts in appropriate location
                            print('Chrome driver needs to be installed. It can be installed from here: {}.'.format(
                                chrome_driver_path))
                            print('NOTE: Chrome version must be >= 51.0.2704.0')
                            input('Place it in {} & continue..'.format(base_path))
                            cred['browser']['driverPath'] = base_path + os.sep + 'chromedriver'
                break
            else:
                print('Incorrect choice. Try again')
        write_credentials(out_file_path, cred)
    else:
        cred = json.load(open(out_file_path, 'r'))
    return cred


def auth(driver, cred):
    """
    Method for automating login procedure
    """
    try:
        ele_un = driver.find_element_by_xpath("//input[@id='ft_un']")
        ele_un.send_keys(cred['username'])
        ele_pd = driver.find_element_by_xpath("//input[@id='ft_pd']")
        ele_pd.send_keys(cred['password'])
        driver.find_element_by_xpath("//input[@type='submit']").click()
    except NoSuchElementException:
        print('Already active or No internet connection')


def main():
    """
    The expected 'main()' function :)
    """
    while True:
        cred = read_credentials(out_file_path)

        try:
            driver = webdriver.__getattribute__(cred['browser']['name'])(cred['browser'].get('driverPath', ''))
            url = 'https://67.media.tumblr.com/tumblr_lmfix57faG1qhq4cpo1_400.gif'
            driver.get(url)

            auth(driver, cred)
            break
        except WebDriverException:
            # Makes sure user downloads chromedriver & puts in appropriate location
            print('Chrome driver needs to be installed. It can be installed from here: {}.'.format(
                chrome_driver_path))
            print('NOTE: Chrome version must be >= 51.0.2704.0')
            input('Place it in {} & continue..'.format(base_path))


if __name__ == '__main__':
    main()
