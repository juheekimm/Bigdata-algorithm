from django.shortcuts import render
# from django.http import HttpResponse
# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# import seaborn as sns
# from ast import literal_eval
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.feature_extraction.text import CountVectorizer
# from sklearn.metrics.pairwise import cosine_similarity
# from datetime import datetime
# Create your views here.

def index(request):
    return HttpResponse("This is recommend test page ")
