# import pandas as pd

# df = pd.read_csv("E:/lang/MOVIE-RECOMMODATION-SYSTEM/model/data/top10K-TMDB-movies.csv")

# # print(df.head(2))

# titles = df['title'].tolist()

# with open('script.js', 'w') as js_file:
#     js_file.write("const movieTitles = [\n")
#     js_file.write(",\n".join([f'    "{title}"' for title in titles]))
#     js_file.write("\n];\n\n")
#     js_file.write("export default movieTitles;\n")

import pandas as pd

# Load your CSV file into a DataFrame
df = pd.read_csv('E:/lang/MOVIE-RECOMMODATION-SYSTEM/model/data/top10K-TMDB-movies.csv')

# Extract movie titles
titles = df['title'].tolist()

# Specify the output file and encoding as 'utf-8'
output_file = 'titles.js'

try:
    with open(output_file, 'w', encoding='utf-8') as js_file:
        js_file.write("const movieTitles = [\n")
        js_file.write(",\n".join([f'    "{title}"' for title in titles]))
        js_file.write("\n];\n\n")
        js_file.write("export default movieTitles;\n")
except UnicodeEncodeError as e:
    print(f"UnicodeEncodeError: {e}")
    # Handle the error as needed, such as skipping the problematic title
