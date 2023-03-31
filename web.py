import streamlit as st
import BeYourEars
from PIL import Image
import matplotlib.pyplot as plt
import os

# markdown
st.markdown('CPS 4951 PROJECT')

# title

left_column_1, right_column_1= st.columns(2)

right_column_1.image('img/logo.png')

left_column_1.title('Be Your Ears')
st.write('**The purpose of the project is to help the hearing impaired.**')
st.write('**It will try to translate voice to sign language.**')
st.write('~~It still exists some problems, such as the lack of database and wrong translation~~')
st.text('')
# button for record
if st.button('record voice (at most 5s)',help='click to start recording'):
    
    st.write('*recording*')
    bar=st.progress(0)
    BeYourEars.start_audio()
    bar.progress(100)
    st.write('done')
    res = BeYourEars.get_text()
    if res == 0:
        st.write('Please record again')


st.text('')
st.text('')
if st.button('translate to gesture', help='click to start translating'):
    list_word = BeYourEars.readText('voice.txt')
    list_path = BeYourEars.photos()
    length = len(list_path)
    if list_word==[]:
        st.write('Please record again')
    else:
        left_column, right_column= st.columns(2)
        colunm1,colunm2,colunm3,colunm4,colunm5,colunm6=st.columns(6)
        side = 0

        for i in reversed(range(length)):
            path_str='img/'+ list_path[i]+'.gif'
            if (os.path.exists(path_str) == True):
                if (side == 0):
                    left_column.image(path_str)
                    left_column.write(list_word[i])
                    side=1
                else:
                    right_column.image(path_str)
                    right_column.write(list_word[i])
                    side=0
            else:
                if (side == 0):
                    left_column.write('the database does not have the gesture of '+list_word[i])
                    side=1
                else:
                    right_column.write('the database does not have the gesture of '+list_word[i])
                    side=0


            
