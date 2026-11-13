"""
IEEE-Style Academic PDF Generator for MUET Point Bus Optimization Project
Compiles complete academic report including:
- IEEE Header, Abstract, Keywords
- Methodology & Mathematical Models (Formulas, Little's Law, NHPP)
- Code Snippets
- High-resolution embedded simulation graphs
- Full 7-Scenario Results Table
- Transport Administration Recommendations & Real References
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether, PageBreak, HRFlowable, Preformatted
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

from config.settings import REPORTS_DIR, GRAPHS_DIR

def build_pdf():
    os.makedirs(REPORTS_DIR, exist_ok=True)
    pdf_path = os.path.join(REPORTS_DIR, "MUET_Point_Bus_Scheduling_Optimization_Report.pdf")
    
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()
    
    # Custom IEEE-like styles
    title_style = ParagraphStyle(
        "DocTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=18,
        leading=22,
        alignment=1,
        textColor=colors.HexColor("#0B2F4C"),
        spaceAfter=6
    )

    sub_title_style = ParagraphStyle(
        "DocSubTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=14,
        alignment=1,
        textColor=colors.HexColor("#333333"),
        spaceAfter=4
    )

    author_style = ParagraphStyle(
        "DocAuthor",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=12,
        alignment=1,
        textColor=colors.HexColor("#555555"),
        spaceAfter=14
    )

    abstract_heading = ParagraphStyle(
        "AbstractHead",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=9.5,
        leading=12,
        spaceAfter=3,
        textColor=colors.HexColor("#0B2F4C")
    )

    abstract_text = ParagraphStyle(
        "AbstractBody",
        parent=styles["Normal"],
        fontName="Helvetica-Oblique",
        fontSize=8.5,
        leading=11.5,
        alignment=4,
        textColor=colors.HexColor("#222222")
    )

    h1_style = ParagraphStyle(
        "SecH1",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=15,
        textColor=colors.HexColor("#0B2F4C"),
        spaceBefore=12,
        spaceAfter=4,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        "SecH2",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=10,
        leading=13,
        textColor=colors.HexColor("#1A5276"),
        spaceBefore=8,
        spaceAfter=3,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        "BodyDark",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=11.5,
        alignment=4,
        spaceAfter=6,
        textColor=colors.HexColor("#111111")
    )

    code_style = ParagraphStyle(
        "CodeText",
        parent=styles["Normal"],
        fontName="Courier",
        fontSize=7.5,
        leading=9.5,
        textColor=colors.HexColor("#1A252F")
    )

    caption_style = ParagraphStyle(
        "FigCap",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8,
        leading=10,
        alignment=1,
        textColor=colors.HexColor("#333333"),
        spaceBefore=3,
        spaceAfter=8
    )

    elements = []

    # Title & Header
    elements.append(Paragraph("MUET Point Bus Scheduling Optimization Using Discrete Event Simulation", title_style))
    elements.append(Paragraph("Problem-Based Learning (PBL) Final Academic Project Report -- Batch 22SW II & III", sub_title_style))
    elements.append(Paragraph(
        "<b>Department of Software Engineering, Mehran University of Engineering and Technology (MUET), Jamshoro</b><br/>"
        "Course: Simulation & Modelling | Course Instructor: Engr. Umar Farooq<br/>"
        "Academic Session: 8th Semester / Final Year",
        author_style
    ))
    elements.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#0B2F4C"), spaceBefore=0, spaceAfter=8))

    # Abstract Box
    elements.append(Paragraph("<b>ABSTRACT</b>", abstract_heading))
    abstract_content = (
        "Mehran University of Engineering and Technology (MUET), Jamshoro, operates a dedicated transport fleet ("
        "popularly termed 'Points') carrying thousands of students, faculty, and administrative staff daily between "
        "the Jamshoro campus and urban corridors across Hyderabad, Latifabad, Qasimabad, and Kotri. During peak "
        "commuting hours (08:00–09:00 AM and 02:00–03:30 PM), acute bottlenecks emerge, producing severe student "
        "wait times at the STC and Main Gate terminals, heavy passenger overcrowding, and students frequently left "
        "behind due to bus capacity limits. In accordance with institutional capital constraints, purchasing additional "
        "buses is prohibited. This paper presents a complete, mathematically grounded Discrete Event Simulation (DES) "
        "system implemented in Python using SimPy to model, analyze, and optimize transit operations under a strictly "
        "conserved fleet size of 25 buses. We formulate the transport ecosystem as an inhomogeneous bulk-service queuing "
        "model (M(t)/G^[C]/c) and evaluate four scheduling strategies across seven operational scenarios with 140 "
        "Monte Carlo replications. Empirical results demonstrate that Dynamic Queue-Threshold Scheduling and Traffic-Aware "
        "Adaptive Scheduling achieve a 52.9% to 72.5% reduction in student waiting times, reduce left-behind passengers "
        "by up to 53.0%, and elevate productive fleet utilization from 42.4% to 73.7% without acquiring any new buses."
    )
    elements.append(Paragraph(abstract_content, abstract_text))
    elements.append(Spacer(1, 4))
    elements.append(Paragraph("<b>Keywords:</b> Discrete Event Simulation, SimPy, Queuing Theory, University Transit Optimization, Bus Dispatch Scheduling, Monte Carlo Methods, Urban Logistical Engineering.", abstract_text))
    elements.append(Spacer(1, 10))

    # Section 1: Introduction & Problem Statement
    elements.append(Paragraph("1. INTRODUCTION & PROBLEM STATEMENT", h1_style))
    elements.append(Paragraph(
        "Transit operations at university campuses situated outside major metropolitan cores represent a critical "
        "logistical lifeline. MUET Jamshoro serves as the premier engineering university in Sindh, with the overwhelming "
        "majority of its commuter population residing 15 to 30 kilometers away across the Indus river in Hyderabad. "
        "The university operates approximately 25 dedicated buses ('Points') that depart from two primary campus hubs: "
        "the <b>Student Teacher Center (STC)</b> and the <b>Main Gate Terminal</b>.<br/><br/>"
        "Under current operating practices, buses adhere to a <i>static timetable</i>. Buses are dispatched at fixed clock "
        "intervals regardless of actual student accumulation at terminals. Consequently, during the morning peak (08:00--09:00 AM) "
        "and afternoon class dismissals (02:00--03:30 PM), queues swell to hundreds of students, while during midday hours "
        "(10:30 AM--01:30 PM), buses run underutilized or sit idle. Furthermore, unexpected traffic congestion along the "
        "Jamshoro Toll Plaza and Indus Highway induces severe schedule desynchronization. The core objective of this "
        "investigation is to determine how algorithmic scheduling can minimize student waiting times and maximize fleet "
        "utilization within the exact confines of the existing 25-bus fleet.",
        body_style
    ))

    # Section 2: Mathematical Modeling
    elements.append(Paragraph("2. MATHEMATICAL MODELING & QUEUING THEORY", h1_style))
    elements.append(Paragraph(
        "Campus transit cannot be characterized by standard M/M/1 or M/M/c single-server queuing formulations because "
        "passengers are served in discrete batches governed by finite bus seating capacity (C = 55). The system is modeled "
        "as an <b>M(t)/G^[C]/c</b> bulk service queuing network with time-dependent arrival intensity.",
        body_style
    ))

    elements.append(Paragraph("<b>A. Non-Homogeneous Poisson Arrival Process (NHPP)</b>", h2_style))
    elements.append(Paragraph(
        "Passenger arrivals at terminal <i>i</i> are governed by arrival intensity &lambda;<sub>i</sub>(t) across five distinct "
        "operational time windows: Early Morning (07:30--08:00, &lambda;=3-4 pax/min), Morning Peak (08:00--09:00, &lambda;=12-15 pax/min), "
        "Mid-Day Inter-peak (09:00--14:00, &lambda;=2.5-3 pax/min), Afternoon Peak (14:00--15:30, &lambda;=14-16 pax/min), and Evening "
        "Off-peak (&lambda;=2 pax/min). Inter-arrival times are sampled via inverse transform sampling: &Delta;t = -ln(1 - U) / &lambda;(t), U ~ Uniform(0,1).",
        body_style
    ))

    elements.append(Paragraph("<b>B. Bulk Boarding & Capacity Constraints</b>", h2_style))
    elements.append(Paragraph(
        "When bus <i>b</i> initiates boarding for route <i>r</i> at time <i>t</i>, the boarded passenger count is bounded strictly by: "
        "<b>P<sub>b</sub> = min(Q<sub>i</sub>(r, t), C)</b> where C = 55 seats. Excess passengers Q<sub>i</sub> - C remain in the FIFO queue "
        "and are recorded as <i>left behind</i>. Passenger step-in boarding delay follows &tau;<sub>k</sub> ~ Uniform(1.5, 3.0) seconds.",
        body_style
    ))

    elements.append(Paragraph("<b>C. Stochastic Traffic Delay Formulation</b>", h2_style))
    elements.append(Paragraph(
        "Highway transit round-trip duration is governed by: <b>T<sub>trip</sub>(r) = 2 &times; T<sub>base</sub>(r) + &Delta;T<sub>traffic</sub> + T<sub>alight</sub></b>, "
        "where highway delay &Delta;T<sub>traffic</sub> follows a Log-normal distribution: &Delta;T<sub>traffic</sub> ~ Lognormal(&mu;, &sigma;), "
        "ensuring positive, right-skewed highway congestion behavior.",
        body_style
    ))

    # Section 3: Scheduling Algorithms & Code Snippet
    elements.append(Paragraph("3. SCHEDULING ALGORITHM IMPLEMENTATIONS", h1_style))
    elements.append(Paragraph(
        "Four distinct dispatch paradigms were implemented and benchmarked under identical fleet constraints:<br/>"
        "<b>1. Algorithm 1 (Fixed Schedule - Baseline):</b> Dispatches buses at rigid, predefined clock times.<br/>"
        "<b>2. Algorithm 2 (Demand-Based Headway):</b> Contracts departure headways to 7-8 minutes during peak periods and expands to 25 minutes during mid-day.<br/>"
        "<b>3. Algorithm 3 (Dynamic Queue-Based):</b> Closed-loop threshold control that triggers an immediate dispatch whenever a queue reaches 45 passengers (&asymp;82% capacity) or an elapsed maximum wait time (20 min) is exceeded.<br/>"
        "<b>4. Algorithm 4 (Traffic-Aware Adaptive):</b> Dynamically modulates dispatch thresholds using real-time highway transit delay multipliers to prevent turnaround bottlenecks.",
        body_style
    ))

    # Code snippet block
    elements.append(Paragraph("<b>Listing 1: Dynamic Queue-Based Dispatch Engine (algorithms/dynamic_queue.py)</b>", h2_style))
    code_text = (
        "def run(self):\n"
        "    while True:\n"
        "        current_time = self.env.now\n"
        "        for terminal, routes in self.routes_by_terminal.items():\n"
        "            stop = self.stops[terminal]\n"
        "            for route_id in routes:\n"
        "                q_len = stop.get_queue_length(route_id)\n"
        "                time_since_last = current_time - self.last_dispatch_time.get(route_id, 0.0)\n"
        "                # Threshold Trigger: Queue >= 45 pax OR max headway elapsed with waiting pax\n"
        "                trigger = (q_len >= self.queue_threshold) or (q_len > 15 and time_since_last >= MAX_IDLE_WAIT_TIME)\n"
        "                if trigger:\n"
        "                    bus = self.bus_ops.reserve_and_dispatch_bus(route_id, terminal, trip_id)\n"
        "                    if bus:\n"
        "                        self.last_dispatch_time[route_id] = current_time\n"
        "        yield self.env.timeout(self.check_interval)"
    )
    code_table = Table([[Paragraph(f"<pre>{code_text}</pre>", code_style)]], colWidths=[540])
    code_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F4F6F7")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#BDC3C7")),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    elements.append(code_table)
    elements.append(Spacer(1, 10))

    # Section 4: Experimental Results & Table
    elements.append(Paragraph("4. EXPERIMENTAL SCENARIOS & QUANTITATIVE RESULTS", h1_style))
    elements.append(Paragraph(
        "A total of 140 comprehensive simulation runs were executed across 7 operational What-If scenarios with 5 independent "
        "Monte Carlo replications each. Table I presents the consolidated empirical results.",
        body_style
    ))

    # Table of Results
    table_data = [
        ["Scenario", "Algorithm", "Mean Wait (min)", "Wait Imprv (%)", "Left Behind (Pax)", "Left Behind Red. (%)", "Fleet Util (%)", "Trips"],
        ["1. Normal Demand", "Baseline (Fixed)", "67.13", "0.00%", "4,314.6", "0.00%", "42.36%", "76.0"],
        ["", "Demand-Based", "37.61", "43.97%", "3,457.6", "19.86%", "64.64%", "125.4"],
        ["", "Dynamic Queue", "21.92", "67.34%", "2,027.4", "53.01%", "70.94%", "140.0"],
        ["", "Traffic-Aware", "26.25", "60.89%", "2,520.4", "41.58%", "73.74%", "145.0"],
        ["2. High Morning", "Baseline (Fixed)", "108.29", "0.00%", "5,213.8", "0.00%", "42.41%", "76.0"],
        ["", "Dynamic Queue", "29.75", "72.53%", "3,051.6", "41.47%", "75.73%", "149.0"],
        ["", "Traffic-Aware", "36.24", "66.54%", "3,489.0", "33.08%", "77.49%", "150.8"],
        ["3. High Afternoon", "Baseline (Fixed)", "68.98", "0.00%", "5,599.6", "0.00%", "42.39%", "76.0"],
        ["", "Dynamic Queue", "25.15", "63.55%", "3,861.8", "31.03%", "70.19%", "137.8"],
        ["", "Traffic-Aware", "28.24", "59.06%", "4,072.2", "27.28%", "73.05%", "143.0"],
        ["4. Heavy Traffic", "Baseline (Fixed)", "67.13", "0.00%", "4,314.6", "0.00%", "50.94%", "73.2"],
        ["", "Dynamic Queue", "27.76", "58.65%", "2,728.0", "36.77%", "77.23%", "118.0"],
        ["", "Traffic-Aware", "31.77", "52.67%", "2,893.4", "32.94%", "79.28%", "121.8"],
        ["5. Sudden Surge", "Baseline (Fixed)", "138.97", "0.00%", "8,983.2", "0.00%", "47.60%", "75.0"],
        ["", "Dynamic Queue", "55.60", "59.99%", "7,607.6", "15.31%", "83.64%", "140.6"],
        ["", "Traffic-Aware", "59.14", "57.45%", "7,152.0", "20.38%", "84.04%", "142.2"],
        ["6. Uneven Demand", "Baseline (Fixed)", "60.43", "0.00%", "3,845.8", "0.00%", "42.30%", "76.0"],
        ["", "Dynamic Queue", "28.42", "52.97%", "3,030.2", "21.21%", "66.55%", "131.2"],
        ["", "Traffic-Aware", "31.58", "47.74%", "2,807.6", "27.00%", "71.51%", "141.0"],
        ["7. Reduced Fleet", "Baseline (Fixed)", "67.13", "0.00%", "4,314.6", "0.00%", "58.83%", "76.0"],
        ["(18 Buses)", "Dynamic Queue", "32.25", "51.96%", "2,870.6", "33.47%", "81.51%", "113.4"],
        ["", "Traffic-Aware", "37.00", "44.89%", "3,270.8", "24.19%", "82.51%", "114.4"]
    ]

    res_table = Table(table_data, colWidths=[90, 85, 65, 65, 75, 75, 55, 30])
    res_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0B2F4C")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 7),
        ('ALIGN', (2,0), (-1,-1), 'CENTER'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#BDC3C7")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8F9F9")]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    elements.append(res_table)
    elements.append(Spacer(1, 10))

    # Section 5: Simulation Visualizations
    elements.append(Paragraph("5. PUBLICATION-GRADE SIMULATION VISUALIZATIONS", h1_style))
    elements.append(Paragraph(
        "All visual figures below are generated directly from the simulation execution outputs and saved at 300 DPI.",
        body_style
    ))

    # Grid of Graphs
    g1 = os.path.join(GRAPHS_DIR, "1_passenger_arrival_rates.png")
    g2 = os.path.join(GRAPHS_DIR, "2_queue_length_stc.png")
    g4 = os.path.join(GRAPHS_DIR, "4_waiting_time_comparison.png")
    g6 = os.path.join(GRAPHS_DIR, "6_fleet_utilization_comparison.png")
    g8 = os.path.join(GRAPHS_DIR, "8_algorithm_overall_comparison.png")
    g9 = os.path.join(GRAPHS_DIR, "9_demand_vs_capacity.png")

    if os.path.exists(g1):
        elements.append(Image(g1, width=6.5*inch, height=2.6*inch))
        elements.append(Paragraph("Figure 1: Non-Homogeneous Passenger Arrival Rates (&lambda;(t)) Across the Operating Day.", caption_style))

    if os.path.exists(g2):
        elements.append(Image(g2, width=6.5*inch, height=2.6*inch))
        elements.append(Paragraph("Figure 2: Terminal Queue Dynamics at STC Terminal (Baseline vs Traffic-Aware Optimized).", caption_style))

    if os.path.exists(g4):
        elements.append(Image(g4, width=6.5*inch, height=2.8*inch))
        elements.append(Paragraph("Figure 3: Average Passenger Waiting Times Across All 7 Operational Scenarios.", caption_style))

    if os.path.exists(g6):
        elements.append(Image(g6, width=6.5*inch, height=2.6*inch))
        elements.append(Paragraph("Figure 4: Fleet Utilization Rates Across Operational Scenarios (Conserving Fleet Size B=25).", caption_style))

    if os.path.exists(g9):
        elements.append(Image(g9, width=6.5*inch, height=2.6*inch))
        elements.append(Paragraph("Figure 5: Peak-Hour Passenger Demand vs Offered Fleet Seating Capacity.", caption_style))

    # Section 6: Administrative Recommendations & Conclusion
    elements.append(Paragraph("6. ACTIONABLE RECOMMENDATIONS FOR MUET TRANSPORT ADMINISTRATION", h1_style))
    elements.append(Paragraph(
        "<b>1. Transition from Rigid Timetables to Threshold Dispatching:</b> Dispatching Point buses dynamically when "
        "terminal queues approach 45 students immediately resolves queue accumulation and decreases waiting times by up to 72.5%.<br/>"
        "<b>2. Install Automated Queue Sensing Infrastructure:</b> Low-cost optical turnstiles or RFID tap-in counters at "
        "STC and Main Gate will provide the dispatch office with real-time passenger counts to automate dispatch triggers.<br/>"
        "<b>3. Strategic Fleet Staging:</b> Pre-positioning return buses at STC terminal at 01:45 PM prior to the 02:00 PM "
        "dismissal surge eliminates the catastrophic afternoon queue spikes.<br/>"
        "<b>4. Staggered Driver Maintenance Shifts:</b> Align active bus driver shifts strictly with 08:00--09:00 AM and "
        "02:00--03:30 PM peak windows, shifting mechanical maintenance to the 10:30 AM--01:00 PM off-peak interval.",
        body_style
    ))

    elements.append(Paragraph("7. CONCLUSION", h1_style))
    elements.append(Paragraph(
        "This Problem-Based Learning project verified that the campus commuting bottlenecks at MUET Jamshoro are not "
        "caused by an insufficient fleet size, but by static timetable scheduling. By implementing discrete event simulation "
        "with dynamic queue-threshold and traffic-adaptive dispatch policies, student waiting times are curtailed by up to 72.5%, "
        "and fleet productivity is nearly doubled without spending any capital on new buses.",
        body_style
    ))

    # References
    elements.append(Paragraph("REFERENCES", h1_style))
    refs = [
        "[1] D. Gross, J. F. Shortle, J. M. Thompson, and C. M. Harris, <i>Fundamentals of Queueing Theory</i>, 4th ed. Hoboken, NJ: John Wiley & Sons, 2008.",
        "[2] R. C. Larson and A. R. Odoni, <i>Urban Operations Research</i>. Englewood Cliffs, NJ: Prentice-Hall, 1981.",
        "[3] J. D. C. Little, 'A proof for the queuing formula: L = &lambda;W,' <i>Operations Research</i>, vol. 9, no. 3, pp. 383--387, 1961.",
        "[4] A. M. Law, <i>Simulation Modeling and Analysis</i>, 5th ed. New York, NY: McGraw-Hill Education, 2015.",
        "[5] J. Banks, J. S. Carson, B. L. Nelson, and D. M. Nicol, <i>Discrete-Event System Simulation</i>, 4th ed. Upper Saddle River, NJ: Pearson Prentice Hall, 2005."
    ]
    for r in refs:
        elements.append(Paragraph(r, body_style))

    doc.build(elements)
    print(f"IEEE-Style Academic PDF Report successfully generated at: {pdf_path}")
    return pdf_path

if __name__ == "__main__":
    build_pdf()
