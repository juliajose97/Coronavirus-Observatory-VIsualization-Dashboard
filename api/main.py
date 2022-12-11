import streamlit as st
from utils import *

st.set_page_config(page_title="COVID", page_icon=":ghost:", layout="wide")


def interactive_map():
    st.title(
        "Covid World Map: Confirmed Cases, Deaths, Recoveries, and Vaccination Statistics"
    )

    confirmed, deaths, recovered, vaccinated = st.tabs(
        ["Confirmed Cases", "Deaths", "Recovered", "Vaccinated"]
    )

    with confirmed:
        with st.spinner("Loading graphs..."):
            st.plotly_chart(get_confirmed(), use_container_width=True)
    with deaths:
        with st.spinner("Loading graphs..."):
            st.plotly_chart(get_deaths(), use_container_width=True)
    with recovered:
        with st.spinner("Loading graphs..."):
            st.plotly_chart(get_recovered(), use_container_width=True)
    with vaccinated:
        with st.spinner("Loading graphs..."):
            st.plotly_chart(get_vaccinated(), use_container_width=True)


def world_statistics():
    df = get_data()
    country = st.selectbox(
        "Which country?",
        list_of_countries(),
    )

    col1, col2, _, _, _, _ = st.columns(6)
    months = ["0" + str(x) for x in range(1, 10)]
    months.append("11")
    months.append("12")
    years = ["2020", "2021", "2022"]
    with col1:
        startMonth = st.selectbox("Start month", (months))
        endMonth = st.selectbox("End month", (months))
    with col2:
        startYear = st.selectbox("Start year", (years))
        endYear = st.selectbox("End year", (years))

    if st.button("get results"):
        total, result = get_stats(df, startMonth, startYear, endMonth, endYear, country)

        st.write("Total deaths in this time period:", total)
        progressbar(0.6)
        plots = get_plot_rate(result)

        st.pyplot(plots)


def covid_policies():
    df = get_data()
    country = st.selectbox(
        "Which country?",
        list_of_countries(),
    )

    col1, col2, _, _, _, _ = st.columns(6)
    months = ["0" + str(x) for x in range(1, 10)]
    months.append("11")
    months.append("12")
    years = ["2020", "2021", "2022"]
    with col1:
        startMonth = st.selectbox("Start month", (months))
        endMonth = st.selectbox("End month", (months))
    with col2:
        startYear = st.selectbox("Start year", (years))
        endYear = st.selectbox("End year", (years))

    if st.button("get policies - min cases"):
        policy = get_min_policy(df, startMonth, startYear, endMonth, endYear, country)

        st.write(
            "policies in this time period which lead to minimum cases are as follows:",
            policy,
        )

    if st.button("get policies - max cases"):
        policy = get_max_policy(df, startMonth, startYear, endMonth, endYear, country)

        st.write(
            "policies in this time period which lead to maximum cases are as follows:",
            policy,
        )

    (
        school_closing_policy,
        workplace_closing,
        cancel_events,
        gatherings_restrictions,
        transport_closing,
        stay_home_restrictions,
        internal_movement_restrictions,
        international_movement_restrictions,
        information_campaigns,
        testing_policy,
        contact_tracing,
        facial_coverings,
        vaccination_policy,
        elderly_people_protection,
    ) = get_policy_descriptions()

    st.write("School closing policy description", school_closing_policy)
    st.write("workplace closing  policy description", workplace_closing)
    st.write("cancelled events policy description", cancel_events)
    st.write(" gatherings restrictions policy description", gatherings_restrictions)
    st.write("transport closing policy description", transport_closing)
    st.write("stay home restrictions policy description", stay_home_restrictions)
    st.write(
        "internal movement restrictionspolicy description",
        internal_movement_restrictions,
    )
    st.write(
        "international movement restrictions policy description",
        international_movement_restrictions,
    )
    st.write(" information campaigns policy description", information_campaigns)
    st.write("testing policy description", testing_policy)
    st.write("contact tracing policy description", contact_tracing)
    st.write("facial coverings policy description", facial_coverings)
    st.write("vaccination policy description", vaccination_policy)
    st.write("elderly people protection description", elderly_people_protection)


def search_engine():
    query = st.text_input("Search for an article")
    # milvus search limit - 16384
    no_of_results = st.slider(
        "number of search results", min_value=10, max_value=16384, value=10
    )
    if query:
        txt = f'<p style="font-style:italic;color:gray;">Showing top {no_of_results} related articles</p>'
        st.markdown(txt, unsafe_allow_html=True)
        search_param = {
            "query": query,
            "no_of_results": no_of_results,
        }
        with st.spinner("Searching..."):
            articles = get_articles(search_param=search_param)

            for i in articles:
                title, summary, authors, link = i
                if not title:
                    st.write("Title Not Available")
                else:
                    st.title(title)
                if not authors:
                    st.write("Author Information Not Available")
                else:
                    st.write(authors)
                if not summary:
                    st.write("Abstract Not Available")
                else:
                    st.write(summary)
                if not link:
                    st.write("URL Not Available")
                else:
                    st.markdown("[View Paper](%s)" % link)


page_names_to_funcs = {
    "Interactive Map": interactive_map,
    "Policy Measures": covid_policies,
    "World Statistics": world_statistics,
    "Search Engine": search_engine,
}

pages = st.sidebar.selectbox("What would you like to do?", page_names_to_funcs.keys())
page_names_to_funcs[pages]()
