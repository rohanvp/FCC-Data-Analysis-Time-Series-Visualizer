import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import calendar
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df=pd.read_csv('fcc-forum-pageviews.csv',parse_dates=['date'])
df=df.set_index('date')

# Clean data
df=df.loc[
        (df['value'] >= df['value'].quantile(0.025))
        & (df['value'] <= df['value'].quantile(0.975))
    ]


def draw_line_plot():
    # Draw line plot

    p1=df.copy()
    fig, ax = plt.subplots(figsize=(10,5))
    plt.title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')
    ax=plt.plot(p1.index,p1.values,color="red")

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar=df.copy()
    df_bar['year']=pd.DatetimeIndex(df_bar.index).year
    df_bar['month']=pd.DatetimeIndex(df_bar.index).month
    df_bar['month']=df_bar['month'].apply(lambda x: calendar.month_abbr[x])
  
    
    g = sns.catplot(
            data=df_bar,
            x="year",
            y="value",
            hue="month",
            kind="bar",
            legend=False,errorbar=None
        )
    
    
    g.set_xlabels("Years")
    g.set_ylabels("Average Page Views")
    plt.legend(loc='upper left',labels=[
                "January",
                "February",
                "March",
                "April",
                "May",
                "June",
                "July",
                "August",
                "September",
                "October",
                "November",
                "December",
            ],title='Months')

    # Save image and return fig (don't change this part)
    g.savefig('bar_plot.png')
    return g.fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    
    # REMOVING TWO OUTLIER VALUES
    df_box=df_box[df_box['value']!=df_box['value'].max()]
    df_box=df_box[df_box['value']!=df_box['value'].max()]
    df_box["year"] = [d.year for d in df_box.date]
    df_box["month"] = [d.strftime("%b") for d in df_box.date]

    months=[
                "Jan",
                "Feb",
                "Mar",
                "Apr",
                "May",
                "Jun",
                "Jul",
                "Aug",
                "Sep",
                "Oct",
                "Nov",
                "Dec",
            ]
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
    sns.boxplot(data=df_box,x=df_box['year'],y=df_box['value'],ax=ax1)
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Page Views')
    ax1.set_title('Year-wise Box Plot (Trend)')
    
    sns.boxplot(data=df_box,x=df_box['month'],y=df_box['value'],ax=ax2)
    ax2.set_xlabel('Month')
    ax2.set_ylabel('Page Views')
    ax2.set_title('Month-wise Box Plot (Seasonality)')
    ax2.set_xticklabels(months)

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
