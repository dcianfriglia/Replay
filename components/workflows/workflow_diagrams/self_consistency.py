import streamlit as st


def render_self_consistency_diagram():
    """Render Self-Consistency workflow diagram"""

    html = """
    <div class="workflow-diagram">
        <svg viewBox="0 0 800 250" xmlns="http://www.w3.org/2000/svg">
            <!-- Input Node -->
            <circle cx="100" cy="125" r="30" fill="#f8d7da" stroke="#721c24" stroke-width="2"/>
            <text x="100" y="130" text-anchor="middle" font-family="sans-serif">In</text>

            <!-- Input arrow -->
            <line x1="130" y1="125" x2="180" y2="125" stroke="#6c757d" stroke-width="2"/>
            <polygon points="180,125 170,120 170,130" fill="#6c757d"/>

            <!-- Multiple reasoning paths -->
            <rect x="180" y="50" width="140" height="50" rx="5" ry="5" fill="#d4edda" stroke="#155724" stroke-width="2"/>
            <text x="250" y="75" text-anchor="middle" font-family="sans-serif">Reasoning Path 1</text>

            <rect x="180" y="110" width="140" height="50" rx="5" ry="5" fill="#d4edda" stroke="#155724" stroke-width="2"/>
            <text x="250" y="135" text-anchor="middle" font-family="sans-serif">Reasoning Path 2</text>

            <rect x="180" y="170" width="140" height="50" rx="5" ry="5" fill="#d4edda" stroke="#155724" stroke-width="2"/>
            <text x="250" y="195" text-anchor="middle" font-family="sans-serif">Reasoning Path 3</text>

            <!-- Branching lines -->
            <line x1="180" y1="125" x2="180" y2="75" stroke="#6c757d" stroke-width="2"/>
            <line x1="180" y1="125" x2="180" y2="135" stroke="#6c757d" stroke-width="2"/>
            <line x1="180" y1="125" x2="180" y2="195" stroke="#6c757d" stroke-width="2"/>

            <!-- Conclusions -->
            <rect x="360" y="50" width="140" height="50" rx="5" ry="5" fill="#f0f9ff" stroke="#0c63e4" stroke-width="2"/>
            <text x="430" y="75" text-anchor="middle" font-family="sans-serif">Conclusion 1</text>

            <rect x="360" y="110" width="140" height="50" rx="5" ry="5" fill="#f0f9ff" stroke="#0c63e4" stroke-width="2"/>
            <text x="430" y="135" text-anchor="middle" font-family="sans-serif">Conclusion 2</text>

            <rect x="360" y="170" width="140" height="50" rx="5" ry="5" fill="#f0f9ff" stroke="#0c63e4" stroke-width="2"/>
            <text x="430" y="195" text-anchor="middle" font-family="sans-serif">Conclusion 3</text>

            <!-- Reasoning to Conclusion arrows -->
            <line x1="320" y1="75" x2="360" y2="75" stroke="#6c757d" stroke-width="2"/>
            <polygon points="360,75 350,70 350,80" fill="#6c757d"/>

            <line x1="320" y1="135" x2="360" y2="135" stroke="#6c757d" stroke-width="2"/>
            <polygon points="360,135 350,130 350,140" fill="#6c757d"/>

            <line x1="320" y1="195" x2="360" y2="195" stroke="#6c757d" stroke-width="2"/>
            <polygon points="360,195 350,190 350,200" fill="#6c757d"/>

            <!-- Consistency Checker -->
            <rect x="540" y="95" width="140" height="60" rx="5" ry="5" fill="#cce5ff" stroke="#004085" stroke-width="2"/>
            <text x="610" y="125" text-anchor="middle" font-family="sans-serif">Consistency</text>
            <text x="610" y="145" text-anchor="middle" font-family="sans-serif">Checker</text>

            <!-- Conclusion to Checker arrows -->
            <line x1="500" y1="75" x2="540" y2="115" stroke="#6c757d" stroke-width="2"/>
            <polygon points="540,115 530,110 535,120" fill="#6c757d"/>

            <line x1="500" y1="135" x2="540" y2="125" stroke="#6c757d" stroke-width="2"/>
            <polygon points="540,125 530,120 532,130" fill="#6c757d"/>

            <line x1="500" y1="195" x2="540" y2="135" stroke="#6c757d" stroke-width="2"/>
            <polygon points="540,135 535,145 530,135" fill="#6c757d"/>

            <!-- Output Node -->
            <circle cx="730" cy="125" r="30" fill="#f8d7da" stroke="#721c24" stroke-width="2"/>
            <text x="730" y="130" text-anchor="middle" font-family="sans-serif">Out</text>

            <!-- Checker to Output arrow -->
            <line x1="680" y1="125" x2="700" y2="125" stroke="#6c757d" stroke-width="2"/>
            <polygon points="700,125 690,120 690,130" fill="#6c757d"/>
        </svg>
        <p class="diagram-caption">The Self-Consistency workflow showing multiple reasoning paths and consistency checking</p>
    </div>
    """

    st.markdown(html, unsafe_allow_html=True)