
# Task 2: A Line Plot with Pandas
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

try:
    with  sqlite3.connect('../db/lesson.db') as conn:
        print("Database created and connected successfully.")
        cursor = conn.cursor()

        sql_statement = """
        SELECT o.order_id,
            SUM(price * quantity) AS total_price
            FROM orders o 
        JOIN line_items l 
            ON o.order_id = l.order_id
        JOIN products p
            ON l.product_id = p.product_id
        GROUP BY o.order_id;
        """

        df = pd.read_sql_query(sql_statement, conn)
        print(df)

        def cumulative(row):
            totals_above = df['total_price'][0:row.name+1]
            return totals_above.sum()

        df['cumulative'] = df['total_price'].cumsum()

        # Line Plot
        df.plot(x="order_id", y="cumulative", kind="line", title="Cumulative revenue vs Orders")
        plt.xlabel("Orders")
        plt.ylabel("Cumulative revenue")
        plt.show()

except sqlite3.Error as e:
    print(f"An error occurred: {e}")

# Task 3: Interactive Visualizations with Plotly

import plotly.express as px
import plotly.data as pldata
df = pldata.wind(return_type='pandas')

print(df.head(10))
print(df.tail(10))

df['strength'] = df['strength'].str.replace(r'-\d+|\+', '', regex=True)
df['strength'] = df['strength'].astype(float)

fig = px.scatter(df, x='strength', y='frequency', color='direction',
                 title="Wind Data, Strength vs. Frequency", hover_data=["direction"])
fig.write_html("wind.html", auto_open=True)