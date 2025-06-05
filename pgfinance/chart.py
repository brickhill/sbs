# TODO Make Candle optional.
# TODO Bollinger bands.
# TODO Date range.
# XXX Make slider optional.
# TODO Remove unused packages.

import datetime as dt
from dateutil.relativedelta import relativedelta
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pytz


class Chart:

    def __init__(self, symbol,
                 df, period="year",
                 candles=True,
                 centre=None,
                 filename=None):
        self.traces = 0
        self.period = period
        self.symbol = symbol
        self.df = df
        self.filename = filename
        # Work the range of the chart.
        if str(self.period).isdigit():
            self.df = self.df[-int(self.period):]
        elif self.period == "year":
            self.df = self.df[self.df.index >=
                              pytz.utc.localize(dt.datetime.now())
                              - relativedelta(years=1)]
        else:
            period = -1
        self.candles = candles
        self.create_candle_fig()  # Create the figure.
        self.show_plot_browser()

    def show_plot_browser(self,
                          width=1400,
                          height=800,
                          nticks=8,
                          line_traces=['MA10', 'MA30']
                          ):
        self.add_traces(line_traces=line_traces)
        self.update_layout(width=width, height=height, nticks=nticks)
        self.fig.show()
        if self.filename:
            self.fig.write_image(self.filename)

    def create_candle_fig(self):
        self.df.index.name = 'Date'
        self.fig = make_subplots(rows=3, cols=1, row_heights=[0.15, 0.7, 0.15])
        # self.fig = go.Figure()
        if self.candles is True:
            self.fig.add_trace(go.Candlestick(
                               x=self.df.index,
                               open=self.df.open,
                               high=self.df.high,
                               low=self.df.low,
                               close=self.df.close,
                               line=dict(width=1),
                               opacity=.7,
                               name="candles",
                               increasing_fillcolor="#24a06b",
                               decreasing_fillcolor="#cc2e3c",
                               increasing_line_color="#2ec886",
                               decreasing_line_color="#ff3a4c"), row=2, col=1)
#       # Experiment to annotate chart.
#       xx = '2024-11-01'
#       yy = self.df['close'][xx] * 1.01
#       self.fig.add_annotation(x=xx, y=yy,
#                    text=f'\U000025b2 buy', # 'Big black arrow up'.
#                    showarrow=True,
#                    arrowhead=4,
#                    arrowcolor="#ff0000",
#                    font=dict(
#                     # family="Courier New, monospace",
#                     size=16,
#                     color="#ff0000"
#                     ),
#                    row=2,
#                    col=1,
#                    yshift=10)

#       yy /= 1.1
#       self.fig.add_annotation(x=xx, y=yy,
#                    text=f'\U000025bc sell', # 'Big black arrow down'.
#                    showarrow=False,
#                    row=2,
#                    col=1,
#                    yshift=10)

        self.fig.add_trace(
            go.Bar(x=self.df.index, y=self.df.volume, name='volume'),
            row=3,
            col=1
        )

        self.fig.add_trace(go.Scatter(x=self.df.index, y=self.df.BOLL_low,
                           fill=None, name="Bollinger(low)",
                           line=dict(width=1),
                           line_shape="spline",), row=2, col=1)
        self.fig.add_trace(go.Scatter(x=self.df.index, y=self.df.BOLL_middle,
                           name="Bollinger(middle)",
                           fill="tonexty",
                           line=dict(width=1), line_shape="spline",
                           fillcolor='rgba(55, 10, 12, 0.1)'), row=2, col=1)
        self.fig.add_trace(
                        go.Scatter(x=self.df.index,
                                   y=self.df.BOLL_high,
                                   fill="tonexty",
                                   name="Bollinger(high)",
                                   line=dict(width=1),
                                   line_shape="spline",
                                   fillcolor='rgba(55, 150, 122, 0.1)'
                                   ),
                        row=2,
                        col=1
                        )

    def update_layout(self, width, height, nticks):
        self.fig.update_yaxes(
            gridcolor="#1f292f"
        )
        self.fig.update_xaxes(
            gridcolor="#1f292f",
            rangeslider=dict(
                visible=False
            ),
            nticks=nticks,
            rangebreaks=[
                dict(
                    # enabled=False,
                    bounds=['sat', 'mon']
                )
            ],
            type="date"
        )
        self.fig.update_layout(
            # width=width,
            # height=height,
            margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor="#2c303c",
            plot_bgcolor="#2c303c",
            font=dict(
                    size=8,
                    color="#e1e1e1"
                    )
        )

    def add_traces(self, line_traces):
        print(f"traces {self.traces}")
        # fill = "tonexty" if self.traces > 1 else
        for t in line_traces:
            self.traces += 1
            self.fig.add_trace(go.Scatter(
                x=self.df.index,
                y=self.df[t],
                fill="tonexty" if self.traces > 1 else None,
                line=dict(width=1),
                line_shape="spline",
                name=t
            ))
