import streamlit as st


def render_parallelization_diagram():
    """Render Parallelization workflow diagram"""

    html = """
    <div class="workflow-diagram">
        <svg viewBox="0 0 800 200" xmlns="http://www.w3.org/2000/svg">
            <!-- Input Node -->
            <circle cx="100" cy="100" r="30" fill="#f8d7da" stroke="#721c24" stroke-width="2"/>
            <text x="100" y="105" text-anchor="middle" font-family="sans-serif">In</text>

            <!-- LLM Calls -->
            <rect x="220" y="30" width="100" height="60" rx="5" ry="5" fill="#d4edda" stroke="#155724" stroke-width="2"/>
            <text x="270" y="65" text-anchor="middle" font-family="sans-serif">LLM Call 1</text>

            <rect x="220" y="100" width="100" height="60" rx="5" ry="5" fill="#d4edda" stroke="#155724" stroke-width="2"/>
            <text x="270" y="135" text-anchor="middle" font-family="sans-serif">LLM Call 2</text>

            <rect x="220" y="170" width="100" height="60" rx="5" ry="5" fill="#d4edda" stroke="#155724" stroke-width="2"/>
            <text x="270" y="205" text-anchor="middle" font-family="sans-serif">LLM Call 3</text>

            <!-- Input arrows -->
            <line x1="130" y1="100" x2="180" y2="100" stroke="#6c757d" stroke-width="2"/>
            <polygon points="180,100 170,95 170,105" fill="#6c757d"/>

            <line x1="180" y1="100" x2="220" y2="60" stroke="#6c757d" stroke-width="2"/>
            <polygon points="220,60 210,65 215,55" fill="#6c757d"/>

            <line x1="180" y1="100" x2="220" y2="130" stroke="#6c757d" stroke-width="2"/>
            <polygon points="220,130 210,125 210,135" fill="#6c757d"/>

            <line x1="180" y1="100" x2="220" y2="200" stroke="#6c757d" stroke-width="2"/>
            <polygon points="220,200 210,195 215,205" fill="#6c757d"/>

            <!-- Aggregator -->
            <rect x="400" y="70" width="120" height="60" rx="5" ry="5" fill="#cce5ff" stroke="#004085" stroke-width="2"/>
            <text x="460" y="105" text-anchor="middle" font-family="sans-serif">Aggregator</text>

            <!-- Output arrows to Aggregator -->
            <line x1="320" y1="60" x2="400" y2="100" stroke="#6c757d" stroke-width="2"/>
            <polygon points="400,100 390,95 390,105" fill="#6c757d"/>

            <line x1="320" y1="130" x2="400" y2="100" stroke="#6c757d" stroke-width="2"/>
            <polygon points="400,100 390,105 395,95" fill="#6c757d"/>

            <line x1="320" y1="200" x2="400" y2="100" stroke="#6c757d" stroke-width="2"/>
            <polygon points="400,100 395,110 390,100" fill="#6c757d"/>

            <!-- Output Node -->
            <circle cx="600" cy="100" r="30" fill="#f8d7da" stroke="#721c24" stroke-width="2"/>
            <text x="600" y="105" text-anchor="middle" font-family="sans-serif">Out</text>

            <!-- Aggregator to Output arrow -->
            <line x1="520" y1="100" x2="570" y2="100" stroke="#6c757d" stroke-width="2"/>
            <polygon points="570,100 560,95 560,105" fill="#6c757d"/>
        </svg>
        <p class="diagram-caption">The Parallelization workflow showing multiple parallel LLM calls</p>
    </div>
    """

    st.markdown(html, unsafe_allow_html=True)