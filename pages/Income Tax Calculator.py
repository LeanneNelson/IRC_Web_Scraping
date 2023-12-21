import streamlit as st

st.set_page_config("Tax Calculator", None, "wide")


# # # # # # # # # # # # # # # # # # # # # # # # # # # #
# INITIAL VARIABLES                                   #
# Stuff I'm using multiple times throughout the file  #
# # # # # # # # # # # # # # # # # # # # # # # # # # # #
ss = st.session_state
tax_rates = [0, .10, .12, .22, .24, .32, .35, .37]
tax_brackets = {"Individual":        [0, 11000, 44725,  95375, 182100, 231250, 578125],
                "Separate":          [0, 11000, 44725,  95375, 182100, 231250, 578125],
                "Joint":             [0, 22000, 89450, 190750, 364200, 462500, 693750],
                "Head of Household": [0, 15700, 59850,  95350, 182100, 231250, 578100]}
above_line_deductions = {"Trade & Business":                                                         "tb",
                         "Trade & Business Reimbursed Expenses of Employees":                       "tbree",
                         "Trade & Business Performing Arts Expenses of Employees":                  "tbpaee",
                         "Losses from Sale / Exchange of Property":                                 "lsep",
                         "Rents & Royalties":                                                       "rr",
                         "Pension, Profit-Sharing, and Annuity Plans of Self Employed Individuals": "ppapsei",
                         "Education Loan Interest":                                                 "eli"}
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
    options.form_submit_button("Update Tax Options", use_container_width=True)
    options.radio("Filing Status",
                  ["Individual", "Joint", "Separate", "Head of Household"],
                  horizontal=True,                                                      key="fs")
    options.checkbox("Corporation",                                                     key="isCorporation")
    options.checkbox("Specified Service Trades or Businesses (SSTB)",                   key="isSSTB")
    options.radio("Tax Credit Type", ["Nonrefundable", "Refundable"], horizontal=True,  key="tct")
    options.multiselect("Above the Line Deduction Types", above_line_deductions.keys(), key="aldt")
    options.date_input("Mortgage Start Date", format="MM/DD/YYYY",                      key="msd")
    with options.expander("Find Value of Selected Deductions"):
        left_col, right_col = st.columns(2)
        with left_col:
            st.checkbox("Select All Above the Line Deductions", True,                   key="aald")
            if not ss.aald:
                st.multiselect("Above the Line Deductions",
                               list(above_line_deductions.keys())+["Net Capital"],
                               list(above_line_deductions.keys())+["Net Capital"],      key="aldv")
        with right_col:
            st.multiselect("Below the Line Deductions",
                           ["Standard", "Itemized", "Qualified Business Income"],
                           ["Standard", "Itemized", "Qualified Business Income"],       key="bldv")


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# GENERATE DEDUCTION VALUE LIST                                                                             #
# Concatenates all selected deductions from the options to be displayed later in the input & output section #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
if len(ss.bldv) == 3 and (ss.aald or len(ss.aldv) == len(above_line_deductions)+1):
    deduction_list = "All"
elif not ss.aald and len(ss.aldv)+len(ss.bldv) == 0:
    deduction_list = "No"
else:
    deduction_list = ""
    if len(ss.bldv) > 0:
        deduction_list += ", ".join(ss.bldv)
        if ss.aald or len(ss.aldv) > 0:
            deduction_list += ", "
    if ss.aald:
        deduction_list += ", All Above the Line"
    elif len(ss.aldv) > 0:
        deduction_list += ", ".join(ss.aldv)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# CALCULATING INPUTS & OUTPUTS                                          #
# Calculates variables to output & override user input where applicable #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
with input_col:
    calc = st.form("Input")
    calc.form_submit_button("Input & Output", use_container_width=True, disabled=True)

    # Adjusted Basis
    if is_valid(["basis", "adjustment"]):
        ss.ab = str(float(ss.basis) + float(ss.adjustment))

    # Gain Realized
    if is_valid(["ar", "ab"]):
        ss.gr = str(float(ss.ar) - float(ss.ab))

    # Total Above the Line Deduction
    ld = 0
    tald = 0
    if is_valid(["tb"]):
        tald += float(ss.tb)
    if is_valid(["tbree"]):
        tald += float(ss.tbree)
    if is_valid(["tbpaee"]):
        tald += float(ss.tbpaee)
    if is_valid(["lsep"]):
        tald += float(ss.lsep)
    if is_valid(["rr"]):
        tald += float(ss.rr)
    if is_valid(["ppapsei"]):
        tald += float(ss.ppapsei)
    if is_valid(["eli"]):
        tald += min(float(ss.eli), 2500)
    if is_valid(["nc"]):
        if float(ss.nc) < 0:
            nc = float(ss.nc) * -1
            tald += min(nc, 3000)
            if nc > 3000:
                ld = nc - 3000
    if tald > 0:
        ss.tald = str(tald)

    # Total Gross Income
    tgi = 0
    if is_valid(["salary"]):
        tgi += float(ss.salary)
    if is_valid(["ii"]):
        tgi += float(ss.ii)
    if is_valid(["oi"]):
        tgi += float(ss.oi)
    if tgi > 0:
        ss.tgi = tgi

    # Adjusted Gross Income
    if is_valid(["tald", "tgi"]):
        ss.agi = str(float(ss.tgi) - float(ss.tald))

    # Taxable Income & Below the Line Deductions
    if is_valid(["agi", "fs"]):

        # Standardized Deduction
        standard_deduction = {"Individual": 13850, "Separate": 13850, "Joint": 27700, "Head of Household": 20800}
        ss.sd = str(standard_deduction[ss.fs])

        # Itemized Deduction
        itemized_deduction = 0

        mi_limit = {"new": {"Separate": 375000, "Individual": 750000, "Joint": 750000, "Head of Household": 750000},
                    "old": {"Separate": 500000, "Individual": 1000000, "Joint": 1000000, "Head of Household": 1000000}}
        if is_valid(["mi"]):
            if ss.msd.year >= 2018:
                itemized_deduction += min(float(ss.mi), mi_limit["new"][ss.fs])
            else:
                itemized_deduction += min(float(ss.mi), mi_limit["old"][ss.fs])

        if is_valid(["cc"]):
            if float(ss.cc) < .60 * float(ss.agi):
                itemized_deduction += float(ss.cc)
            else:
                itemized_deduction += float(ss.agi)
                ld += float(ss.cc) - .60 * float(ss.agi)

        if is_valid(["salt"]):
            itemized_deduction += min(float(ss.salt), 10000)

        if is_valid(["me"]):
            if float(ss.me) > .075 * float(ss.agi):
                itemized_deduction += float(ss.me) - .075 * float(ss.agi)
        if itemized_deduction > 0:
            ss.id = str(itemized_deduction)

        # Pre-QBI Taxable Income
        if is_valid(["id"]):
            ti = float(ss.agi) - max(float(ss.id), float(ss.sd))
        else:
            ti = float(ss.agi)-float(ss.sd)
        ss.ti = str(ti)

        # Qualified Business Income Deduction
        if is_valid(["ww", "qbi", "basis"]):
            income_range = {"Individual":        {"min": 182100, "max": 232100, "phase": 50000},
                            "Separate":          {"min": 182100, "max": 232100, "phase": 50000},
                            "Head of Household": {"min": 182100, "max": 232100, "phase": 50000},
                            "Joint":             {"min": 364200, "max": 464200, "phase": 100000}}
            component = .2 * float(ss.qbi)
            if ti <= income_range[ss.fs].min or (not ss.isSSTB and ti <= income_range[ss.fs].max):
                ss.qbid = str(component)
            elif ti <= income_range[ss.fs].max or not ss.isSSTB:
                reduction = max(.5 * float(ss.ww), .25 * float(ss.ww) + .025 * float(ss.basis))
                ss.qbid = str(max(min(component, reduction),
                                  component -
                                  (reduction - component) *
                                  ((income_range[ss.fs].min - ti)/income_range[ss.fs].phase)))

            # Post-QBI Taxable Income (Refer to Pre-QBI Taxable Income if QBI Deduction is 0)
            if float(ss.qbid) > 0:
                ss.ti = str(ti - float(ss.qbid))

    # Leftover Deductions
    if ld > 0:
        ss.ld = ld

    # Surplus Investment Tax

    # Payroll Tax


    # Corporate Tax Liability
    if is_valid(["cti"]):
        ss.ctl = str(float(ss.cti) * .21)

    # Income Tax Liability
    if is_valid(["ti", "fs"]):
        tax_liability = 0
        remaining_tax_base = float(ss.ti)
        for i, rate in enumerate(tax_rates):
            if i+1 == len(tax_rates) or float(ss.ti) <= tax_brackets[ss.fs][i]:
                ss.tl = str(tax_liability + remaining_tax_base * rate)
                break

            if i > 0:
                tax_liability += (tax_brackets[ss.fs][i] - tax_brackets[ss.fs][i - 1]) * rate
                remaining_tax_base -= tax_brackets[ss.fs][i] - tax_brackets[ss.fs][i - 1]

    # Average Tax Rate
    if is_valid(["tl", "ti"]):
        ss.atr = str(float(ss.tl)/float(ss.ti))

    # Marginal Tax Rate
    if is_valid(["ti", "fs"]):
        for i, rate in enumerate(tax_rates):
            if i+1 == len(tax_rates) or float(ss.ti)+.01 < tax_brackets[ss.fs][i]:
                ss.mtr = str(rate)
                break

    # Value of Deductions
    if is_valid(["mtr"]):
        deduction = 0
        if not ss.aald:
            for ald in above_line_deductions:
                if ald in ss.aldv and is_valid([above_line_deductions[ald]]):
                    deduction += float(ss[above_line_deductions[ald]])
            if "Net Capital" in ss.aldv and is_valid(["nc"]):
                deduction += float(ss.nc)
        elif is_valid(["tald"]):
            deduction += float(ss.tald)
        if "Standard" in ss.bldv and is_valid(["sd"]):
            deduction += float(ss.sd)
        if "Itemized" in ss.bldv and is_valid(["id"]):
            deduction += float(ss.id)
        if "Qualified Business Income" in ss.bldv and is_valid(["qbid"]):
            deduction += float(ss.qbid)
        ss.dv = str(deduction * float(ss.mtr))

    # Amount Due
    if is_valid(["tl", "tc", "tct"]):
        tl = float(ss.tl)
        if is_valid(["ctl"]):
            tl += float(ss.ctl)
        if float(ss.tc) > tl and ss.tct == "Nonrefundable":
            ss.ad = "0"
        else:
            ss.ad = str(tl - float(ss.tc))

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # INITIALIZING INPUTS & OUTPUTS                                                   #
    # Initializes the input & output boxes for all calculatable variable in the page  #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    calc.text_input("Basis ($)",                                                                       key="basis")

    with calc.expander("Adjusted Basis and Realizations ($)"):
        st.text_input("Adjustment",                                                                    key="adjustment")
        st.text_input("Adjusted Basis",                                                                key="ab")
        st.text_input("Amount Realized",                                                               key="ar")
        st.text_input("Gain Realized",                                                                 key="gr")

    calc.text_input("W-2 Wages ($)",                                                                   key="ww")
    calc.text_input("Qualified Business Income ($)",                                                   key="qbi")

    with calc.expander("Capital ($)"):
        st.text_input("Net Capital",                                                                   key="nc")

    with calc.expander("Gross Income"):
        st.text_input("Salary ($)",                                                                    key="salary")
        st.text_input("Investment Income ($)",                                                         key="ii")
        st.text_input("Other Income ($)",                                                              key="oi")
        st.text_input("Total Gross Income ($)",                                                        key="tgi")

    with calc.expander("Above the Line Deductions ($)"):
        for ald in above_line_deductions:
            if ald in ss.aldt:
                st.text_input(ald, key=above_line_deductions[ald])
        st.text_input("Total Above the Line Deductions",                                               key="tald")

    calc.text_input("Adjusted Gross Income ($)",                                                       key="agi")

    with calc.expander("Itemized Deduction Sources ($)"):
        st.text_input("Mortgage Interest",                                                             key="mi")
        st.text_input("Charitable Contributions",                                                      key="cc")
        st.text_input("State and Local Tax (SALT)",                                                    key="salt")
        st.text_input("Medical Expenses",                                                              key="me")

    with calc.expander("Below the Line Deductions ($)"):
        st.text_input("Standard Deduction",                                                            key="sd")
        st.text_input("Itemized Deduction",                                                            key="id")
        st.text_input("Qualified Business Income Deduction",                                           key="gbid")

    calc.text_input("Value of "+deduction_list+" Deductions ($)",                                      key="dv")
    calc.text_input("Leftover Deductions for Next Year ($)",                                           key="ld")
    calc.text_input("Tax Base / Taxable Income ($)",                                                   key="ti")
    if ss.isCorporation:
        calc.text_input("Corporate Tax Base / Taxable Income ($)",                                     key="cti")

    with calc.expander("Tax Rates, Liability, and Credits"):
        st.text_input("Average Tax Rate (%)",                                                          key="atr")
        st.text_input("Marginal Tax Rate (%)",                                                         key="mtr")
        st.text_input("Tax Credits ($)",                                                               key="tc")
        if ss.isCorporation:
            st.text_input("Corporate Tax Liability ($)",                                               key="ctl")
        st.text_input("Tax Liability ($)",                                                             key="tl")

    calc.text_input("Amount Due ($)",                                                                  key="ad")
