import streamlit as st

def load_css():

    st.markdown(
        """
<style>

/* ------------------------
BACKGROUND
------------------------ */

.stApp{
    background-color:#0E1117;
    color:white;
}

/* ------------------------
REMOVE DEFAULT PADDING
------------------------ */

.block-container{
    padding-top:1rem;
    padding-bottom:1rem;
    padding-left:2rem;
    padding-right:2rem;
}

/* ------------------------
TITLE
------------------------ */

.main-title{
    font-size:42px;
    font-weight:700;
    color:white;
    margin-top:20px;
    margin-bottom:8px;
    line-height:1.3;
    padding-top:10px;
    overflow:visible;
}
.sub-title{
    font-size:18px;
    color:#B8C1CC;
    margin-bottom:25px;
}

/* ------------------------
KPI CARD
------------------------ */

.metric-card{

    background:#161B22;

    border-radius:18px;

    padding:22px;

    text-align:center;

    border:1px solid #30363D;

    transition:.3s;

    box-shadow:0px 0px 12px rgba(0,255,100,.15);

}

.metric-card:hover{

    transform:translateY(-6px);

    box-shadow:0px 0px 25px rgba(0,255,100,.35);

}

/* ------------------------
PRICE CARD
------------------------ */

.price-card{

    background:linear-gradient(
    135deg,
    #00C853,
    #00ACC1
    );

    border-radius:22px;

    padding:30px;

    text-align:center;

    color:white;

    box-shadow:0px 0px 20px rgba(0,255,150,.25);

}

/* ------------------------
HEALTH CARD
------------------------ */

.health-card{

    background:#1E293B;

    border-radius:18px;

    padding:25px;

    text-align:center;

}

/* ------------------------
SUCCESS BUTTON
------------------------ */

.stButton>button{

    width:100%;

    background:#00C853;

    color:white;

    border:none;

    border-radius:12px;

    height:55px;

    font-size:18px;

    font-weight:bold;

}

.stButton>button:hover{

    background:#00E676;

}

/* ------------------------
SELECTBOX
------------------------ */

.stSelectbox{

    border-radius:12px;

}

/* ------------------------
NUMBER INPUT
------------------------ */

.stNumberInput{

    border-radius:12px;

}

/* ------------------------
SLIDER
------------------------ */

.stSlider{

    padding-top:10px;

}

/* ------------------------
SIDEBAR
------------------------ */

section[data-testid="stSidebar"]{

    background:#111827;

}

/* ------------------------
TABLE
------------------------ */

[data-testid="stDataFrame"]{

    border-radius:18px;

}

/* ------------------------
FOOTER
------------------------ */

.footer{

    text-align:center;

    color:#9CA3AF;

    padding-top:40px;

}

/* ------------------------
BADGES
------------------------ */

.good{

    background:#16A34A;

    padding:8px 18px;

    border-radius:20px;

    color:white;

}

.fair{

    background:#EAB308;

    padding:8px 18px;

    border-radius:20px;

    color:black;

}

.poor{

    background:#DC2626;

    padding:8px 18px;

    border-radius:20px;

    color:white;

}

.excellent{

    background:#00E676;

    padding:8px 18px;

    border-radius:20px;

    color:black;

}

/* ------------------------
SCROLLBAR
------------------------ */

::-webkit-scrollbar{

width:10px;

}

::-webkit-scrollbar-thumb{

background:#00C853;

border-radius:15px;

}

</style>

""",
        unsafe_allow_html=True
    )