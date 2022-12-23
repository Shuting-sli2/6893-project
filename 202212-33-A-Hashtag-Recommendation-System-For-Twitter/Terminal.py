#!/usr/bin/env python
# coding: utf-8

# In[1]:


from Project1 import *
from Project2 import *
from Trend import *
import tkinter
import webbrowser
import os


# In[2]:


def play():
    try:
        twitter_id = int(name_var.get())
        print(twitter_id)
    except ValueError:
        print("The input user id format is wrong. Please reenter enter a valid id.")
    BEARER_TOKEN = name_var2.get()
    consumer_key = name_var3.get()
    consumer_secret = name_var4.get()
    try:
        Output.insert(tkinter.END, 'Start getting tweets...\n')
        Twitter_tweets(twitter_id, BEARER_TOKEN)
        Output.insert(tkinter.END, 'Finish getting tweets...\n')
        Output.insert(tkinter.END, 'Start getting mentions...\n')
        Twitter_mentions(twitter_id, BEARER_TOKEN)
        Output.insert(tkinter.END, 'Finish getting mentions...\n')
        Output.insert(tkinter.END, 'Start getting trends...\n')
        Get_Trends('YwjSpr3oPZjPg2mDxghAJ4ing', 'SN0Jb3iwE93eN0BoJSRWkWptPXI628ECA5ce1Yapeg81SoY6Up')
        Output.insert(tkinter.END, 'Finish getting trends...\n')
        Output.insert(tkinter.END, 'Start the website for recommendation...\n')
        webbrowser.open_new_tab("http://127.0.0.1:8887/")
    except ValueError:
        print("Please check the id number and Bearer Token")


# In[3]:


parent_widget = tkinter.Tk()
parent_widget.geometry("700x400")
parent_widget.title("Recommendation for Twitter")
name_var=tkinter.StringVar()
name_var2=tkinter.StringVar()
name_var3=tkinter.StringVar()
name_var4=tkinter.StringVar()
label = tkinter.Label(parent_widget, text="Hey")
label['text'] = "Type Twitter User ID here."
label.pack()
entry_widget = tkinter.Entry(parent_widget, width = 40, textvariable = name_var)
entry_widget.insert(0, "199534925")
entry_widget.pack()
label2 = tkinter.Label(parent_widget, text="Hey")
label2['text'] = "Type Twitter BEARER TOKEN here."
label2.pack()
entry_widget2 = tkinter.Entry(parent_widget, width = 8, textvariable = name_var2)
entry_widget2.insert(0, "AAAAAAAAAAAAAAAAAAAAAEB8iQEAAAAA6SB8lbvTAqUpJ0z5sWfH31zflCI%3DiMklZddj0btPFc54VEIEYpfld1pxJdB37nGnUHRhtgQQgzjYpd")
entry_widget2.pack()
label3 = tkinter.Label(parent_widget, text="Hey")
label3['text'] = "Type Twitter consumer_key here."
label3.pack()
entry_widget3 = tkinter.Entry(parent_widget, width = 8, textvariable = name_var3)
entry_widget3.insert(0, "YwjSpr3oPZjPg2mDxghAJ4ing")
entry_widget3.pack()
label4 = tkinter.Label(parent_widget, text="Hey")
label4['text'] = "Type Twitter consumer_secret TOKEN here."
label4.pack()
entry_widget4 = tkinter.Entry(parent_widget, width = 8, textvariable = name_var4)
entry_widget4.insert(0, "SN0Jb3iwE93eN0BoJSRWkWptPXI628ECA5ce1Yapeg81SoY6Up")
entry_widget4.pack()
tkinter.Button(parent_widget, text="Check Recommendation", command=play).pack()
Output = tkinter.Text(parent_widget, height = 5, width = 25)
Output.pack()
tkinter.mainloop()


# In[ ]:




