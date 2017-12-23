# -*- coding: utf-8 -*-
import os

from flask import Flask, render_template
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField
