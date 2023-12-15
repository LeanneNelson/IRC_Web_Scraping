from bs4 import BeautifulSoup as bs
import lxml
import requests
import streamlit as st

st.set_page_config("IRC_Lookup", None, "wide")

st.title("IRC Lookup")
irc = st.text_input("IRC")

if irc:
    soup = bs(requests.get("https://www.law.cornell.edu/uscode/text/26/"+irc.upper()).text, "lxml")
    soup = soup.find("div", class_="section")
    for a in soup.findAll('a', href=True):
        a['href'] = "https://www.law.cornell.edu"+str(a['href'])
    st.markdown(soup, unsafe_allow_html=True)

