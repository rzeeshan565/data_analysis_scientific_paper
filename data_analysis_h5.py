import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
input_file_name = f"{base_dir}//Conference_full_papers.xlsx"
out_folder = f"{base_dir}//Scientific_Practise_First_paper_draft _IEEE_double_column-2025"

# column names 
citation_col = "Number of citations under Google Scholar"
table_col = "Number of tables"
fig_graph_col = "Number of figures and graphs"
ref_col = "Number of references provided in the PDF"
conference_col = "Conference"
title_col = "Publication title"
conference_country_col = "Conference country"
authors_col = "Number of authors"
first_author_country_col = "Country of first author (as per publication date)"

# Load your Excel file (adjust the path and sheet name if needed)
df = pd.read_excel(input_file_name, engine="openpyxl")

# Clean column names: strip leading/trailing spaces
df.columns = df.columns.str.strip()

# Remove trailing spaces from values in conference column
df[conference_col] = df[conference_col].str.strip()
#print(df.head())  # Peek at your data

## Research question 1
# Selected features to correlate with the target
selected_features = [table_col, fig_graph_col, ref_col]
target_column = citation_col


# Compute correlation of each selected feature with the target
correlations = df[selected_features + [target_column]].corr()[target_column].drop(target_column)
#print(correlations)

# Set plot style
sns.set_theme(style="whitegrid", context="paper", font_scale=1.2)

# Width in inches for single-column fit (IEEE style)
width = 3.45  # approx. 88 mm
height = width * 0.75  # maintain aspect ratio

# Set font family and sizes for IEEE-like style
mpl.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "Times", "DejaVu Serif"],
    "axes.labelsize": 10,
    "axes.titlesize": 10,
    "font.size": 10,
    "legend.fontsize": 9,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9
})


correlations = pd.Series({
    "Nr. of Tables": correlations[table_col],
    "Nr. of Figures and graphs": correlations[fig_graph_col],
    "Nr. of References": correlations[ref_col],
}).sort_values()

# Create horizontal barplot
plt.figure(figsize=(width, height))
correlations.plot(kind="barh", color="teal", edgecolor="black")

plt.xlabel("Pearson Correlation Coefficient")
plt.title("Correlation with Citation Count")
plt.tight_layout()
plt.savefig(f"{out_folder}//correlation_plot.pdf", dpi=600, bbox_inches="tight", format="pdf")

# uncomment below to generate correlation of [# of tables, figure/graph, reference] against citation count graph
'''
plt.show()
'''

## Research question 2

#  group by conference name and aggregate by sum (for citations count)
grouped = df.groupby(conference_col, as_index=False).sum(numeric_only=True)

# Sort for better readability
grouped_df = grouped.sort_values(target_column, ascending=False)
#print(grouped_df[[conference_col, citation_col]])

# Create the line plot
plt.figure(figsize=(width, height))
sns.lineplot(
    data=grouped_df,
    x=conference_col,
    y=target_column,
    marker="o",
    color="teal"
)

# Enhance aesthetics
plt.xticks(rotation=45, ha="right")
plt.xlabel("Conference")
plt.ylabel("Total Citation Count")
plt.title("Citation Count by Conference", fontsize=14)
plt.tight_layout()

# Save high-res figure
plt.savefig(f"{out_folder}//citation_by_conference.pdf", dpi=600, bbox_inches="tight", format="pdf")

# uncomment to generate conference vs citation count graph
'''
plt.show()
'''


#print(df[[title_col, conference_col, citation_col]])

# Find the title with the maximum citation count
top_conference = grouped_df.loc[grouped_df[citation_col].idxmax(), conference_col]
#print(top_conference)

# filter original DF against top_conference
top_conference_df = df[df[conference_col] == top_conference].copy()
#print(top_conference_df[[title_col, citation_col]])

# Truncate long names to first 15 characters and add ellipsis
top_conference_df[title_col] = top_conference_df[title_col].apply(lambda x: x[:15] + "..." if isinstance(x, str) and len(x) > 15 else x)


# Create the line plot
plt.figure(figsize=(width, height))
sns.lineplot(
    data=top_conference_df,
    x=title_col,
    y=citation_col,
    marker="o",
    color="teal"
)

# Enhance aesthetics
plt.xticks(rotation=45, ha="right")
plt.xlabel("Publication Title")
plt.ylabel("Total Citation Count")
plt.title("Top Conference Citation distribution", fontsize=14)
plt.tight_layout()

# Save high-res figure
plt.savefig(f"{out_folder}//top_conference_citation_distribution.pdf", dpi=600, bbox_inches="tight", format="pdf")

# uncomment to generate top_conference_citation_distribution graph
'''
plt.show()
'''

## Research question 3 (find corelation of geographic distribution of the conferences and the authors to citations count)
target_col = citation_col

df_encoded = pd.get_dummies(
    df[[conference_country_col, first_author_country_col]],
    drop_first=True  # to avoid dummy variable trap
)

# Add citations
df_encoded[target_col] = df[target_col]

# Compute correlation of encoded features vs citations
correlation_series = df_encoded.corr()[target_col].drop(target_col).sort_values(ascending=False)

#print("Categorical feature correlations with citations:")
#print(correlation_series)

# Truncated, cleaned interesting data
correlations = {
    "Conference country: Cyprus": correlation_series[f"{conference_country_col}_Cyprus"],
    "First author: UK": correlation_series[f"{first_author_country_col}_UK"],
    "First author: Greece": correlation_series[f"{first_author_country_col}_Greece"],
    "First author: UAE": correlation_series[f"{first_author_country_col}_UAE"],
    "First author: Norway": correlation_series[f"{first_author_country_col}_Norway"],
    "First author: Japan": correlation_series[f"{first_author_country_col}_Japan"],
    "First author: Germany": correlation_series[f"{first_author_country_col}_Germany"],
    "First author: USA": correlation_series[f"{first_author_country_col}_USA"],
    "First author: China": correlation_series[f"{first_author_country_col}_China"],
    "First author: Belgium": correlation_series[f"{first_author_country_col}_Belgium"],
    "First author: Pakistan": correlation_series[f"{first_author_country_col}_Pakistan"],
    "Conference country: Slovakia": correlation_series[f"{conference_country_col}_Slovakia"],
    "First author: Taiwan": correlation_series[f"{first_author_country_col}_Taiwan"],
    "First author: India": correlation_series[f"{first_author_country_col}_India"],
}

# Sort and prepare
corr_series = pd.Series(correlations).sort_values()

# Convert Series to DataFrame
corr_df = corr_series.reset_index()
corr_df.columns = ["Geo-Category", "Correlation"]
corr_df["Geo-Category"] = corr_df["Geo-Category"].astype(str).str.strip()

# Set style
sns.set(style="whitegrid", context="paper")
plt.figure(figsize=(width, height))

# Plot
sns.barplot(
    data=corr_df,
    x="Correlation",
    y="Geo-Category",
    color="teal",
    edgecolor="black"
)
plt.xlabel("Pearson Correlation with Citation Count")
plt.title("Geo-Categorical Correlation with Citations", fontsize=10)
plt.tight_layout()
plt.savefig(f"{out_folder}//geo_citation_correlations.pdf", dpi=600, bbox_inches="tight")

# uncomment to generate to graph corelation of geographic distribution of the conferences and the authors to citations count
'''
plt.show()
'''