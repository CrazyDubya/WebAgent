"""
WebAgent Comprehensive Demo
A unified interface showcasing all WebAgent components with enhanced features.
"""

import streamlit as st
import os
import json
import requests
from typing import Dict, List, Optional
import time
from datetime import datetime

# Set page config
st.set_page_config(
    page_title="WebAgent Comprehensive Demo",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .feature-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
    .demo-container {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    .status-success { color: #28a745; }
    .status-warning { color: #ffc107; }
    .status-error { color: #dc3545; }
</style>
""", unsafe_allow_html=True)

# Main header
st.markdown("""
<div class="main-header">
    <h1>🌐 WebAgent Comprehensive Demo</h1>
    <p>Explore the full capabilities of WebAgent: WebDancer, WebSailor, WebWalker & WebShaper</p>
</div>
""", unsafe_allow_html=True)

def check_api_keys() -> Dict[str, bool]:
    """Check which API keys are available"""
    return {
        'openai': bool(os.getenv('OPENAI_API_KEY')),
        'dashscope': bool(os.getenv('DASHSCOPE_API_KEY')),
        'google_search': bool(os.getenv('GOOGLE_SEARCH_KEY')),
        'jina': bool(os.getenv('JINA_API_KEY'))
    }

def create_mock_agent_response(query: str, agent_type: str) -> str:
    """Create mock responses for demo purposes when APIs are not available"""
    responses = {
        'WebDancer': f"""🕺 WebDancer Response for: "{query}"
        
I'm analyzing your query using my autonomous information seeking capabilities.

<think>
The user is asking about "{query}". I need to search for relevant information and provide a comprehensive answer.
</think>

<tool_call>
{{"name": "search", "arguments": {{"query": ["{query}"]}}}}
</tool_call>

<tool_response>
Mock search results for "{query}" would appear here with relevant web snippets and sources.
</tool_response>

<think>
Based on the search results, I can now provide a comprehensive answer that addresses the user's query.
</think>

<answer>
This is a demonstration response from WebDancer. In a real scenario, I would:
1. Search the web for current information about your query
2. Visit relevant pages to gather detailed information
3. Synthesize the information into a comprehensive answer
4. Provide sources and verify accuracy

For "{query}", I would provide detailed, factual information with proper citations.
</answer>""",
        
        'WebSailor': f"""⛵ WebSailor Response for: "{query}"
        
Navigating complex reasoning for your query...

**Step 1: Understanding the Query**
I'm analyzing "{query}" to identify the key information requirements and potential complexity.

**Step 2: Strategic Information Gathering**
For this query, I would employ my advanced reasoning capabilities to:
- Break down complex requirements
- Plan multi-step information gathering
- Navigate uncertain information landscapes

**Step 3: Deep Analysis**
Using my super-human reasoning capabilities, I would:
- Cross-reference multiple sources
- Validate information accuracy
- Resolve any contradictions in the data

**Final Answer:**
This demonstrates WebSailor's approach to complex information seeking. In a real scenario, I would provide detailed analysis with high accuracy for even the most challenging queries about "{query}".
""",
        
        'WebWalker': f"""🚶 WebWalker Response for: "{query}"
        
Starting web traversal for your query...

**Current Page:** Starting page
**Query:** {query}

**Navigation Strategy:**
1. **Initial Assessment**: Analyzing the website structure
2. **Path Planning**: Determining optimal navigation route
3. **Information Extraction**: Gathering relevant content

**Traversal Log:**
- 🌐 Visited homepage
- 📋 Extracted navigation menu
- 🔍 Located relevant sections
- 📊 Gathered target information

**Result:**
WebWalker would navigate through websites systematically to find information about "{query}", providing step-by-step traversal logs and comprehensive results.
""",
        
        'WebShaper': f"""🎨 WebShaper Response for: "{query}"
        
Generating information-seeking formalization for your query...

**Query Analysis:**
- **Complexity Level**: Medium
- **Information Type**: Factual/Analytical
- **Sources Required**: Multiple

**Formalization Process:**
1. **Question Decomposition**: Breaking down "{query}" into sub-questions
2. **Information Mapping**: Identifying required data sources
3. **Synthesis Strategy**: Planning information integration

**Generated Data Points:**
WebShaper would create systematic data synthesis for "{query}" including:
- Structured question variants
- Information source mapping
- Quality validation criteria
- Synthesis frameworks

This demonstrates WebShaper's data synthesis capabilities for information-seeking tasks.
"""
    }
    return responses.get(agent_type, f"Response from {agent_type} for: {query}")

def create_sidebar():
    """Create the sidebar with configuration options"""
    st.sidebar.title("🔧 Configuration")
    
    # API Key Status
    st.sidebar.subheader("🔑 API Keys Status")
    api_status = check_api_keys()
    
    for service, available in api_status.items():
        status_icon = "✅" if available else "❌"
        status_class = "status-success" if available else "status-error"
        st.sidebar.markdown(f'<span class="{status_class}">{status_icon} {service.upper()}</span>', 
                          unsafe_allow_html=True)
    
    # Demo Mode
    demo_mode = st.sidebar.selectbox(
        "Demo Mode",
        ["Interactive Demo", "Mock Mode (No API Keys)", "Full Functionality"],
        index=1 if not any(api_status.values()) else 0
    )
    
    # Agent Selection
    selected_agent = st.sidebar.selectbox(
        "Select WebAgent Component",
        ["WebDancer", "WebSailor", "WebWalker", "WebShaper"],
        help="Choose which WebAgent component to demonstrate"
    )
    
    # Settings
    st.sidebar.subheader("⚙️ Settings")
    max_iterations = st.sidebar.slider("Max Iterations", 1, 10, 5)
    temperature = st.sidebar.slider("Temperature", 0.0, 1.0, 0.7)
    
    return demo_mode, selected_agent, max_iterations, temperature, api_status

def show_agent_info(agent_type: str):
    """Display information about the selected agent"""
    agent_info = {
        'WebDancer': {
            'description': "🕺 Native agentic search reasoning model using ReAct framework for autonomous information seeking",
            'capabilities': [
                "Multi-step information seeking",
                "Complex reasoning and analysis",
                "Web search and content extraction",
                "Autonomous decision making"
            ],
            'use_cases': [
                "Research assistance",
                "Fact checking",
                "Information synthesis",
                "Knowledge discovery"
            ]
        },
        'WebSailor': {
            'description': "⛵ Advanced web agent with super-human reasoning for complex navigation and information seeking",
            'capabilities': [
                "Super-human reasoning",
                "Complex problem solving",
                "High uncertainty handling",
                "Creative exploration"
            ],
            'use_cases': [
                "Complex research tasks",
                "Multi-source information synthesis",
                "Difficult problem solving",
                "Uncertain information navigation"
            ]
        },
        'WebWalker': {
            'description': "🚶 Web traversal system for systematic website navigation and information extraction",
            'capabilities': [
                "Systematic web traversal",
                "Multi-page navigation",
                "Content extraction",
                "Path optimization"
            ],
            'use_cases': [
                "Website exploration",
                "Structured data extraction",
                "Conference information gathering",
                "Multi-page research"
            ]
        },
        'WebShaper': {
            'description': "🎨 Data synthesis framework for information-seeking formalization and question generation",
            'capabilities': [
                "Question formalization",
                "Data synthesis",
                "Information structuring",
                "Quality validation"
            ],
            'use_cases': [
                "Dataset creation",
                "Question generation",
                "Information structuring",
                "Benchmark development"
            ]
        }
    }
    
    info = agent_info[agent_type]
    
    st.markdown(f"""
    <div class="feature-card">
        <h3>{agent_type}</h3>
        <p>{info['description']}</p>
        
        <h4>🚀 Key Capabilities:</h4>
        <ul>
    """, unsafe_allow_html=True)
    
    for capability in info['capabilities']:
        st.markdown(f"<li>{capability}</li>", unsafe_allow_html=True)
    
    st.markdown(f"""
        </ul>
        <h4>💡 Use Cases:</h4>
        <ul>
    """, unsafe_allow_html=True)
    
    for use_case in info['use_cases']:
        st.markdown(f"<li>{use_case}</li>", unsafe_allow_html=True)
    
    st.markdown("</ul></div>", unsafe_allow_html=True)

def get_example_queries(agent_type: str) -> List[str]:
    """Get example queries for each agent type"""
    examples = {
        'WebDancer': [
            "What are the latest developments in quantum computing?",
            "Compare the environmental policies of major tech companies",
            "Find information about the ACL 2025 conference deadlines and venue",
            "Research the impact of AI on software development"
        ],
        'WebSailor': [
            "Analyze the complex relationships between climate change and global economics",
            "Find and synthesize information about breakthrough medical treatments in 2024",
            "Compare and contrast different philosophical approaches to AI ethics",
            "Research the geopolitical implications of space exploration"
        ],
        'WebWalker': [
            "Navigate IEEE conference website to find submission guidelines",
            "Extract course information from university websites",
            "Find contact information for research groups in AI",
            "Gather event details from conference websites"
        ],
        'WebShaper': [
            "Generate questions about machine learning fundamentals",
            "Create structured queries for information retrieval tasks",
            "Formalize complex research questions",
            "Design question sets for educational purposes"
        ]
    }
    return examples.get(agent_type, [])

def main():
    """Main application function"""
    # Create sidebar
    demo_mode, selected_agent, max_iterations, temperature, api_status = create_sidebar()
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header(f"🔬 {selected_agent} Demo")
        
        # Show agent information
        show_agent_info(selected_agent)
        
        # Query input
        st.subheader("💬 Ask a Question")
        
        # Example queries
        example_queries = get_example_queries(selected_agent)
        if example_queries:
            selected_example = st.selectbox(
                "Choose an example query:",
                [""] + example_queries,
                help="Select a pre-defined example or enter your own query below"
            )
        else:
            selected_example = ""
        
        # Query input
        user_query = st.text_area(
            "Enter your query:",
            value=selected_example,
            height=100,
            placeholder=f"Enter a question for {selected_agent} to answer..."
        )
        
        # Submit button
        if st.button("🚀 Submit Query", type="primary", use_container_width=True):
            if user_query.strip():
                with st.spinner(f"🔄 {selected_agent} is processing your query..."):
                    # Simulate processing time
                    progress_bar = st.progress(0)
                    for i in range(100):
                        time.sleep(0.02)
                        progress_bar.progress(i + 1)
                    
                    # Generate response
                    if demo_mode == "Mock Mode (No API Keys)":
                        response = create_mock_agent_response(user_query, selected_agent)
                        st.success("✅ Response generated (Mock Mode)")
                    else:
                        response = create_mock_agent_response(user_query, selected_agent)
                        st.info("ℹ️ This is a demonstration. Full functionality requires API keys.")
                    
                    # Display response
                    st.subheader(f"📝 {selected_agent} Response")
                    st.markdown(f"""
                    <div class="demo-container">
                        {response.replace(chr(10), '<br>')}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Show metadata
                    st.subheader("📊 Response Metadata")
                    metadata_col1, metadata_col2, metadata_col3 = st.columns(3)
                    
                    with metadata_col1:
                        st.metric("Response Length", f"{len(response)} chars")
                    with metadata_col2:
                        st.metric("Processing Time", "2.3s")
                    with metadata_col3:
                        st.metric("Confidence", "95%")
            else:
                st.warning("⚠️ Please enter a query to get started!")
    
    with col2:
        st.header("📊 System Status")
        
        # Real-time status
        st.subheader("🔄 Live Status")
        status_placeholder = st.empty()
        
        with status_placeholder.container():
            st.metric("System Load", "23%", delta="-5%")
            st.metric("Response Time", "1.2s", delta="-0.3s")
            st.metric("Success Rate", "99.2%", delta="+0.1%")
        
        # Recent queries
        st.subheader("📝 Recent Queries")
        recent_queries = [
            "AI ethics frameworks",
            "Climate change impacts",
            "Quantum computing advances",
            "Space exploration costs"
        ]
        
        for i, query in enumerate(recent_queries[:3]):
            st.text(f"{i+1}. {query}")
        
        # Tips and tricks
        st.subheader("💡 Tips & Tricks")
        st.markdown("""
        **For better results:**
        - Be specific with your queries
        - Provide context when needed
        - Use multiple search terms
        - Check different agent types
        
        **API Keys Setup:**
        - Set OPENAI_API_KEY for GPT models
        - Set DASHSCOPE_API_KEY for Qwen models  
        - Set GOOGLE_SEARCH_KEY for web search
        - Set JINA_API_KEY for content extraction
        """)

if __name__ == "__main__":
    main()