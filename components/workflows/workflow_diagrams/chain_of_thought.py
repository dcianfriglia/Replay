import streamlit as st


def render_chain_of_thought_diagram():
    """Render Chain-of-Thought workflow diagram"""

    html = """
    <div class="workflow-diagram">
        <svg viewBox="0 0 800 200" xmlns="http://www.w3.org/2000/svg">
            <!-- Input Node -->
            <circle cx="100" cy="100" r="30" fill="#f8d7da" stroke="#721c24" stroke-width="2"/>
            <text x="100" y="105" text-anchor="middle" font-family="sans-serif">In</text>

            <!-- LLM Call 1 -->
            <rect x="180" y="70" width="100" height="60" rx="5" ry="5" fill="#d4edda" stroke="#155724" stroke-width="2"/>
            <text x="230" y="105" text-anchor="middle" font-family="sans-serif">LLM Call 1</text>

            <!-- Output 1 arrow -->
            <text x="310" y="85" text-anchor="middle" font-family="sans-serif" font-size="12">Output 1</text>
            <line x1="280" y1="100" x2="350" y2="100" stroke="#6c757d" stroke-width="2"/>
            <polygon points="350,100 340,95 340,105" fill="#6c757d"/>

            <!-- Gate -->
            <rect x="350" y="70" width="100" height="60" rx="5" ry="5" fill="#cce5ff" stroke="#004085" stroke-width="2"/>
            <text x="400" y="105" text-anchor="middle" font-family="sans-serif">Gate</text>

            <!-- Pass arrow -->
            <text x="430" y="80" text-anchor="middle" font-family="sans-serif" font-size="12">Pass</text>
            <line x1="450" y1="90" x2="500" y2="90" stroke="#6c757d" stroke-width="2"/>
            <polygon points="500,90 490,85 490,95" fill="#6c757d"/>

            <!-- Fail arrow -->
            <text x="430" y="150" text-anchor="middle" font-family="sans-serif" font-size="12">Fail</text>
            <line x1="400" y1="130" x2="400" y2="160" stroke="#6c757d" stroke-width="2" stroke-dasharray="5,5"/>
            <line x1="400" y1="160" x2="500" y2="160" stroke="#6c757d" stroke-width="2" stroke-dasharray="5,5"/>
            <polygon points="500,160 490,155 490,165" fill="#6c757d"/>

            <!-- LLM Call 2 -->
            <rect x="500" y="60" width="100" height="60" rx="5" ry="5" fill="#d4edda" stroke="#155724" stroke-width="2"/>
            <text x="550" y="95" text-anchor="middle" font-family="sans-serif">LLM Call 2</text>

            <!-- Output 2 arrow -->
            <text x="630" y="85" text-anchor="middle" font-family="sans-serif" font-size="12">Output 2</text>
            <line x1="600" y1="90" x2="640" y2="90" stroke="#6c757d" stroke-width="2"/>
            <polygon points="640,90 630,85 630,95" fill="#6c757d"/>

            <!-- LLM Call 3 -->
            <rect x="640" y="60" width="100" height="60" rx="5" ry="5" fill="#d4edda" stroke="#155724" stroke-width="2"/>
            <text x="690" y="95" text-anchor="middle" font-family="sans-serif">LLM Call 3</text>

            <!-- Final Output arrow -->
            <line x1="740" y1="90" x2="770" y2="90" stroke="#6c757d" stroke-width="2"/>
            <polygon points="770,90 760,85 760,95" fill="#6c757d"/>

            <!-- Output Node -->
            <circle cx="770" cy="90" r="30" fill="#f8d7da" stroke="#721c24" stroke-width="2"/>
            <text x="770" y="95" text-anchor="middle" font-family="sans-serif">Out</text>

            <!-- Exit Node -->
            <circle cx="500" cy="160" r="30" fill="#f8d7da" stroke="#721c24" stroke-width="2"/>
            <text x="500" y="165" text-anchor="middle" font-family="sans-serif">Exit</text>

            <!-- Input to LLM arrow -->
            <line x1="130" y1="100" x2="180" y2="100" stroke="#6c757d" stroke-width="2"/>
            <polygon points="180,100 170,95 170,105" fill="#6c757d"/>
        </svg>
        <p class="diagram-caption">The Chain-of-Thought workflow with gate checks</p>
    </div>
    """

    st.markdown(html, unsafe_allow_html=True)