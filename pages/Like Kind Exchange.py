import streamlit as st

st.set_page_config("Tax Calculator", None, "wide")


# # # # # # # # # # # # # # # # # # # # # # # # # # # #
# INITIAL VARIABLES                                   #
# Stuff I'm using multiple times throughout the file  #
# # # # # # # # # # # # # # # # # # # # # # # # # # # #
ss = st.session_state
input_col, option_col = st.columns(2)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# CHECKING FOR VALID KEY                                                      #
# Checks if a Streamlit Session State Key exists and if it has anything in it #
# Primarily to prevent key usage before initialization                        #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def is_valid(keys):
    for k in keys:
        if k not in ss or len(ss[k]) == 0:
            return False
    return True


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# INITIALIZING OPTIONS                                                      #
# Initializes the option section that appears on the right side of the page #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
with option_col:
    options = st.form("Options")


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# CALCULATING INPUTS & OUTPUTS                                          #
# Calculates variables to output & override user input where applicable #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
with input_col:
    calc = st.form("Input")
    calc.form_submit_button("Input & Output", use_container_width=True, disabled=True)
    first_col, second_col = calc.columns(2)

    if is_valid(["fvB"]):
        ss.arA = ss.fvB
    if is_valid(["abA"]):
        ss.grA = str(float(ss.arA) - float(ss.abA))


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# INITIALIZING INPUTS & OUTPUTS                                                   #
# Initializes the input & output boxes for all calculable variable in the page    #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
with first_col:
    st.text_input("Fair Market Value (FV)",              key="fvA")
    st.text_input("Adjusted Basis (AB)",                 key="abA")
    st.text_input("Debt (Like a Mortgage)",              key="dA")
    st.text_input("Amount Realized (AR)",                key="arA")
    st.text_input("Gain Realized (GR)",                  key="grA")
with second_col:
    st.text_input("Fair Market Value (FV)",              key="fvB")
    st.text_input("Adjusted Basis (AB)",                 key="abB")
    st.text_input("Debt (Like a Mortgage)",              key="dB")
    st.text_input("Amount Realized (AR)",                key="arB")
    st.text_input("Gain Realized (GR)",                  key="grB")

