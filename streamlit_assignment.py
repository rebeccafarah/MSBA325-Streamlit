import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv("e8f4cc52fe8355b98ffb42007eae48bb_20260912_174053.csv")

st.title("Healthcare Resources Across Lebanon")

st.write(
    "This website explores the availability of healthcare resources across Lebanese towns."
)


# -----------------------------
# INTERACTION 1: Choose resource
# -----------------------------

resource = st.selectbox(
    "Choose a healthcare resource",
    [
        "Pharmacies",
        "Hospitals",
        "Clinics",
        "Medical Centers",
        "Labs & Radiology"
    ]
)

resource_columns = {
    "Pharmacies": "Type and size of medical resources - Pharmacies",
    "Hospitals": "Type and size of medical resources - Hospitals",
    "Clinics": "Type and size of medical resources - Clinics",
    "Medical Centers": "Type and size of medical resources - Medical Centers",
    "Labs & Radiology": "Type and size of medical resources - Labs and Radiology "
}

selected_column = resource_columns[resource]


# -----------------------------
# VISUALIZATION 1
# Top 10 towns for selected resource
# -----------------------------

top10 = df.nlargest(10, selected_column)

fig1 = px.bar(
    top10,
    x=selected_column,
    y="Town",
    orientation="h",
    title=f"Top 10 Towns by Number of {resource}",
    labels={
        selected_column: f"Number of {resource}"
    }
)

st.plotly_chart(fig1, use_container_width=True)


# -----------------------------
# INSIGHT 1
# Distribution of selected resource
# -----------------------------

total_towns = len(df)

towns_without_resource = (df[selected_column] == 0).sum()
percent_without = (towns_without_resource / total_towns) * 100

top10_total = top10[selected_column].sum()
overall_total = df[selected_column].sum()
top10_share = (top10_total / overall_total) * 100

st.write(
    f"{percent_without:.1f}% of towns have no recorded {resource.lower()}, "
    f"while the top 10 towns account for {top10_share:.1f}% of all recorded "
    f"{resource.lower()} in the dataset."
)

with st.expander("Resource Filter"):
    st.write(
        "The filter lets the user focus on one type of healthcare resource at a time and see which towns have the highest numbers. I used a dropdown because it allows users to focus on one healthcare resource at a time instead of mixing several categories in the same chart.")



# -----------------------------
# INTERACTION 2
# Choose a town from the Top 10
# -----------------------------

town = st.selectbox(
    "Choose one of the top 10 towns to explore",
    top10["Town"]
)


# -----------------------------
# Prepare selected town data
# -----------------------------

selected_town = df[df["Town"] == town]

town_resources = pd.DataFrame({
    "Resource": [
        "Pharmacies",
        "Hospitals",
        "Clinics",
        "Medical Centers",
        "Labs & Radiology"
    ],

    "Count": [
        selected_town[
            "Type and size of medical resources - Pharmacies"
        ].iloc[0],

        selected_town[
            "Type and size of medical resources - Hospitals"
        ].iloc[0],

        selected_town[
            "Type and size of medical resources - Clinics"
        ].iloc[0],

        selected_town[
            "Type and size of medical resources - Medical Centers"
        ].iloc[0],

        selected_town[
            "Type and size of medical resources - Labs and Radiology "
        ].iloc[0]
    ]
})


# -----------------------------
# VISUALIZATION 2
# Healthcare profile of selected town
# -----------------------------

fig2 = px.treemap(
    town_resources,
    path=["Resource"],
    values="Count",
    title=f"Healthcare Resource Profile for {town}"
)

fig2.update_traces(textinfo="label+value")

st.plotly_chart(fig2, use_container_width=True)


# -----------------------------
# INSIGHT 2
# Healthcare variety in selected town
# -----------------------------

types_available = (town_resources["Count"] > 0).sum()

total_resources = town_resources["Count"].sum()

largest_resource = town_resources.loc[
    town_resources["Count"].idxmax()
]

st.write(
    f"{town} has {types_available} out of 5 healthcare resource types represented, "
    f"with {total_resources} recorded resources in total. "
    f"The largest category is {largest_resource['Resource']}, "
    f"with {largest_resource['Count']} recorded."
)


with st.expander("Town Filter"):
    st.write(
        "After choosing a resource, the user can select one of the top 10 towns and look at its healthcare profile in more detail. This helps keep the analysis focused instead of showing details for every town."
    )