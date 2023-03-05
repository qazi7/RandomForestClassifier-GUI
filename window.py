from asyncio.windows_events import NULL
from tkinter import *
import pandas as pd
import numpy as np
from sklearn.impute  import SimpleImputer
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import MinMaxScaler
import warnings
warnings.filterwarnings("ignore")
import smtplib
import os
import ssl
from email.message import EmailMessage

c = pd.read_csv("D:/biohackathon/c.csv")
l = pd.read_csv("D:/biohackathon/l.csv")

c.dropna(subset=['CDR'],inplace=True)

l= l.rename(columns={'EDUC':'Educ'})
l.drop(columns=['Subject ID','MRI ID','Group','Visit','MR Delay'],inplace=True)

data = pd.concat([c,l])
data.iloc[:,0]=data.iloc[:,0].map({'F':0, 'M':1})
data.iloc[:,1]=data.iloc[:,1].map({'L':0, 'R':1})

#Right -> 1
#Left - > 0
#Male -> 1
#Female -> 0

c['Educ'] = MinMaxScaler().fit_transform(np.array(c['Educ']).reshape(-1,1))
l['Educ'] = MinMaxScaler().fit_transform(np.array(l['Educ']).reshape(-1,1))

imputer = SimpleImputer ( missing_values = np.nan,strategy='most_frequent')
imputer.fit(data[['SES']])
data[['SES']] = imputer.fit_transform(data[['SES']])
imputer = SimpleImputer ( missing_values = np.nan,strategy='median')
imputer.fit(data[['MMSE']])
data[['MMSE']] = imputer.fit_transform(data[['MMSE']])

le = preprocessing.LabelEncoder()
data['CDR'] = le.fit_transform(data['CDR'].values)
data[['SES','MMSE']] = data[['SES','MMSE']].astype(int)

y = data.iloc[:,6]
x = data.iloc[:,[0,1,2,3,4,5,7,8,9]]

X_train, X_test, y_train, y_test = train_test_split(x, y, random_state = 42,test_size=0.3)

clfrf = RandomForestClassifier() 
clfrf.fit(X_train, y_train)
y_pred_rf = clfrf.predict(X_test)

print(accuracy_score(y_test, y_pred_rf))  


def ml():

    print("Brain Button Clicked")

    entry10.insert(END,"\nPlease Wait.......\n")

    if(entry0.get()=="Male" or entry0.get()=="male" or entry0.get()=="M" or entry0.get()=="m"):
        x1 = 1
    else:
        x1 = 0
    print(x1)

    if(entry1.get()=="Right" or entry1.get()=="right" or entry1.get()=="R" or entry1.get()=="r"):
        x2 = 1
    else:
        x2 = 0
    print(x2)

    x3 = int(entry2.get())
    print(x3)

    if(entry3.get()=="NA" or entry3.get()=="na" or entry3.get()=="" ):
        x4 = 0
    elif(entry3.get()=='School' or entry3.get()=='school' or entry3.get()=='high school' or entry3.get()=='High School'):
        x4 = 0.25
    elif(entry3.get()=='College' or entry3.get()=='college' or entry3.get()=='UG'):
        x4 = 0.50
    elif(entry3.get()=='Masters' or entry3.get()=='PG'):
        x4 = 0.75
    elif(entry3.get()=='PHD' or entry3.get()=='Ph.d'):
        x4 = 1
    print(x4)

    x5 = int(entry4.get())
    print(x5)
    x6 = int(entry5.get())
    print(x6)
    x7 = int(entry8.get())
    print(x7)
    x8 = float(entry6.get())
    print(x8)
    x9 = float(entry7.get())
    print(x9)
   
    print("ML ENGAGED")
    

    arr=[[x1,x2,x3,x4,x5,x6,x7,x8,x9]]

    print(clfrf.predict((arr)))

    #[[0]] -> No Dementia
    #[[1]] -> Mild Dementia
    #[[2]] -> Moderate Dementia
    #[[3]] -> Severe Dementia
    if (clfrf.predict((arr))==[[0]]):
        txt = "DEMPRED PREDICTION: \nNo Brain Damage \nNO DEMENTIA"
        entry10.insert(END,txt)
    if (clfrf.predict((arr))==[[1]]):
        txt = "DEMPRED PREDICTION: \nLight Brain Damage, \nchances of \nMILD DEMENTIA"
        entry10.insert(END,txt)
    if (clfrf.predict((arr))==[[2]]):
        txt = "DEMPRED PREDICTION: \nMild Brain Damage, \nchances of \nMODERATE DEMENTIA"
        entry10.insert(END,txt)
    if (clfrf.predict((arr))==[[3]]):
        txt = "DEMPRED PREDICTION: \nExtensive Brain Damage, \nchances of \nSEVERE DEMENTIA"
        entry10.insert(END,txt)
    return txt

def stmp():

    print("Mail Button Clicked")
   
    rec_email=entry9.get()
    print(rec_email)


    sender_email="dementiapredictor@gmail.com"
    password=os.environ.get("DB_Pass")
    print(password)

    txt1 = ml()

    subject="Dementia Prediction"
    body = """
Gender : {}
Dominant Hand : {}
Age : {}
Education Level : {}
Socio Economic Status (1-5) : {}
Mini Mental State Examiantion : {}
Total Intercranial Volume : {}
Normalize Whole Brain Volume : {}
Atlas Scaling Factor : {}
\n\n{}\n\n
~from the developers of DemPred.
    """.format(entry0.get(),entry1.get(),entry2.get(),entry3.get(),entry4.get(),entry5.get(),entry6.get(),entry7.get(),entry8.get(),txt1)
    # body = ("HELLO", entry0.get())

    print(body)

    em = EmailMessage()
    em['From'] = sender_email
    em['To'] = rec_email
    em['Subject'] = subject
    em.set_content(body)



    # Add SSL (layer of security)
    context = ssl.create_default_context()
    
    # Log in and send the email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(sender_email, password)
        smtp.sendmail(sender_email, rec_email, em.as_string())

    entry10.insert(END,"\n\nReport sent ✅ !")

window = Tk()

window.geometry("1133x744")
window.title("DemPred")
window.wm_iconbitmap("D:/biohackathon/pyfile/Proxlight_Designer_Export/a.ico")

window.configure(bg = "#ffffff")
canvas = Canvas(
    window,
    bg = "#ffffff",
    height = 744,
    width = 1133,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge")
canvas.place(x = 0, y = 0)

background_img = PhotoImage(file = f"D:/biohackathon/pyfile/Proxlight_Designer_Export/background.png")
background = canvas.create_image(
    250.5, 375.0,
    image=background_img)

img0 = PhotoImage(file = f"D:/biohackathon/pyfile/Proxlight_Designer_Export/img0.png")
b0 = Button(
    image = img0,
    borderwidth = 0,
    highlightthickness = 0,
    command = ml,
    relief = "flat")

b0.place(
    x = 835, y = 33,
    width = 224,
    height = 180)

img1 = PhotoImage(file = f"D:/biohackathon/pyfile/Proxlight_Designer_Export/img1.png")
b1 = Button(
    image = img1,
    borderwidth = 0,
    highlightthickness = 0,
    command=stmp,
    relief = "flat")

b1.place(
    x = 867, y = 645,
    width = 159,
    height = 44)

entry0_img = PhotoImage(file = f"D:/biohackathon/pyfile/Proxlight_Designer_Export/img_textBox0.png")
entry0_bg = canvas.create_image(
    610.5, 83.0,
    image = entry0_img)

entry0 = Entry(
    bd = 0,
    bg = "#d6d6d6",
    highlightthickness = 0,
    font="Montserrat 16")

entry0.place(
    x = 467, y = 61,
    width = 290,
    height = 42)

entry1_img = PhotoImage(file = f"D:/biohackathon/pyfile/Proxlight_Designer_Export/img_textBox1.png")
entry1_bg = canvas.create_image(
    610.5, 148.0,
    image = entry1_img)

entry1 = Entry(
    bd = 0,
    bg = "#d9d9d9",
    highlightthickness = 0,
    font="Montserrat 16")

entry1.place(
    x = 467, y = 126,
    width = 290,
    height = 42)

entry2_img = PhotoImage(file = f"D:/biohackathon/pyfile/Proxlight_Designer_Export/img_textBox2.png")
entry2_bg = canvas.create_image(
    610.5, 213.0,
    image = entry2_img)

entry2 = Entry(
    bd = 0,
    bg = "#d9d9d9",
    highlightthickness = 0,
    font="Montserrat 16")

entry2.place(
    x = 467, y = 191,
    width = 290,
    height = 42)

entry3_img = PhotoImage(file = f"D:/biohackathon/pyfile/Proxlight_Designer_Export/img_textBox3.png")
entry3_bg = canvas.create_image(
    610.5, 278.0,
    image = entry3_img)

entry3 = Entry(
    bd = 0,
    bg = "#d9d9d9",
    highlightthickness = 0,
    font="Montserrat 16")

entry3.place(
    x = 467, y = 256,
    width = 290,
    height = 42)

entry4_img = PhotoImage(file = f"D:/biohackathon/pyfile/Proxlight_Designer_Export/img_textBox4.png")
entry4_bg = canvas.create_image(
    610.5, 342.5,
    image = entry4_img)

entry4 = Entry(
    bd = 0,
    bg = "#d9d9d9",
    highlightthickness = 0,
    font="Montserrat 16")

entry4.place(
    x = 467, y = 321,
    width = 290,
    height = 41)

entry5_img = PhotoImage(file = f"D:/biohackathon/pyfile/Proxlight_Designer_Export/img_textBox5.png")
entry5_bg = canvas.create_image(
    610.5, 407.0,
    image = entry5_img)

entry5 = Entry(
    bd = 0,
    bg = "#d9d9d9",
    highlightthickness = 0,
    font="Montserrat 16")

entry5.place(
    x = 467, y = 385,
    width = 290,
    height = 42)

entry6_img = PhotoImage(file = f"D:/biohackathon/pyfile/Proxlight_Designer_Export/img_textBox6.png")
entry6_bg = canvas.create_image(
    610.5, 537.0,
    image = entry6_img)

entry6 = Entry(
    bd = 0,
    bg = "#d9d9d9",
    highlightthickness = 0,
    font="Montserrat 16")

entry6.place(
    x = 467, y = 515,
    width = 290,
    height = 42)

entry7_img = PhotoImage(file = f"D:/biohackathon/pyfile/Proxlight_Designer_Export/img_textBox7.png")
entry7_bg = canvas.create_image(
    610.5, 602.0,
    image = entry7_img)

entry7 = Entry(
    bd = 0,
    bg = "#d9d9d9",
    highlightthickness = 0,
    font="Montserrat 16")

entry7.place(
    x = 467, y = 580,
    width = 290,
    height = 42)

entry8_img = PhotoImage(file = f"D:/biohackathon/pyfile/Proxlight_Designer_Export/img_textBox8.png")
entry8_bg = canvas.create_image(
    610.5, 472.0,
    image = entry8_img)

entry8 = Entry(
    bd = 0,
    bg = "#d9d9d9",
    highlightthickness = 0,
    font="Montserrat 16")

entry8.place(
    x = 467, y = 450,
    width = 290,
    height = 42)

entry9_img = PhotoImage(file = f"D:/biohackathon/pyfile/Proxlight_Designer_Export/img_textBox9.png")
entry9_bg = canvas.create_image(
    490.5, 667.0,
    image = entry9_img)

entry9 = Entry(
    bd = 0,
    bg = "#d9d9d9",
    highlightthickness = 0,
    font="Montserrat 16")

entry9.place(
    x = 247, y = 645,
    width = 510,
    height = 42)

entry10_img = PhotoImage(file = f"D:/biohackathon/pyfile/Proxlight_Designer_Export/img_textBox10.png")
entry10_bg = canvas.create_image(
    940.5, 419.0,
    image = entry10_img)

entry10 = Text(
    bd = 0,
    bg = "#d9d9d9",
    highlightthickness = 0,
    font="Montserrat 16")

entry10.place(
    x = 803, y = 217,
    width = 270,
    height = 410)

window.resizable(False, False)
window.mainloop()