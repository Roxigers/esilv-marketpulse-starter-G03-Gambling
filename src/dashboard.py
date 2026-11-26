"""MarketPulse TD11. From the repository root, run python3 src/dashboard.py."""

from datetime import date
from urllib.parse import quote

from dash import Dash, dcc, html
import plotly.graph_objects as go

from main import build_market_snapshot


CYAN = "#22D3EE"
INDIGO = "#8795FF"
CSS = """
:root {
  color-scheme: dark;
  --bg: #070B14; --panel: #101827; --surface: #162133; --text: #F8FAFC;
  --muted: #a3b2c7; --line: #28364b; --cyan: #22D3EE; --blue: #3B82F6;
  --green: #10B981; --red: #F43F5E;
  --mono: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
}
* {box-sizing: border-box}
body {margin: 0; background: var(--bg); color: var(--text);
  font: 15px/1.45 -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  -webkit-font-smoothing: antialiased; font-variant-numeric: tabular-nums}
h1,h2,h3,p,dl,dd {margin: 0}
.shell {min-height: 100vh; background:
  radial-gradient(ellipse at 82% 2%, rgba(35,65,112,.20), transparent 45%), var(--bg)}
.wrap {width: min(1480px, 93%); margin-inline: auto}
.topbar {background: rgba(13,20,33,.92); border-bottom: 1px solid var(--line)}
.header-inner,.brand,.meta,.pair,.chart-head,.foot,.range,.series-name,.kpi-bottom {
  display: flex; align-items: center}
.header-inner {justify-content: space-between; gap: 20px; min-height: 74px}
.brand {gap: 12px}
.mark {width: 38px; height: 38px; border: 1px solid #285062; border-radius: 11px;
  background: linear-gradient(145deg,#183b4c,#0d1928); display: flex;
  align-items: center; justify-content: center; gap: 3px}
.mark i {width: 4px; border-radius: 1px; background: var(--cyan); transform: skewY(-20deg)}
.mark i:nth-child(1) {height: 9px}.mark i:nth-child(2) {height: 20px}.mark i:nth-child(3) {height: 14px}
.wordmark {font-weight: 760; letter-spacing: .09em; font-size: 18px}
.brand-sub,.overline,dt,.kpi-title,.range,th,.chip,.chart-unit,.foot,.tag,.mini-label {
  font-family: var(--mono)}
.brand-sub {font-size: 9px; color: var(--muted); letter-spacing: .12em}
.meta {gap: clamp(16px,2.5vw,42px)}
.meta div {padding-left: 16px; border-left: 1px solid var(--line)}
dt,.mini-label {font-size: 10px; color: var(--muted); text-transform: uppercase; letter-spacing: .08em}
dd {margin-top: 3px; font: 12px/1.4 var(--mono)}
.mode {color: #91e8ee}
.overview {display: flex; justify-content: space-between; align-items: flex-end;
  gap: 18px; padding: 29px 0 20px}
.overline {font-size: 10px; font-weight: 650; letter-spacing: .17em; text-transform: uppercase;
  color: var(--cyan); display: flex; align-items: center; gap: 9px}
.overline::before {content: ""; width: 22px; height: 2px; background: var(--cyan)}
h1 {font-size: clamp(34px,3.5vw,54px); letter-spacing: -.055em; line-height: 1.13; margin: 7px 0 4px}
.sub {color: var(--muted); font-size: 14px}
.pair {gap: 8px; flex-wrap: wrap; justify-content: flex-end}
.chip {padding: 5px 9px; border: 1px solid var(--line); border-radius: 5px;
  font-size: 11px; color: #d7e3f3; background: #111b2a}
.dot {width: 8px; height: 8px; display: inline-block; margin-right: 7px;
  border-radius: 50%; background: var(--accent)}
.vs {font: 11px var(--mono); color: var(--muted)}
.cards {display: grid; grid-template-columns: repeat(3,minmax(0,1fr)); gap: 14px}
.card,.panel {border: 1px solid var(--line); border-radius: 13px;
  background: linear-gradient(125deg,#141f30,var(--panel) 65%); box-shadow: 0 10px 26px #0002}
.card {position: relative; overflow: hidden; padding: 17px 20px 14px;
  transition: border-color .18s, transform .18s}
.card::before {content: ""; position: absolute; top: 0; left: 20px; width: 43px;
  height: 2px; background: var(--accent)}
@media (hover:hover) {.card:hover {border-color: #526581; transform: translateY(-2px)}}
.kpi-title {font-size: 11px; font-weight: 600; letter-spacing: .09em; text-transform: uppercase;
  color: #cad6e5}
.kpi-body {display: flex; align-items: center; justify-content: space-between; gap: 8px; min-height: 65px}
.amount {font: 550 clamp(27px,3.05vw,48px)/1.2 var(--mono); letter-spacing: -.075em; white-space: nowrap}
.amount small {font-size: .50em; margin-left: 4px; letter-spacing: -.03em}
.positive {color: var(--green)}.negative {color: var(--red)}.flat {color: var(--muted)}
.spark {width: clamp(50px,6.8vw,110px); max-width: 25%; height: 35px}
.kpi-bottom {border-top: 1px solid #29364a; padding-top: 9px; gap: 6px;
  color: var(--muted); font-size: 12px; justify-content: space-between; flex-wrap: wrap}
.tag {font-size: 10px; color: #c6d2e1}
.panel {margin-top: 16px}
.chart-head {padding: 19px 21px 6px; justify-content: space-between; gap: 12px}
h2 {font-weight: 630; font-size: clamp(17px,1.65vw,24px); letter-spacing: -.04em}
.range {color: #c6d2e3; font-size: 11px; gap: 7px; white-space: nowrap}
.chart-unit {font-size: 11px; color: var(--muted); margin-top: 4px}
.chart {height: clamp(295px,40vh,510px); margin: 0 7px 6px}
.insight-head {padding: 18px 21px 12px; display: flex; justify-content: space-between;
  align-items: baseline; gap: 14px; flex-wrap: wrap}
.summary {font-size: 13px; color: #cad6e5}
.table-wrap {overflow-x: auto; padding: 0 21px 10px}
table {border-collapse: collapse; width: 100%; font: 12px/1.5 var(--mono)}
th,td {text-align: right; padding: 9px 8px; white-space: nowrap; border-top: 1px solid var(--line)}
th {font-size: 10px; font-weight: 500; color: var(--muted); text-transform: uppercase; letter-spacing: .04em}
th:first-child,td:first-child {text-align: left; padding-left: 0}
.series-name {gap: 4px; font-weight: 600}
.foot {justify-content: space-between; gap: 8px 18px; flex-wrap: wrap; color: var(--muted);
  padding: 16px 0 24px; font-size: 10px}
@media(max-width: 900px) {
  .meta {gap: 12px}.meta div {padding-left: 9px}.card {padding-inline: 13px}
  .spark {max-width: 23%}.chart {height: 340px}
}
@media(max-width: 720px) {
  .header-inner {flex-wrap: wrap; gap: 13px; padding: 16px 0}
  .meta {width: 100%; flex-wrap: wrap; gap: 8px 16px}
  .meta div {border: 0; padding: 0}dd {font-size: 11px}
  .overview {align-items: flex-start; flex-direction: column; padding: 21px 0 15px; gap: 12px}
  .pair {justify-content: flex-start}.cards {gap: 8px}.card {padding: 14px 10px 10px}
  .kpi-title {font-size: 10px}.spark {display: none}.kpi-body {min-height: 49px}
  .amount {font-size: clamp(23px,4.8vw,32px)}.kpi-bottom {font-size: 11px}
  .chart-head,.insight-head {padding: 16px 13px 4px; flex-wrap: wrap}
  .chart {height: 305px; margin-inline: 0}.table-wrap {padding-inline: 13px}
}
@media(max-width: 480px) {
  .cards {grid-template-columns: repeat(2,minmax(0,1fr))}
  .card:last-child {grid-column: 1 / -1; display: grid; grid-template-columns: 1fr auto; align-items: center}
  .card:last-child .kpi-bottom {grid-column: 1 / -1}.card:last-child .kpi-body {min-height: 36px}
  .chart {height: 275px}.range {font-size: 10px}
}
@media(prefers-reduced-motion: reduce) {.card {transition: none}}
"""


def day(iso_date):
    return date.fromisoformat(iso_date).strftime("%d %b %Y")


def tone(value):
    if value > 0:
        return "positive"
    if value < 0:
        return "negative"
    return "flat"


def sparkline(rows, color):
    """Map the supplied index levels to pixels for a decorative miniature."""
    values = [row["value"] for row in rows]
    if len(values) < 2:
        return None
    low, high = min(values), max(values)
    points = []
    for i, value in enumerate(values):
        x = 2 + 96 * i / (len(values) - 1)
        y = 18 if high == low else 32 - 28 * (value - low) / (high - low)
        points.append(f"{x:.1f},{y:.1f}")
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 36">'
           f'<polyline points="{" ".join(points)}" fill="none" stroke="{color}" '
           'stroke-width="2" stroke-linejoin="round" stroke-linecap="round"/></svg>')
    return html.Img(src="data:image/svg+xml," + quote(svg), className="spark", alt="")


def kpi(title, value, unit, caption, tag, accent, rows=()):
    body = [html.Div([f"{value:+.2f}", html.Small(unit)], className=f"amount {tone(value)}")]
    if rows:
        body.append(sparkline(rows, accent))
    return html.Article([
        html.H3(title, className="kpi-title"),
        html.Div(body, className="kpi-body"),
        html.Div([html.Span(caption), html.Span(tag, className="tag")], className="kpi-bottom"),
    ], className="card", style={"--accent": accent})


def figure(snapshot):
    chart = go.Figure()
    for role, color in (("instrument", CYAN), ("benchmark", INDIGO)):
        asset = snapshot[role]
        rows = snapshot[f"{role}_base_100"]
        chart.add_trace(go.Scatter(
            x=[row["date"] for row in rows], y=[row["value"] for row in rows],
            name=asset["ticker"] if role == "instrument" else asset["name"],
            mode="lines+markers" if len(rows) == 1 else "lines",
            line=dict(color=color, width=3, dash="solid" if role == "instrument" else "dash"),
            hovertemplate="%{y:.2f}<extra></extra>",
        ))
    chart.add_hline(y=100, line_width=1, line_dash="dot", line_color="#7789a2", layer="below")
    chart.update_layout(
        template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Menlo, Consolas, monospace", size=11, color="#b4c2d6"),
        margin=dict(l=51, r=18, t=40, b=37), hovermode="x unified", dragmode="zoom",
        legend=dict(orientation="h", x=0, y=1.02, xanchor="left", yanchor="bottom",
                    bgcolor="rgba(0,0,0,0)"),
        hoverlabel=dict(bgcolor="#172437", bordercolor="#415771", font_color="#f8fafc"),
        xaxis=dict(type="date", showgrid=False, tickformat="%d %b", nticks=6,
                   hoverformat="%d %b %Y", showline=True, linecolor="#364458",
                   showspikes=True, spikemode="across", spikedash="dot", spikecolor="#a3b2c7"),
        yaxis=dict(showgrid=True, gridcolor="#253246", zeroline=False, tickformat=".2f",
                   nticks=6, automargin=True),
    )
    return chart


def details(label, value, class_name=""):
    return html.Div([html.Dt(label), html.Dd(value, className=class_name)])


def chip(asset, accent):
    return html.Span([html.I(className="dot"), asset["ticker"]], className="chip",
                     style={"--accent": accent})


def insights_row(snapshot, role, color):
    rows = snapshot[f"{role}_base_100"]
    value = snapshot[f"{role}_return"]
    return html.Tr([
        html.Th(html.Span([html.I(className="dot"), snapshot[role]["name"]], className="series-name"),
                scope="row", style={"--accent": color}),
        html.Td(day(rows[0]["date"])), html.Td(day(rows[-1]["date"])), html.Td(len(rows)),
        html.Td(f"{rows[0]['value']:.2f}"), html.Td(f"{rows[-1]['value']:.2f}"),
        html.Td(f"{value:+.2f}%", className=tone(value)),
    ])


def layout(snapshot):
    instrument, benchmark = snapshot["instrument"], snapshot["benchmark"]
    left, right = instrument["ticker"], benchmark["name"]
    series = snapshot["instrument_base_100"]
    spread = snapshot["relative_performance"]
    if spread == 0:
        summary = f"{left} matched {right} over the period."
    else:
        verb = "outperformed" if spread > 0 else "underperformed"
        summary = f"{left} {verb} {right} by {abs(spread):.2f} percentage points."

    header = html.Header(html.Div([
        html.Div([
            html.Span([html.I(), html.I(), html.I()], className="mark", **{"aria-hidden": "true"}),
            html.Div([html.Div("MARKETPULSE", className="wordmark"),
                      html.Div("INSTITUTIONAL MARKET INTELLIGENCE", className="brand-sub")]),
        ], className="brand"),
        html.Dl([details("Provider", snapshot["provider"]),
                 details("Access mode", snapshot["access_mode"], "mode"),
                 details("Period", snapshot["lookback"]), details("Interval", snapshot["interval"])],
                className="meta"),
    ], className="wrap header-inner"), className="topbar")

    overview = html.Section([
        html.Div([html.P("Market intelligence", className="overline"), html.H1("Market Overview"),
                  html.P("Instrument vs Benchmark Performance Analysis", className="sub")]),
        html.Div([chip(instrument, CYAN), html.Span("vs", className="vs"), chip(benchmark, INDIGO)],
                 className="pair"),
    ], className="overview")
    cards = html.Section([
        kpi(f"{left} return", snapshot["instrument_return"], "%", instrument["name"],
            instrument["market"], CYAN, series),
        kpi(f"{right} return", snapshot["benchmark_return"], "%", benchmark["name"],
            benchmark["ticker"], INDIGO, snapshot["benchmark_base_100"]),
        kpi("Relative performance", spread, "pp", f"{left} vs {right}", "Period spread", "#3B82F6"),
    ], className="cards", **{"aria-label": "Period performance"})

    hero = html.Section([
        html.Div([html.Div([html.H2("Performance comparison — Base 100"),
                            html.P("Indexed performance · first observation = 100", className="chart-unit")]),
                  html.P(f"{day(series[0]['date'])} — {day(series[-1]['date'])}", className="range")],
                 className="chart-head"),
        dcc.Graph(figure=figure(snapshot), responsive=True, className="chart",
                  config={"displaylogo": False, "displayModeBar": "hover", "scrollZoom": False,
                          "modeBarButtonsToRemove": ["select2d", "lasso2d"]}),
    ], className="panel")
    columns = ["Series", "First date", "Last date", "Observations", "Start index", "End index", "Return"]
    insights = html.Section([
        html.Div([html.H2("Performance insights"), html.P(summary, className="summary")],
                 className="insight-head"),
        html.Div(html.Table([
            html.Thead(html.Tr([html.Th(c, scope="col") for c in columns])),
            html.Tbody([insights_row(snapshot, "instrument", CYAN),
                        insights_row(snapshot, "benchmark", INDIGO)]),
        ]), className="table-wrap", tabIndex=0, role="region", **{"aria-label": "Series statistics"}),
    ], className="panel")
    footer = html.Footer([
        html.Span("MARKETPULSE | Financial Engineering Project — ESILV"),
        html.Span(f"Educational demonstration — {snapshot['access_mode']} data"),
    ], className="wrap foot")
    return html.Div([header, html.Main([overview, cards, hero, insights], className="wrap"), footer],
                    className="shell")


app = Dash(__name__, title="MarketPulse | Market Intelligence", serve_locally=True)
app.index_string = app.index_string.replace("</head>", f"<style>{CSS}</style></head>")
app.layout = layout(build_market_snapshot())

if __name__ == "__main__":
    app.run(debug=False)
