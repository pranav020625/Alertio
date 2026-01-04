from flask import Flask,request,jsonify
from flask_cors import CORS
from threading import Thread
import time
import smtplib
from email.mime.text import MIMEText
from selenium import webdriver
from selenium.webdriver.chrome

