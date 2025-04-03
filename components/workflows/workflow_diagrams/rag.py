import streamlit as st


def render_rag_diagram():
    """Render Retrieval-Augmented Generation workflow diagram"""

    html = """
    <div class="workflow-diagram">
        <svg viewBox="0 0 800 250" xmlns="http://www.w3.org/2000/svg">
            <!-- Input Node -->
            <circle cx="100" cy="125" r="30" fill="#f8d7da" stroke="#721c24" stroke-width="2"/>
            <text x="100" y="130" text-anchor="middle" font-family="sans-serif">In</text>

            <!-- LLM -->
            <rect x="220" y="95" width="120" height="60" rx="5" ry="5" fill="#d4edda" stroke="#155724" stroke-width="2"/>
            <text x="280" y="130" text-anchor="middle" font-family="sans-serif">LLM</text>

            <!-- Input to LLM arrow -->
            <line x1="130" y1="125" x2="220" y2="125" stroke="#6c757d" stroke-width="2"/>
            <polygon points="220,125 210,120 210,130" fill="#6c757d"/>

            <!-- Knowledge sources -->
            <rect x="380" y="20" width="170" height="40" rx="5" ry="5" fill="#fff3cd" stroke="#856404" stroke-width="2"/>
            <text x="465" y="45" text-anchor="middle" font-family="sans-serif" font-size="14">Internal Documentation</text>

            <rect x="380" y="70" width="170" height="40" rx="5" ry="5" fill="#fff3cd" stroke="#856404" stroke-width="2"/>
            <text x="465" y="95" text-anchor="middle" font-family="sans-serif" font-size="14">Industry Standards</text>

            <rect x="380" y="120" width="170" height="40" rx="5" ry="5" fill="#fff3cd" stroke="#856404" stroke-width="2"/>
            <text x="465" y="145" text-anchor="middle" font-family="sans-serif" font-size="14">Academic Research</text>

            <rect x="380" y="170" width="170" height="40" rx="5" ry="5" fill="#fff3cd" stroke="#856404" stroke-width="2"/>
            <text x="465" y="195" text-anchor="middle" font-family="sans-serif" font-size="14">Case Studies</text>

            <rect x="380" y="220" width="170" height="40" rx="5" ry="5" fill="#fff3cd" stroke="#856404" stroke-width="2"/>
            <text x="465" y="245" text-anchor="middle" font-family="sans-serif" font-size="14">Custom Knowledge Base</text>

            <!-- Query/Results arrows -->
            <path d="M 305 95 C 305 50, 350 40, 380 40" stroke="#6c757d" stroke-width="2" fill="transparent" stroke-dasharray="5,5"/>
            <polygon points="380,40 370,35 370,45" fill="#6c757d"/>
            <text x="325" y="50" text-anchor="middle" font-family="sans-serif" font-size="12">Query/Results</text>

            <path d="M 305 105 C 305 80, 350 90, 380 90" stroke="#6c757d" stroke-width="2" fill="transparent" stroke-dasharray="5,5"/>
            <polygon points="380,90 370,85 370,95" fill="#6c757d"/>

            <path d="M 305 115 C 305 120, 350 140, 380 140" stroke="#6c757d" stroke-width="2" fill="transparent" stroke-dasharray="5,5"/>
            <polygon points="380,140 370,135 370,145" fill="#6c757d"/>

            <path d="M 305 125 C 305 160, 350 190, 380 190" stroke="#6c757d" stroke-width="2" fill="transparent" stroke-dasharray="5,5"/>
            <polygon points="380,190 370,185 370,195" fill="#6c757d"/>

            <path d="M 305 135 C 305 200, 350 240, 380 240" stroke="#6c757d" stroke-width="2" fill="transparent" stroke-dasharray="5,5"/>
            <polygon points="380,240 370,235 370,245" fill="#6c757d"/>

            <!-- Output Node -->
            <circle cx="630" cy="125" r="30" fill="#f8d7da" stroke="#721c24" stroke-width="2"/>
            <text x="630" y="130" text-anchor="middle" font-family="sans-serif">Out</text>

            <!-- LLM to Output arrow -->
            <line x1="340" y1="125" x2="600" y2="125" stroke="#6c757d" stroke-width="2"/>
            <polygon points="600,125 590,120 590,130" fill="#6c757d"/>
            <text x="470" y="115" text-anchor="middle" font-family="sans-serif" font-size="12">Augmented Response</text>
        </svg>
        <p class="diagram-caption">The RAG workflow showing retrieval from external knowledge sources</p>
    </div>
    """

    st.markdown(html, unsafe_allow_html=True)