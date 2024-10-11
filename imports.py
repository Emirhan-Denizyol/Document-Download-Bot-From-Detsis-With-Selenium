import pandas as pd
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup
import os
from tqdm import tqdm
import glob
import subprocess
from selenium.webdriver.common.keys import Keys  # Keys modülünü buradan import ediyoruz
from webdriver_manager.chrome import ChromeDriverManager



# ChromeDriver'ın bulunduğu yol
driver_path = "C:/Users/Emirhan Denizyol/Desktop/chromedriver.exe"

rar_executable = 'C:/Program Files/WinRAR/rar.exe'

base_path="C:/Users/Emirhan Denizyol/Desktop/"

web_url="https://detsis.gov.tr/"