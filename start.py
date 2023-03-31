import os

#the path of the file
path = os.path.dirname(os.path.abspath(__file__))
os.system(r"cd "+path)
os.system("streamlit run web.py")