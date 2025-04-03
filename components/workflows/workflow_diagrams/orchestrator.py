import streamlit as st


def render_orchestrator_diagram():
    """Render Orchestrator-Workers workflow diagram"""

    html = """
    <div class="workflow-diagram">
        <svg viewBox="0 0 800 200" xmlns="http://www.w3.org/2000/svg">
            <!-- Input Node -->
            <circle cx="100" cy="100" r="30" fill="#f8d7da" stroke="#721c24" stroke-width="2"/>
            <text x="100" y="105" text-anchor="middle" font-family="sans-serif">In</text>

            <!-- Orchestrator -->
            <rect x="180" y="70" width="120" height="60" rx="5" ry="5" fill="#d4edda" stroke="#155724" stroke-width="2"/>
            <text x="240" y="105" text-anchor="middle" font-family="sans-serif">Orchestrator</text>

            <!-- Worker LLMs -->
            <rect x="380" y="20" width="100" height="60" rx="5" ry="5" fill="#d4edda" stroke="#155724" stroke-width="2"/>
            <text x="430" y="55" text-anchor="middle" font-family="sans-serif">LLM Call 1</text>

            <rect x="380" y="90" width="100" height="60" rx="5" ry="5" fill="#d4edda" stroke="#155724" stroke-width="2"/>
            <text x="430" y="125" text-anchor="middle" font-family="sans-serif">LLM Call 2</text>

            <rect x="380" y="160" width="100" height="60" rx="5" ry="5" fill="#d4edda" stroke="#155724" stroke-width="2"/>
            <text x="430" y="195" text-anchor="middle" font-family="sans-serif">LLM Call 3</text>

            <!-- Orchestrator to Workers arrows -->
            <line x1="300" y1="85" x2="380" y2="50" stroke="#6c757d" stroke-width="2" stroke-dasharray="5,5"/>
            <polygon points="380,50 370,48 372,58" fill="#6c757d"/>

            <line x1="300" y1="100" x2="380" y2="120" stroke="#6c757d" stroke-width="2" stroke-dasharray="5,5"/>
            <polygon points="380,120 370,115 370,125" fill="#6c757d"/>

            <line x1="300" y1="115" x2="380" y2="180" stroke="#6c757d" stroke-width="2" stroke-dasharray="5,5"/>
            <polygon points="380,180 370,175 374,185" fill="#6c757d"/>

            <!-- Synthesizer -->
            <rect x="550" y="70" width="120" height="60" rx="5" ry="5" fill="#cce5ff" stroke="#004085" stroke-width="2"/>
            <text x="610" y="105" text-anchor="middle" font-family="sans-serif">Synthesizer</text>

            <!-- Workers to Synthesizer arrows -->
            <line x1="480" y1="50" x2="550" y2="90" stroke="#6c757d" stroke-width="2" stroke-dasharray="5,5"/>
            <polygon points="550,90 540,85 540,95" fill="#6c757d"/>

            <line x1="480" y1="120" x2="550" y2="100" stroke="#6c757d" stroke-width="2" stroke-dasharray="5,5"/>
            <polygon points="550,100 540,105 542,95" fill="#6c757d"/>

            <line x1="480" y1="190" x2="550" y2="110" stroke="#6c757d" stroke-width="2" stroke-dasharray="5,5"/>
            <polygon points="550,110 545,120 540,110" fill="#6c757d"/>

            <!-- Output Node -->
            <circle cx="720" cy="100" r="30" fill="#f8d7da" stroke="#721c24" stroke-width="2"/>
            <text x="720" y="105" text-anchor="middle" font-family="sans-serif">Out</text>

            <!-- Synthesizer to Output arrow -->
            <line x1="670" y1="100" x2="690" y2="100" stroke="#6c757d" stroke-width="2"/>
            <polygon points="690,100 680,95 680,105" fill="#6c757d"/>

            <!-- Input to Orchestrator arrow -->
            <line x1="130" y1="100" x2="180" y2="100" stroke="#6c757d" stroke-width="2"/>
            <polygon points="180,100 170,95 170,105" fill="#6c757d"/>
        </svg>
        <p class="diagram-caption">The Orchestrator-Workers workflow with dynamic task delegation</p>
    </div>
    """

    st.markdown(html, unsafe_allow_html=True)