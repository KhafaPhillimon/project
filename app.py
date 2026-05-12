"""
AI Solutions – Institutional Intelligence Platform
Premium BAC-Inspired Overhaul (Senior Developer Edition)
"""

import dash
from dash import dcc, html, dash_table, Input, Output, State
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import flask

# ── Institutional Design System (BAC Inspired) ──────────────────────────────
NAVY    = "#003366"  
GOLD    = "#C5A059"  
BG      = "#f8fafc"  
SUCCESS = "#10b981"
DANGER  = "#ef4444"
TEXT    = "#1e293b"
MUTED   = "#64748b"
BORDER  = "#e2e8f0"

# ── Authorised users ─────────────────────────────────────────────────────────
USERS = {
    "admin":  "aisolutions2026",
    "letty":  "dashboard123",
    "viewer": "view2026",
}

# ── Data Loading ─────────────────────────────────────────────────────────────
CSV_PATH = "AI_Solutions_Web_Log_Dataset.csv"

def load_data():
    try:
        df = pd.read_csv(CSV_PATH)
        # Verify essential columns exist
        cols = ["timestamp", "country", "service_type", "status_code", "response_size", "ip_address", "method", "page"]
        for c in cols:
            if c not in df.columns:
                df[c] = 0 if "size" in c else "Unknown"

        df["timestamp"] = pd.to_datetime(df["timestamp"], dayfirst=True, errors='coerce')
        df = df.dropna(subset=["timestamp"]) # Remove rows with invalid dates
        df["date"]      = df["timestamp"].dt.date
        df["hour"]      = df["timestamp"].dt.hour
        df["week"]      = df["timestamp"].dt.isocalendar().week.astype(int)
        df["status_code"] = df["status_code"].astype(str)
        return df
    except Exception as e:
        print(f"LOG: Data load failed, using empty schema. Error: {e}")
        return pd.DataFrame(columns=["timestamp", "country", "service_type", "status_code", "response_size", "ip_address", "method", "page", "date", "hour", "week"])

df = load_data()

SERVICE_COLOURS = {
    "Job Request":       NAVY,
    "Demo Request":      GOLD,
    "Demo Submission":   "#005A9C",
    "AI Assistant":      "#2C3E50",
    "Promotional Event": "#E67E22",
    "Prototype Request": SUCCESS,
    "Homepage":          "#7F8C8D",
    "Image Asset":       "#BDC3C7",
    "CSS Asset":         "#ECF0F1",
    "Job Application":   "#3498DB",
    "Contact Page":      DANGER,
}

# ── CSS Design System (Managed via assets/style.css) ──────────────────────────


# ── CSS Design System (Bulletproof Injection) ──────────────────────────────
CSS_STYLES = """
:root {
    --primary: #003366;
    --secondary: #C5A059;
    --bg-main: #f8fafc;
    --card-bg: rgba(255, 255, 255, 0.95);
    --text-main: #1e293b;
    --text-muted: #64748b;
    --border: #e2e8f0;
    --success: #10b981;
    --danger: #ef4444;
    --sidebar-width: 280px;
    --header-height: 80px;
    --transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
* { box-sizing: border-box; }
body { margin: 0; padding: 0; font-family: 'Inter', sans-serif; background-color: var(--bg-main); color: var(--text-main); overflow-x: hidden; }
.glass-card { background: var(--card-bg); backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.1); box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1); border-radius: 1.5rem; transition: var(--transition); }
.glass-card:hover { transform: translateY(-5px); box-shadow: 0 20px 25px -5px rgb(0 0 0 / 0.1); }
.sidebar { width: var(--sidebar-width); background: linear-gradient(180deg, #001e3c 0%, #003366 100%); padding: 2.5rem 1.5rem; height: 100vh; position: fixed; left: 0; top: 0; z-index: 1000; display: flex; flex-direction: column; box-shadow: 4px 0 24px rgba(0, 0, 0, 0.1); }
.nav-link { display: flex; align-items: center; padding: 0.875rem 1.25rem; margin-bottom: 0.5rem; border-radius: 1rem; color: rgba(255, 255, 255, 0.6); text-decoration: none; font-weight: 500; font-size: 0.9375rem; transition: var(--transition); }
.nav-link:hover { background: rgba(255, 255, 255, 0.05); color: white; }
.nav-link.active { background: var(--secondary); color: #001e3c; box-shadow: 0 10px 15px -3px rgba(197, 160, 89, 0.3); }
.stat-card { padding: 1.5rem; display: flex; flex-direction: column; justify-content: space-between; min-height: 140px; }
.stat-value { font-size: 2rem; font-weight: 800; color: var(--primary); margin: 0.5rem 0; font-family: 'Montserrat', sans-serif; }
@keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
.fade-in { animation: fadeIn 0.5s ease-out forwards; }
.login-container { background: radial-gradient(circle at top right, #004080, #001e3c); min-height: 100vh; display: flex; align-items: center; justify-content: center; padding: 2rem; }
.login-box { background: white; border-radius: 2.5rem; display: flex; overflow: hidden; max-width: 1100px; width: 100%; box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5); }
.login-visual { flex: 1; background: var(--primary); padding: 4rem; color: white; display: flex; flex-direction: column; justify-content: center; position: relative; overflow: hidden; }
.login-form { flex: 1; padding: 5rem; }
.logout-btn-premium { background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.1); color: var(--secondary); width: 100%; padding: 0.75rem; border-radius: 0.75rem; font-size: 0.75rem; font-weight: 700; cursor: pointer; margin-top: 1rem; display: flex; align-items: center; justify-content: center; transition: var(--transition); text-transform: uppercase; letter-spacing: 0.05em; }
.logout-btn-premium:hover { background: rgba(197, 160, 89, 0.1); border-color: var(--secondary); color: white; }
.login-input { width: 100%; padding: 12px 0; border: none; border-bottom: 2px solid var(--border); font-size: 1rem; color: var(--text-main); background: transparent; outline: none; transition: var(--transition); height: 48px; line-height: 24px; }
.login-input:focus { border-color: var(--primary); }
"""

# ── Dash Setup ───────────────────────────────────────────────────────────────
server = flask.Flask(__name__)
app = dash.Dash(
    __name__, 
    server=server, 
    suppress_callback_exceptions=True,
    external_stylesheets=[
        "https://fonts.googleapis.com/css2?family=Montserrat:wght@600;700;800&family=Inter:wght@400;500;600;700&display=swap",
        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.2/css/all.min.css"
    ]
)
app.title = "AI Solutions | Institutional Intelligence"

app.index_string = f'''
<!DOCTYPE html>
<html>
    <head>
        {{%metas%}}
        <title>{{%title%}}</title>
        {{%favicon%}}
        {{%css%}}
        <style>{CSS_STYLES}</style>
    </head>
    <body>
        {{%app_entry%}}
        <footer>
            {{%config%}}
            {{%scripts%}}
            {{%renderer%}}
        </footer>
    </body>
</html>
'''

# ═══════════════════════════════════════════════════════════════════════════════
#  COMPONENTS
# ═══════════════════════════════════════════════════════════════════════════════

def stat_card(title, value, subtitle="", colour=NAVY):
    return html.Div(
        className="glass-card stat-card fade-in",
        children=[
            html.Div(style={"display": "flex", "justifyContent": "space-between", "alignItems": "center"}, children=[
                html.P(title, style={"color": MUTED, "fontSize": "0.75rem", "fontWeight": "700", "textTransform": "uppercase", "letterSpacing": "0.05em", "margin": "0"}),
                html.Div(style={"width": "8px", "height": "8px", "borderRadius": "50%", "background": colour})
            ]),
            html.H2(value, className="stat-value"),
            html.P(style={"color": MUTED, "fontSize": "0.8rem", "margin": "0", "display": "flex", "alignItems": "center"}, children=[
                html.I(className="fa-solid fa-arrow-up", style={"marginRight": "4px", "color": SUCCESS, "fontSize": "0.7rem"}) if "Success" in subtitle or "Volume" in title else "",
                html.Span(subtitle)
            ]),
        ]
    )

def section_header(title, subtitle="Live Institutional Insights"):
    return html.Div(
        style={"marginBottom": "2rem"},
        children=[
            html.H3(title, style={"color": NAVY, "fontSize": "1.25rem", "fontWeight": "700", "margin": "0", "fontFamily": "Montserrat"}),
            html.P(subtitle, style={"color": MUTED, "fontSize": "0.75rem", "margin": "0.25rem 0 0", "textTransform": "uppercase", "letterSpacing": "0.1em"})
        ]
    )

chart_theme = {
    "plot_bgcolor":  "rgba(0,0,0,0)",
    "paper_bgcolor": "rgba(0,0,0,0)",
    "font": {"family": "Inter, sans-serif", "color": TEXT},
    "margin": dict(l=40, r=20, t=40, b=40),
}

# ═══════════════════════════════════════════════════════════════════════════════
#  LOGIN PAGE
# ═══════════════════════════════════════════════════════════════════════════════

login_layout = html.Div(
    className="login-container",
    children=[
        html.Div(
            className="login-box fade-in",
            children=[
                # Brand Side
                html.Div(
                    className="login-visual",
                    children=[
                        html.Img(src=app.get_asset_url("logo.png"), style={"width": "120px", "marginBottom": "2rem", "borderRadius": "10px"}),
                        html.Div(
                            children=[
                                html.H1("AI SOLUTIONS", style={"fontSize": "3.5rem", "fontWeight": "800", "margin": "0", "letterSpacing": "-0.04em", "lineHeight": "1"}),
                                html.Div(style={"width": "4rem", "height": "4px", "background": "white", "marginBottom": "2rem", "marginTop": "2rem"}),
                                html.P("Empowering data-driven decisions with institutional-grade web analytics and predictive insights.", style={"fontSize": "1rem", "lineHeight": "1.6", "opacity": "0.8"}),
                            ]
                        ),
                    ]
                ),
                # Form Side
                html.Div(
                    className="login-form",
                    children=[
                        html.H2("System Portal", style={"color": NAVY, "fontSize": "1.875rem", "fontWeight": "700", "marginBottom": "0.5rem"}),
                        html.P("Enter your credentials to access the hub.", style={"color": MUTED, "fontSize": "0.9375rem", "marginBottom": "2.5rem"}),
                        
                        html.Div(style={"marginBottom": "1.5rem"}, children=[
                            html.Label("Username", style={"display": "block", "fontSize": "0.75rem", "fontWeight": "700", "color": NAVY, "textTransform": "uppercase", "marginBottom": "0.5rem"}),
                            dcc.Input(id="login-username", type="text", placeholder="Enter ID", className="login-input"),
                        ]),
                        
                        html.Div(style={"marginBottom": "2rem"}, children=[
                            html.Label("Password", style={"display": "block", "fontSize": "0.75rem", "fontWeight": "700", "color": NAVY, "textTransform": "uppercase", "marginBottom": "0.5rem"}),
                            dcc.Input(id="login-password", type="password", placeholder="••••••••", className="login-input"),
                        ]),
                        
                        html.Div(id="login-error", style={"color": DANGER, "fontSize": "0.875rem", "marginBottom": "1.5rem", "minHeight": "1.25rem"}),
                        
                        html.Button(
                            "SIGN IN TO PORTAL", 
                            id="login-btn", 
                            n_clicks=0, 
                            style={"width": "100%", "padding": "1.25rem", "background": NAVY, "color": "white", "border": "none", "borderRadius": "0.75rem", "fontSize": "0.875rem", "fontWeight": "700", "cursor": "pointer", "letterSpacing": "0.05em", "transition": "background 0.3s"}
                        ),
                    ]
                )
            ]
        )
    ]
)

# ═══════════════════════════════════════════════════════════════════════════════
#  PAGES
# ═══════════════════════════════════════════════════════════════════════════════

def generate_overview_page(filtered):
    total = len(filtered)
    success_cnt = len(filtered[filtered["status_code"] == "200"])
    error_cnt   = len(filtered[filtered["status_code"] == "500"])
    countries_n = filtered["country"].nunique()
    success_pct = f"{success_cnt/total*100:.1f}%" if total > 0 else "0%"

    # Summary Charts for Overview
    hourly_data = filtered.groupby("hour").size().reset_index(name="count")
    fig_hour = px.line(hourly_data, x="hour", y="count", color_discrete_sequence=[NAVY])
    fig_hour.update_layout(**chart_theme, height=250, margin=dict(l=10, r=10, t=10, b=10))
    fig_hour.update_xaxes(showgrid=False)

    service_data = filtered.groupby("service_type").size().reset_index(name="count").sort_values("count", ascending=False).head(5)
    fig_service = px.pie(service_data, names="service_type", values="count", color_discrete_sequence=[NAVY, GOLD, SUCCESS, "#cbd5e1", DANGER], hole=0.6)
    fig_service.update_layout(**chart_theme, height=250, showlegend=False, margin=dict(l=10, r=10, t=10, b=10))

    return html.Div([
        html.Div(
            style={"display": "grid", "gridTemplateColumns": "repeat(4, 1fr)", "gap": "1.5rem", "marginBottom": "2.5rem"},
            children=[
                stat_card("Total Traffic", f"{total:,}", "Aggregated Logs", NAVY),
                stat_card("System Health", success_pct, "Successful Requests", SUCCESS),
                stat_card("Security Alerts", f"{error_cnt}", "Critical Errors", DANGER),
                stat_card("Global Reach", str(countries_n), "Active Regions", GOLD),
            ]
        ),
        html.Div(
            style={"display": "grid", "gridTemplateColumns": "1fr 1fr 1.2fr", "gap": "1.5rem"},
            children=[
                html.Div(className="glass-card", style={"padding": "1.5rem"}, children=[
                    section_header("Traffic Velocity", "Hourly Distribution"),
                    dcc.Graph(figure=fig_hour, config={"displayModeBar": False})
                ]),
                html.Div(className="glass-card", style={"padding": "1.5rem"}, children=[
                    section_header("Top Services", "Service Matrix"),
                    dcc.Graph(figure=fig_service, config={"displayModeBar": False})
                ]),
                html.Div(className="glass-card", style={"padding": "2rem"}, children=[
                    section_header("Operational Status"),
                    html.P("This high-fidelity dashboard provides a comprehensive analytical overview of the AI Solutions infrastructure. By leveraging institutional-grade metrics, administrators can monitor real-time traffic fluctuations.", style={"color": TEXT, "lineHeight": "1.6", "fontSize": "0.85rem"}),
                    html.Div(style={"marginTop": "1.5rem", "padding": "1.5rem", "borderRadius": "1rem", "background": f"{SUCCESS}10", "textAlign": "center"}, children=[
                        html.I(className="fa-solid fa-circle-check", style={"color": SUCCESS, "fontSize": "2rem", "marginBottom": "0.5rem"}),
                        html.H4("System Optimal", style={"color": SUCCESS, "margin": "0", "fontSize": "1.1rem"}),
                    ])
                ])
            ]
        )
    ])

def generate_countries_page(filtered):
    country_counts = filtered.groupby("country").size().reset_index(name="count")
    
    fig_map = px.choropleth(
        country_counts, 
        locations="country", 
        locationmode="country names", 
        color="count", 
        color_continuous_scale=[[0, "#f8fafc"], [0.2, "#cbd5e1"], [1, NAVY]],
        labels={"count": "Requests"}
    )
    fig_map.update_layout(**chart_theme, geo=dict(bgcolor="rgba(0,0,0,0)", showframe=False, projection_type="equirectangular"))

    fig_bar = px.bar(
        country_counts.sort_values("count", ascending=False).head(10), 
        x="country", 
        y="count",
        color_discrete_sequence=[GOLD]
    )
    fig_bar.update_layout(**chart_theme, xaxis_title="", yaxis_title="Requests")

    return html.Div(style={"display": "grid", "gap": "1.5rem"}, children=[
        html.Div(className="glass-card", style={"padding": "2rem"}, children=[
            section_header("Geographic Traffic Distribution"),
            dcc.Graph(figure=fig_map, config={"displayModeBar": False})
        ]),
        html.Div(className="glass-card", style={"padding": "2rem"}, children=[
            section_header("Top 10 Performing Regions"),
            dcc.Graph(figure=fig_bar, config={"displayModeBar": False})
        ])
    ])

def generate_services_page(filtered):
    service_counts = filtered.groupby("service_type").size().reset_index(name="count")
    
    fig_pie = px.pie(
        service_counts, 
        names="service_type", 
        values="count", 
        color="service_type", 
        color_discrete_map=SERVICE_COLOURS, 
        hole=0.7
    )
    fig_pie.update_layout(**chart_theme, showlegend=True, legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5))
    fig_pie.update_traces(textinfo="percent", textfont_size=10)

    fig_bar = px.bar(
        service_counts.sort_values("count", ascending=True), 
        x="count", 
        y="service_type", 
        orientation="h", 
        color="service_type", 
        color_discrete_map=SERVICE_COLOURS
    )
    fig_bar.update_layout(**chart_theme, showlegend=False, xaxis_title="Total Logs")

    return html.Div(style={"display": "grid", "gridTemplateColumns": "1fr 1fr", "gap": "1.5rem"}, children=[
        html.Div(className="glass-card", style={"padding": "2rem"}, children=[
            section_header("Service Utilization Matrix"),
            dcc.Graph(figure=fig_pie, config={"displayModeBar": False})
        ]),
        html.Div(className="glass-card", style={"padding": "2rem"}, children=[
            section_header("Workload Distribution"),
            dcc.Graph(figure=fig_bar, config={"displayModeBar": False})
        ])
    ])

def generate_trends_page(filtered):
    daily = filtered.groupby("date").size().reset_index(name="requests")
    
    fig_trend = go.Figure()
    fig_trend.add_trace(go.Scatter(
        x=daily["date"], 
        y=daily["requests"], 
        mode="lines", 
        line=dict(color=NAVY, width=3, shape="spline"),
        fill="tozeroy", 
        fillcolor="rgba(0, 51, 102, 0.05)"
    ))
    fig_trend.update_layout(**chart_theme, xaxis=dict(showgrid=False), yaxis=dict(gridcolor=BORDER))

    fig_scatter = px.scatter(
        filtered[filtered["response_size"]>0], 
        x="timestamp", 
        y="response_size", 
        color="service_type", 
        color_discrete_map=SERVICE_COLOURS, 
        opacity=0.6
    )
    fig_scatter.update_layout(**chart_theme)

    return html.Div(style={"display": "grid", "gap": "1.5rem"}, children=[
        html.Div(className="glass-card", style={"padding": "2rem"}, children=[
            section_header("Temporal Activity Velocity"),
            dcc.Graph(figure=fig_trend, config={"displayModeBar": False})
        ]),
        html.Div(className="glass-card", style={"padding": "2rem"}, children=[
            section_header("Payload Response Correlation"),
            dcc.Graph(figure=fig_scatter, config={"displayModeBar": False})
        ])
    ])

def generate_statistics_page(filtered):
    stats_data = []
    for service in filtered["service_type"].unique():
        subset = filtered[(filtered["service_type"] == service) & (filtered["response_size"] > 0)]["response_size"]
        if not subset.empty:
            stats_data.append({
                "Service": service, 
                "Count": len(subset), 
                "Avg Size": f"{subset.mean():,.0f} B", 
                "Peak": f"{subset.max():,} B"
            })
    
    stats_table = dash_table.DataTable(
        data=stats_data,
        style_table={"overflowX": "auto"},
        style_header={"backgroundColor": NAVY, "color": "white", "fontWeight": "700", "fontSize": "0.75rem", "padding": "1rem", "textTransform": "uppercase"},
        style_cell={"backgroundColor": "white", "color": TEXT, "border": "none", "borderBottom": f"1px solid {BORDER}", "padding": "1rem", "fontSize": "0.875rem", "fontFamily": "Inter"},
    )

    status_counts = filtered.groupby("status_code").size().reset_index(name="count")
    fig_status = px.pie(
        status_counts, 
        names="status_code", 
        values="count", 
        color_discrete_sequence=[SUCCESS, GOLD, "#cbd5e1", DANGER], 
        hole=0.7
    )
    fig_status.update_layout(**chart_theme)

    return html.Div(style={"display": "grid", "gridTemplateColumns": "1.5fr 1fr", "gap": "1.5rem"}, children=[
        html.Div(className="glass-card", style={"padding": "2rem"}, children=[
            section_header("Resource Performance Metrics"), 
            stats_table
        ]),
        html.Div(className="glass-card", style={"padding": "2rem"}, children=[
            section_header("Node Health Status"), 
            dcc.Graph(figure=fig_status, config={"displayModeBar": False})
        ])
    ])

def generate_logs_page(filtered):
    display_cols = ["timestamp","ip_address","country","method","page","service_type","status_code"]
    raw_df = filtered[display_cols].head(200).copy()
    raw_df["timestamp"] = raw_df["timestamp"].astype(str)

    raw_table = dash_table.DataTable(
        data=raw_df.to_dict("records"),
        columns=[{"name": c.replace("_"," ").title(), "id": c} for c in display_cols],
        page_size=15,
        style_table={"overflowX": "auto"},
        style_header={"backgroundColor": NAVY, "color": "white", "fontWeight": "700", "fontSize": "0.75rem", "padding": "1rem"},
        style_cell={"backgroundColor": "white", "color": TEXT, "borderBottom": f"1px solid {BORDER}", "padding": "1rem", "fontSize": "0.75rem", "fontFamily": "Inter"},
    )
    return html.Div(className="glass-card", style={"padding": "2rem"}, children=[
        section_header("Verified Infrastructure Logs"),
        raw_table
    ])

# ═══════════════════════════════════════════════════════════════════════════════
#  MAIN LAYOUT
# ═══════════════════════════════════════════════════════════════════════════════

app.layout = html.Div([
    dcc.Location(id="url", refresh=False),
    dcc.Store(id="session-store", storage_type="session"),
    html.Div(id="page-content"),
])

def dashboard_layout(pathname):
    nav_links = [
        ("/", "Overview", "fa-solid fa-chart-pie"),
        ("/countries", "Regional", "fa-solid fa-earth-africa"),
        ("/services", "Services", "fa-solid fa-microchip"),
        ("/trends", "Velocity", "fa-solid fa-gauge-high"),
        ("/statistics", "Reporting", "fa-solid fa-layer-group"),
        ("/logs", "Security", "fa-solid fa-shield-halved"),
    ]
    
    sidebar_items = []
    for path, label, icon_class in nav_links:
        active_class = "nav-link active" if (pathname == path or (pathname == "" and path == "/")) else "nav-link"
        sidebar_items.append(
            dcc.Link(
                children=[
                    html.I(className=f"{icon_class}", style={"marginRight": "15px", "fontSize": "1.1rem", "width": "20px", "textAlign": "center"}),
                    html.Span(label)
                ],
                href=path,
                className=active_class
            )
        )

    return html.Div(
        children=[
            # Sidebar
            html.Div(
                className="sidebar",
                children=[
                    html.Div(
                        style={"marginBottom": "3rem", "padding": "0 0.5rem", "textAlign": "center"},
                        children=[
                            html.Img(src=app.get_asset_url("logo.png"), style={"width": "80px", "marginBottom": "1.5rem", "borderRadius": "8px"}),
                            html.H2("AI SOLUTIONS", style={"color": "white", "fontSize": "1.5rem", "fontWeight": "800", "margin": "0", "fontFamily": "Montserrat", "letterSpacing": "-0.04em"}),
                            html.P("INTELLIGENCE PORTAL", style={"color": GOLD, "fontSize": "0.625rem", "fontWeight": "700", "margin": "0.25rem 0 0", "letterSpacing": "0.2em"})
                        ]
                    ),
                    html.Div(children=sidebar_items),
                    html.Div(style={"marginTop": "auto"}, children=[
                        html.Div(
                            style={"background": "rgba(255,255,255,0.03)", "borderRadius": "1rem", "padding": "1.25rem", "border": "1px solid rgba(255,255,255,0.05)"},
                            children=[
                                html.Button(
                                    children=[
                                        html.I(className="fa-solid fa-right-from-bracket", style={"marginRight": "10px"}),
                                        "Sign Out"
                                    ], 
                                    id="logout-btn", 
                                    n_clicks=0, 
                                    className="logout-btn-premium",
                                    style={"marginTop": "0"} # Adjust margin since labels are gone
                                )
                            ]
                        )
                    ])
                ]
            ),
            
            # Main Content Area
            html.Div(
                style={
                    "marginLeft": "var(--sidebar-width)", 
                    "minHeight": "100vh", 
                    "display": "flex", 
                    "flexDirection": "column",
                    "width": "calc(100% - var(--sidebar-width))",
                    "position": "relative"
                },
                children=[
                    # Top Navigation Bar
                    html.Div(
                        style={
                            "height": "var(--header-height)", 
                            "background": "white", 
                            "borderBottom": f"1px solid {BORDER}", 
                            "display": "flex", 
                            "alignItems": "center", 
                            "justifyContent": "space-between", 
                            "padding": "0 3rem", 
                            "position": "sticky", 
                            "top": "0", 
                            "zIndex": "950",
                            "flexShrink": "0"
                        },
                        children=[
                            html.Div([
                                html.H1(f"{pathname.replace('/','').title() if pathname != '/' else 'Dashboard Overview'}", style={"color": NAVY, "fontSize": "1.5rem", "fontWeight": "700", "margin": "0", "fontFamily": "Montserrat"}),
                            ]),
                            html.Div(
                                style={"display": "flex", "gap": "1rem", "alignItems": "center"},
                                children=[
                                    html.Div([
                                        html.P("Filter Country", style={"fontSize": "0.7rem", "fontWeight": "700", "color": MUTED, "margin": "0 0 4px", "textTransform": "uppercase"}),
                                        dcc.Dropdown(
                                            id="filter-country", 
                                            options=[{"label": "Global View", "value": "ALL"}] + [{"label": c, "value": c} for c in sorted(df["country"].unique())] if not df.empty else [{"label": "No Data", "value": "ALL"}], 
                                            value="ALL", 
                                            clearable=False, 
                                            style={"width": "160px", "fontSize": "0.8rem"}
                                        ),
                                    ]),
                                    html.Div([
                                        html.P("Filter Service", style={"fontSize": "0.7rem", "fontWeight": "700", "color": MUTED, "margin": "0 0 4px", "textTransform": "uppercase"}),
                                        dcc.Dropdown(
                                            id="filter-service", 
                                            options=[{"label": "All Services", "value": "ALL"}] + [{"label": s, "value": s} for s in sorted(df["service_type"].unique())] if not df.empty else [{"label": "No Data", "value": "ALL"}], 
                                            value="ALL", 
                                            clearable=False, 
                                            style={"width": "160px", "fontSize": "0.8rem"}
                                        ),
                                    ]),
                                ]
                            ),
                        ]
                    ),
                    
                    # Page Body
                    html.Div(
                        style={
                            "padding": "2.5rem 3rem", 
                            "maxWidth": "1600px", 
                            "width": "100%",
                            "margin": "0 auto",
                            "flex": "1"
                        },
                        id="dynamic-page-content"
                    )
                ]
            )
        ]
    )

# ── Callbacks ────────────────────────────────────────────────────────────────
@app.callback(
    Output("page-content", "children"),
    Input("url", "pathname"),
    Input("session-store", "data"),
)
def display_page(pathname, session):
    if session and session.get("logged_in"):
        return dashboard_layout(pathname)
    return login_layout

@app.callback(
    Output("dynamic-page-content", "children"),
    Input("url", "pathname"),
    Input("filter-country", "value"),
    Input("filter-service", "value"),
)
def update_dynamic_content(pathname, country_filter, service_filter):
    if not pathname: return dash.no_update
    
    filtered = df.copy()
    if country_filter and country_filter != "ALL":
        filtered = filtered[filtered["country"] == country_filter]
    if service_filter and service_filter != "ALL":
        filtered = filtered[filtered["service_type"] == service_filter]

    if pathname == "/countries":
        return generate_countries_page(filtered)
    elif pathname == "/services":
        return generate_services_page(filtered)
    elif pathname == "/trends":
        return generate_trends_page(filtered)
    elif pathname == "/statistics":
        return generate_statistics_page(filtered)
    elif pathname == "/logs":
        return generate_logs_page(filtered)
    else:
        return generate_overview_page(filtered)

@app.callback(
    Output("session-store", "data"),
    Output("login-error", "children"),
    Input("login-btn", "n_clicks"),
    Input("login-username", "n_submit"),
    Input("login-password", "n_submit"),
    State("login-username", "value"),
    State("login-password", "value"),
    prevent_initial_call=True,
)
def handle_login(n_clicks, n_submit_u, n_submit_p, username, password):
    if not username or not password:
        return dash.no_update, "Identification required."
    
    # Robust credential check
    clean_username = username.strip().lower()
    clean_password = password.strip()
    
    if clean_username in USERS and USERS[clean_username] == clean_password:
        return {"logged_in": True, "user": clean_username}, ""
    
    return dash.no_update, "Access Denied. Check credentials."

@app.callback(
    Output("session-store", "data", allow_duplicate=True),
    Output("url", "pathname", allow_duplicate=True),
    Input("logout-btn", "n_clicks"),
    prevent_initial_call=True,
)
def handle_logout(n_clicks):
    if n_clicks > 0:
        return {"logged_in": False}, "/"
    return dash.no_update, dash.no_update

if __name__ == "__main__":
    app.run(debug=True, port=8050)
