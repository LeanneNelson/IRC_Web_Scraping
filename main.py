import math

from bs4 import BeautifulSoup as bs
import lxml
import re
import requests
import streamlit as st

def get_irc(irc, key):
    soup = bs(requests.get("https://www.law.cornell.edu/uscode/text/26/" + irc.upper()).text, "lxml")
    body = soup.find("div", class_="section")
    for a in body.findAll('a', href=True):
        a["href"] = "https://www.law.cornell.edu" + str(a["href"])
    sections = body.findAll(string=re.compile("section.*\d+"))
    st.markdown(body, unsafe_allow_html=True)
    for codes in sections:
        text = codes.getText()
        numbers = re.split(" |,", re.search("section.*(\d+)", text).group())
        for number in numbers:
            if re.search("\d", number):
                st.write("")
                st.write("")
                show_irc = st.checkbox("[Section " + str(number) + "](https://www.law.cornell.edu/uscode/text/26/" + str(number) + ")", key=str(key)+" "+number)
                key += 1
                if show_irc:
                    get_irc(number, key)

st.set_page_config("IRC_Lookup", None, "wide")

st.title("IRC Lookup")
irc_input = st.text_input("IRC")

if irc_input:
    get_irc(irc_input, 0)
