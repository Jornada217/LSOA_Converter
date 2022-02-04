#!/usr/bin/env python
# coding: utf-8

# In[1]:
import os
from selenium import webdriver
import time
from os import path
from os.path import sep, join
from pathlib import Path


class driver():

    def geoconv(self, GeoTest):
        #return 'GeoConvertTest.csv'
        return GeoTest

    def dirdnwld(self):
        return os.getcwd()

    def chromedriv(self):
        return 'C:/***/**/Learning_Projects/venv/Scripts/chromedriver.exe'

    def drive(self):  # Step 2: set chrome driver
        chromeOptions = webdriver.ChromeOptions()
        prefs = {'download.default_directory': self.dirdnwld()}
        chromeOptions.add_experimental_option('prefs', prefs)
        chromeOptions.add_argument('headless')
        # Set the driver's directory
        chromeDriver = self.chromedriv()
        chrm = webdriver.Chrome(executable_path=chromeDriver, options=chromeOptions)
        print('The Webdriver is')
        print(type(chrm))
        return chrm


class geoconverter():

    def fjoin(self, *args, **kwargs):
        return join(*args, **kwargs).replace(sep, '/')

    def djoin(self, *args, **kwargs):
        return join(*args, **kwargs).replace(sep, '\\')

    def __init__(self):
        self.drive = driver()

    def autofill(self, sr, b, geoconv_src=None):
        self.stand()
        self.file(sr,b)
        self.step2a(sr, b)  # Convert
        self.rename(b)
        self.drive.geoconv(b)

    def stand(self): #Save for later: This is the last file standing before
                     # the process starts.
        dir = self.drive.dirdnwld()
        last_stand = max(
            [f for f in os.listdir(dir)],
            key=lambda xa: os.path.getctime(os.path.join(dir, xa)))
        lfs = os.path.splitext(last_stand)[0]
        return lfs

    def file(self, src, g):
        file_geo = self.drive.geoconv(g)
        file_src = join(src, file_geo)
        file_path = path.abspath(file_src)
        return self.fjoin(file_path)

    parser_1a = ['//*[@id="help-content"]/p/a', '//*[@id="convertRadioButton"]', '//*[@id="Next"]',
                '//*[@id="sourcegeog"]/option[5]', '//*[@id="helpFooter"]/form[1]/p/input',
                '//*[@id="targetgeog"]/option[5]', '//*[@id="helpFooter"]/form[1]/p/input',
                '//*[@id="helpFooter"]/form[1]/table/tbody/tr[3]/td[3]/label/input',
                '//*[@id="Next"]', '//*[@id="fileUploadButton"]', '//*[@id="comma"]', '//*[@id="yes"]']

    parser_1b = ['Session initiated...', 'Select convert data...', 'Convert Data Selected',
                 'Select Source Geography: LSOA','LSOA Selected', 'Select Target Geography...',
                 'Target Geography -> "LSOA" Selected', 'Select Fixer 2001 Census to Fixed 2011 Census',
                 'Fixed 2001 Census -> Fixed 2011 Census Selected', 'Conversion parameters Confirmed',
                 'GeoConvertTest file is using csv...', 'GeoConvertTest file is using csv -> click']

    parser_2a = ['//*[@id="uploadinputfile"]', '//*[@id="helpFooter"]/form[1]/p/input',
                 '//*[@id="helpFooter"]/div[2]/p/a', '//*[@id="helpFooter"]/form/p[2]/input', ]

    parser_2b = ['Next...', 'Input File successfully uploaded.', 'Files Sucessfully Downloaded',
                 'Start again selected']

    def step2a(self, s, f):
        url = 'http://geoconvert.mimas.ac.uk/index.html'
        d = self.drive.drive()
        print(type(d))
        d.get(url)
        print('Step 2a Done')
        print('Start Step 3')
        # Initiate Session

        for i, j in zip(parser_1a, parser_1b):
            d.find_element_by_xpath(i).click()
            print(j)
            uploadGeo = d.find_element_by_id('uploadButton')
            uploadGeo.send_keys(self.file(s, f))

        # Check Column Delimiter Character or Header Row.
        # For more information on Input File requirements: http://geoconvert.mimas.ac.uk/help/input_files.htm

        for k, l in zip(parser_2a, parser_2b):
            d.find_element_by_xpath(k).click()
            print(l)

        # Close Navigator
        time.sleep(3)
        d.close()

    def rename(self,fl):
        dir = self.drive.dirdnwld()
        last_file = max(
            [f for f in os.listdir(dir)],
            key=lambda xa: os.path.getctime(os.path.join(dir, xa)))
        print('last_file is:', last_file)
        f_src = os.path.join(self.drive.dirdnwld(), last_file)
        dir_last = os.path.abspath(f_src)
        lfn = os.path.splitext(last_file)[0]
        print('lfn, last file name: ', lfn)
        filemain = os.path.splitext(self.drive.geoconv(fl))[0]
        print('Geoconvert file name: ', filemain)
        rename = (str(filemain) + '-converted')
        time.sleep(3)
        try:
            path = Path(dir_last)
            target = path.with_name(path.name.replace(lfn, rename))
            path.rename(target)
        except:
            print('File not found')

# In[ ]:
