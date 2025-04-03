import streamlit as st


def render_autonomous_agent_diagram():
    """Render Autonomous Agent workflow diagram"""

    html = """
    <div class="workflow-diagram">
        <svg viewBox="0 0 800 230" xmlns="http://www.w3.org/2000/svg">
            <!-- Human Node -->
            <circle cx="100" cy="80" r="30" fill="#f8d7da" stroke="#721c24" stroke-width="2"/>
            <text x="100" y="85" text-anchor="middle" font-family="sans-serif">Human</text>

            <!-- LLM Call (Agent) -->
            <rect x="300" y="50" width="100" height="60" rx="5" ry="5" fill="#d4edda" stroke="#155724" stroke-width="2"/>
            <text x="350" y="85" text-anchor="middle" font-family="sans-serif">LLM Call</text>

            <!-- Environment -->
            <rect x="580" y="50" width="120" height="60" rx="5" ry="5" fill="#fff3cd" stroke="#856404" stroke-width="2"/>
            <text x="640" y="85" text-anchor="middle" font-family="sans-serif">Environment</text>

            <!-- Stop -->
            <rect x="300" y="160" width="100" height="40" rx="5" ry="5" fill="#cce5ff" stroke="#004085" stroke-width="2"/>
            <text x="350" y="185" text-anchor="middle" font-family="sans-serif">Stop</text>

            <!-- Human to Agent arrow -->
            <line x1="130" y1="80" x2="300" y2="80" stroke="#6c757d" stroke-width="2" stroke-dasharray="5,5"/>
            <polygon points="300,80 290,75 290,85" fill="#6c757d"/>
            <text x="215" y="70" text-anchor="middle" font-family="sans-serif" font-size="12">Query</text>

            <!-- Agent to Human arrow -->
            <line x1="300" y1="60" x2="130" y2="60" stroke="#6c757d" stroke-width="2" stroke-dasharray="5,5"/>
            <polygon points="130,60 140,55 140,65" fill="#6c757d"/>
            <text x="215" y="50" text-anchor="middle" font-family="sans-serif" font-size="12">Clarify</text>

            <!-- Agent to Environment arrow -->
            <path d="M 400 70 C 450 70, 500 60, 580 60" stroke="#6c757d" stroke-width="2" fill="transparent"/>
            <polygon points="580,60 570,55 570,65" fill="#6c757d"/>
            <text x="490" y="50" text-anchor="middle" font-family="sans-serif" font-size="12">Action</text>

            <!-- Environment to Agent arrow -->
            <path d="M 580 100 C 500 100, 450 90, 400 90" stroke="#6c757d" stroke-width="2" fill="transparent"/>
            <polygon points="400,90 410,85 410,95" fill="#6c757d"/>
            <text x="490" y="110" text-anchor="middle" font-family="sans-serif" font-size="12">Feedback</text>

            <!-- Agent to Human (complete) arrow -->
            <path d="M 300 100 C 240 120, 200 110, 130 100" stroke="#6c757d" stroke-width="2" fill="transparent" stroke-dasharray="5,5"/>
            <polygon points="130,100 140,95 138,105" fill="#6c757d"/>
            <text x="215" y="130" text-anchor="middle" font-family="sans-serif" font-size="12">Complete</text>

            <!-- Agent to Stop arrow -->
            <line x1="350" y1="110" x2="350" y2="160" stroke="#6c757d" stroke-width="2" stroke-dasharray="5,5"/>
            <polygon points="350,160 345,150 355,150" fill="#6c757d"/>

            <!-- Loop arrow -->
            <path d="M 390 80 C 420 80, 420 120, 390 120, 370 120, 370 100, 390 100" stroke="#6c757d" stroke-width="2" fill="transparent"/>
            <polygon points="390,100 385,110 395,110" fill="#6c757d"/>

            <!-- "Until tasks clear" label -->
            <rect x="240" y="20" width="120" height="20" rx="5" ry="5" fill="white" stroke="none"/>
            <text x="300" y="35" text-anchor="middle" font-family="sans-serif" font-size="12">Until tasks clear</text>

            <!-- "Until tests pass" label -->
            <rect x="480" y="150" width="120" height="20" rx="5" ry="5" fill="white" stroke="none"/>
            <text x="540" y="165" text-anchor="middle" font-family="sans-serif" font-size="12">Until tests pass</text>
        </svg>
        <p class="diagram-caption">The Autonomous Agent workflow showing interaction between human, agent, and environment</p>
    </div>
    """

    st.markdown(html, unsafe_allow_html=True)