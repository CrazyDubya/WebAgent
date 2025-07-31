"""
WebAgent Interactive Playground
A comprehensive demonstration platform showcasing all WebAgent components
with interactive features, comparisons, and educational content.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time
import random
import json
from typing import Dict, List, Tuple
import os

# Page configuration
st.set_page_config(
    page_title="🤖 WebAgent Interactive Playground",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for enhanced styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .agent-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 1.5rem;
        border-radius: 15px;
        border: 2px solid #dee2e6;
        margin: 1rem 0;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .agent-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
    }
    
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        text-align: center;
        margin: 0.5rem 0;
    }
    
    .demo-output {
        background: #f8f9fa;
        border-left: 4px solid #007bff;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 5px;
    }
    
    .comparison-table {
        background: white;
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }
    
    .status-indicator {
        display: inline-block;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        margin-right: 8px;
    }
    
    .status-active { background-color: #28a745; }
    .status-warning { background-color: #ffc107; }
    .status-error { background-color: #dc3545; }
    
    .interactive-button {
        background: linear-gradient(135deg, #007bff 0%, #0056b3 100%);
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 25px;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .interactive-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 123, 255, 0.3);
    }
</style>
""", unsafe_allow_html=True)

class WebAgentPlayground:
    def __init__(self):
        self.agents = {
            'WebDancer': {
                'emoji': '🕺',
                'description': 'Native agentic search reasoning model',
                'capabilities': ['Multi-step reasoning', 'Autonomous search', 'Information synthesis'],
                'performance': {'accuracy': 95, 'speed': 88, 'complexity': 92},
                'use_cases': ['Research assistance', 'Fact verification', 'Content discovery']
            },
            'WebSailor': {
                'emoji': '⛵',
                'description': 'Super-human reasoning for web navigation',
                'capabilities': ['Complex reasoning', 'Uncertainty handling', 'Creative exploration'],
                'performance': {'accuracy': 97, 'speed': 82, 'complexity': 96},
                'use_cases': ['Complex problem solving', 'Multi-source synthesis', 'Deep research']
            },
            'WebWalker': {
                'emoji': '🚶',
                'description': 'Systematic web traversal and benchmarking',
                'capabilities': ['Systematic navigation', 'Content extraction', 'Path optimization'],
                'performance': {'accuracy': 90, 'speed': 94, 'complexity': 85},
                'use_cases': ['Website exploration', 'Data extraction', 'Structured queries']
            },
            'WebShaper': {
                'emoji': '🎨',
                'description': 'Data synthesis for information-seeking',
                'capabilities': ['Question generation', 'Data structuring', 'Quality validation'],
                'performance': {'accuracy': 93, 'speed': 91, 'complexity': 89},
                'use_cases': ['Dataset creation', 'Question formalization', 'Benchmark development']
            }
        }
        
        self.demo_scenarios = self._create_demo_scenarios()
        
    def _create_demo_scenarios(self) -> Dict:
        return {
            "Research Challenge": {
                "query": "Compare the environmental impact of different renewable energy technologies",
                "complexity": "High",
                "expected_steps": 8,
                "domains": ["Environmental Science", "Technology", "Policy"]
            },
            "Conference Information": {
                "query": "Find ACL 2025 submission deadlines and venue details",
                "complexity": "Medium", 
                "expected_steps": 4,
                "domains": ["Academic", "Events", "Conferences"]
            },
            "Technical Documentation": {
                "query": "How to implement distributed training in PyTorch?",
                "complexity": "Medium",
                "expected_steps": 6,
                "domains": ["Programming", "Machine Learning", "Documentation"]
            },
            "Market Analysis": {
                "query": "Analyze the current state of the quantum computing market",
                "complexity": "High",
                "expected_steps": 10,
                "domains": ["Technology", "Business", "Finance"]
            },
            "Health Information": {
                "query": "Latest developments in personalized medicine",
                "complexity": "High",
                "expected_steps": 7,
                "domains": ["Healthcare", "Research", "Technology"]
            }
        }

    def create_agent_comparison_chart(self) -> go.Figure:
        """Create a radar chart comparing agent capabilities"""
        categories = ['Accuracy', 'Speed', 'Complexity Handling']
        
        fig = go.Figure()
        
        for agent_name, agent_data in self.agents.items():
            perf = agent_data['performance']
            values = [perf['accuracy'], perf['speed'], perf['complexity']]
            
            fig.add_trace(go.Scatterpolar(
                r=values,
                theta=categories,
                fill='toself',
                name=f"{agent_data['emoji']} {agent_name}",
                line=dict(width=2)
            ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )),
            showlegend=True,
            title="Agent Performance Comparison",
            height=500
        )
        
        return fig

    def simulate_agent_response(self, agent_name: str, query: str, scenario_data: Dict) -> Dict:
        """Simulate agent response with realistic delays and metrics"""
        
        # Simulate processing time based on complexity
        complexity_map = {"Low": 1, "Medium": 2, "High": 3}
        base_time = complexity_map.get(scenario_data.get("complexity", "Medium"), 2)
        processing_time = base_time + random.uniform(0.5, 1.5)
        
        # Agent-specific responses
        responses = {
            'WebDancer': {
                'thinking_process': [
                    f"🤔 Analyzing query: '{query}'",
                    "🔍 Planning information search strategy",
                    "🌐 Initiating web search operations",
                    "📊 Evaluating and synthesizing results",
                    "✅ Generating comprehensive response"
                ],
                'final_answer': f"""Based on my autonomous information seeking analysis of "{query}", I have systematically searched and synthesized information from multiple sources. 

Key findings include:
• Comprehensive analysis across {len(scenario_data.get('domains', []))} domains
• Cross-referenced {scenario_data.get('expected_steps', 5)} primary sources
• Validated information accuracy through multiple verification steps

This demonstrates WebDancer's ability to perform deep, autonomous research with minimal human intervention.""",
                'metrics': {
                    'sources_consulted': random.randint(8, 15),
                    'confidence_score': random.uniform(0.85, 0.98),
                    'processing_steps': scenario_data.get('expected_steps', 5)
                }
            },
            
            'WebSailor': {
                'thinking_process': [
                    f"🧭 Navigating complex information landscape for: '{query}'",
                    "🌊 Applying super-human reasoning strategies", 
                    "🔄 Handling uncertainty and conflicting information",
                    "🎯 Synthesizing insights from multiple perspectives",
                    "⚓ Delivering high-confidence conclusions"
                ],
                'final_answer': f"""Through sophisticated reasoning and navigation of complex information spaces, I have analyzed "{query}" with super-human precision.

My analysis reveals:
• Multi-dimensional perspective across {', '.join(scenario_data.get('domains', []))}
• Resolution of {random.randint(2, 5)} conflicting information sources
• High-confidence synthesis with uncertainty quantification

WebSailor excels at navigating ambiguous information landscapes that challenge conventional approaches.""",
                'metrics': {
                    'sources_consulted': random.randint(10, 20),
                    'confidence_score': random.uniform(0.90, 0.99),
                    'complexity_handled': scenario_data.get('complexity', 'Medium')
                }
            },
            
            'WebWalker': {
                'thinking_process': [
                    f"👣 Planning systematic traversal for: '{query}'",
                    "🗺️ Mapping optimal navigation pathways",
                    "📄 Extracting structured information",
                    "🔗 Following relevant link chains",
                    "📊 Compiling comprehensive results"
                ],
                'final_answer': f"""Through systematic web traversal, I have navigated multiple websites to gather information about "{query}".

Navigation summary:
• Visited {random.randint(5, 12)} relevant web pages
• Extracted structured data from {len(scenario_data.get('domains', []))} domain areas
• Maintained {random.randint(85, 98)}% navigation efficiency

WebWalker provides methodical, comprehensive coverage of web-based information sources.""",
                'metrics': {
                    'pages_visited': random.randint(5, 12),
                    'extraction_efficiency': random.uniform(0.85, 0.98),
                    'navigation_depth': random.randint(3, 6)
                }
            },
            
            'WebShaper': {
                'thinking_process': [
                    f"🎨 Formalizing information-seeking structure for: '{query}'",
                    "📝 Generating structured question variants",
                    "🔧 Applying data synthesis methodologies",
                    "✨ Creating comprehensive information framework",
                    "📊 Validating synthesis quality"
                ],
                'final_answer': f"""I have applied advanced data synthesis techniques to formalize the information-seeking approach for "{query}".

Synthesis results:
• Generated {random.randint(15, 30)} structured sub-questions
• Created comprehensive information framework
• Validated approach across {len(scenario_data.get('domains', []))} domains

WebShaper enables systematic data synthesis and question formalization for complex information-seeking tasks.""",
                'metrics': {
                    'questions_generated': random.randint(15, 30),
                    'synthesis_quality': random.uniform(0.88, 0.97),
                    'framework_completeness': random.uniform(0.90, 0.99)
                }
            }
        }
        
        return {
            'processing_time': processing_time,
            'response_data': responses.get(agent_name, responses['WebDancer']),
            'timestamp': datetime.now()
        }

def create_main_header():
    """Create the main header with dynamic elements"""
    st.markdown("""
    <div class="main-header">
        <h1>🤖 WebAgent Interactive Playground</h1>
        <p>Explore the Full Capabilities of WebAgent Framework</p>
        <p><em>WebDancer • WebSailor • WebWalker • WebShaper</em></p>
    </div>
    """, unsafe_allow_html=True)

def create_agent_overview_cards(playground: WebAgentPlayground):
    """Create overview cards for each agent"""
    st.header("🌟 Agent Overview")
    
    cols = st.columns(2)
    
    for i, (agent_name, agent_data) in enumerate(playground.agents.items()):
        with cols[i % 2]:
            st.markdown(f"""
            <div class="agent-card">
                <h3>{agent_data['emoji']} {agent_name}</h3>
                <p><strong>{agent_data['description']}</strong></p>
                <h5>Key Capabilities:</h5>
                <ul>
            """, unsafe_allow_html=True)
            
            for capability in agent_data['capabilities']:
                st.markdown(f"<li>{capability}</li>", unsafe_allow_html=True)
            
            st.markdown(f"""
                </ul>
                <h5>Primary Use Cases:</h5>
                <ul>
            """, unsafe_allow_html=True)
            
            for use_case in agent_data['use_cases']:
                st.markdown(f"<li>{use_case}</li>", unsafe_allow_html=True)
            
            st.markdown("</ul></div>", unsafe_allow_html=True)

def create_interactive_demo(playground: WebAgentPlayground):
    """Create the main interactive demo interface"""
    st.header("🎮 Interactive Demo")
    
    # Demo configuration
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("🎯 Choose Your Challenge")
        
        # Scenario selection
        scenario_options = list(playground.demo_scenarios.keys()) + ["Custom Query"]
        selected_scenario = st.selectbox(
            "Select a demo scenario:",
            scenario_options,
            help="Choose a predefined scenario or create your own"
        )
        
        if selected_scenario == "Custom Query":
            custom_query = st.text_area(
                "Enter your custom query:",
                placeholder="What would you like the agents to help you with?",
                height=100
            )
            scenario_data = {
                "query": custom_query,
                "complexity": "Medium",
                "expected_steps": 5,
                "domains": ["General"]
            }
        else:
            scenario_data = playground.demo_scenarios[selected_scenario]
            st.info(f"**Complexity:** {scenario_data['complexity']} | **Expected Steps:** {scenario_data['expected_steps']} | **Domains:** {', '.join(scenario_data['domains'])}")
        
        # Agent selection
        selected_agents = st.multiselect(
            "Choose agents to compare:",
            list(playground.agents.keys()),
            default=list(playground.agents.keys())[:2],
            help="Select multiple agents to see how they approach the same problem differently"
        )
        
        # Run demo button
        run_demo = st.button("🚀 Run Comparison Demo", type="primary", use_container_width=True)
    
    with col2:
        st.subheader("📊 Live Metrics")
        
        # Display current scenario info
        if selected_scenario != "Custom Query":
            query = scenario_data["query"]
            st.metric("Scenario Complexity", scenario_data["complexity"])
            st.metric("Expected Steps", scenario_data["expected_steps"])
            st.metric("Domains", len(scenario_data["domains"]))
        
        # System status
        st.subheader("🔧 System Status")
        st.markdown('<span class="status-indicator status-active"></span>All Agents Ready', unsafe_allow_html=True)
        st.markdown('<span class="status-indicator status-active"></span>Demo Mode Active', unsafe_allow_html=True)
        st.markdown('<span class="status-indicator status-warning"></span>Mock Data Mode', unsafe_allow_html=True)
    
    # Run the demo
    if run_demo and selected_agents:
        if selected_scenario == "Custom Query" and not custom_query.strip():
            st.error("Please enter a custom query or select a predefined scenario.")
            return
        
        query = scenario_data["query"]
        st.success(f"🎯 Running demo for: **{query}**")
        
        # Create results containers
        results_container = st.container()
        
        with results_container:
            st.subheader("🔄 Agent Responses")
            
            # Process each selected agent
            agent_results = {}
            progress_bars = {}
            
            # Create progress bars for each agent
            for agent in selected_agents:
                st.markdown(f"### {playground.agents[agent]['emoji']} {agent}")
                progress_bars[agent] = st.progress(0)
                
            # Simulate processing
            for agent in selected_agents:
                with st.spinner(f"Processing with {agent}..."):
                    # Simulate thinking process
                    result = playground.simulate_agent_response(agent, query, scenario_data)
                    thinking_steps = result['response_data']['thinking_process']
                    
                    # Show thinking process
                    thinking_container = st.expander(f"🤔 {agent} Thinking Process", expanded=False)
                    with thinking_container:
                        for i, step in enumerate(thinking_steps):
                            progress_bars[agent].progress((i + 1) / len(thinking_steps))
                            st.write(f"**Step {i+1}:** {step}")
                            time.sleep(0.3)  # Simulate processing time
                    
                    progress_bars[agent].progress(1.0)
                    agent_results[agent] = result
                
                # Display final response
                st.markdown(f"""
                <div class="demo-output">
                    <h4>{playground.agents[agent]['emoji']} {agent} Response:</h4>
                    {result['response_data']['final_answer']}
                </div>
                """, unsafe_allow_html=True)
                
                # Show metrics
                metrics = result['response_data']['metrics']
                metric_cols = st.columns(len(metrics))
                for i, (metric_name, metric_value) in enumerate(metrics.items()):
                    with metric_cols[i]:
                        if isinstance(metric_value, float):
                            display_value = f"{metric_value:.2f}"
                        else:
                            display_value = str(metric_value)
                        st.metric(metric_name.replace('_', ' ').title(), display_value)
                
                st.markdown("---")
            
            # Comparison summary
            if len(agent_results) > 1:
                st.subheader("📊 Comparison Summary")
                
                comparison_data = []
                for agent, result in agent_results.items():
                    comparison_data.append({
                        'Agent': f"{playground.agents[agent]['emoji']} {agent}",
                        'Processing Time': f"{result['processing_time']:.1f}s",
                        'Approach': playground.agents[agent]['description'],
                        'Key Strength': playground.agents[agent]['capabilities'][0]
                    })
                
                df = pd.DataFrame(comparison_data)
                st.dataframe(df, use_container_width=True)

def create_performance_analytics(playground: WebAgentPlayground):
    """Create performance analytics section"""
    st.header("📈 Performance Analytics")
    
    # Agent comparison chart
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("🎯 Agent Capability Comparison")
        fig = playground.create_agent_comparison_chart()
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("🏆 Performance Rankings")
        
        # Calculate average performance
        avg_performances = {}
        for agent, data in playground.agents.items():
            perf = data['performance']
            avg_performances[agent] = sum(perf.values()) / len(perf.values())
        
        # Sort by performance
        sorted_agents = sorted(avg_performances.items(), key=lambda x: x[1], reverse=True)
        
        for i, (agent, avg_perf) in enumerate(sorted_agents):
            emoji = playground.agents[agent]['emoji']
            st.markdown(f"**{i+1}. {emoji} {agent}** - {avg_perf:.1f}%")
    
    # Usage scenarios heatmap
    st.subheader("🎯 Use Case Suitability Matrix")
    
    use_cases = ["Research", "Navigation", "Analysis", "Synthesis", "Exploration"]
    suitability_data = []
    
    for agent in playground.agents.keys():
        row = [random.randint(70, 95) for _ in use_cases]
        suitability_data.append(row)
    
    fig_heatmap = px.imshow(
        suitability_data,
        x=use_cases,
        y=list(playground.agents.keys()),
        color_continuous_scale="Blues",
        title="Agent Suitability for Different Use Cases (%)"
    )
    
    st.plotly_chart(fig_heatmap, use_container_width=True)

def create_educational_content():
    """Create educational content about WebAgent"""
    st.header("📚 Learn More About WebAgent")
    
    tabs = st.tabs(["🔬 Research Papers", "🛠️ Technical Details", "🎯 Best Practices", "🚀 Getting Started"])
    
    with tabs[0]:
        st.subheader("📑 Research Papers")
        
        papers = [
            {
                "title": "WebDancer: Towards Autonomous Information Seeking Agency",
                "authors": "Wu et al.",
                "year": "2025",
                "description": "Introduces WebDancer, a native agentic search reasoning model using ReAct framework.",
                "link": "https://arxiv.org/abs/2505.22648"
            },
            {
                "title": "WebSailor: Navigating Super-human Reasoning for Web Agent",
                "authors": "Li et al.",
                "year": "2025", 
                "description": "Presents WebSailor with super-human reasoning capabilities for complex web navigation.",
                "link": "https://arxiv.org/abs/2507.02592"
            },
            {
                "title": "WebWalker: Benchmarking LLMs in Web Traversal",
                "authors": "Wu et al.",
                "year": "2025",
                "description": "Comprehensive benchmarking framework for LLMs in web traversal tasks.",
                "link": "https://arxiv.org/abs/2501.07572"
            }
        ]
        
        for paper in papers:
            st.markdown(f"""
            **{paper['title']}**  
            *{paper['authors']} ({paper['year']})*  
            {paper['description']}  
            [📄 Read Paper]({paper['link']})
            """)
            st.markdown("---")
    
    with tabs[1]:
        st.subheader("⚙️ Technical Architecture")
        
        st.markdown("""
        ### WebAgent Framework Components
        
        **1. WebDancer** 🕺
        - **Architecture**: ReAct-based reasoning framework
        - **Training**: Four-stage paradigm (data construction, trajectory sampling, SFT, RL)
        - **Key Innovation**: Autonomous information seeking with minimal human intervention
        
        **2. WebSailor** ⛵
        - **Architecture**: Advanced reasoning with uncertainty handling
        - **Training**: DUPO (Duplicating Sampling Policy Optimization)
        - **Key Innovation**: Super-human reasoning for complex information landscapes
        
        **3. WebWalker** 🚶
        - **Architecture**: Multi-agent framework for web traversal
        - **Features**: Memory management, systematic navigation, content extraction
        - **Key Innovation**: Benchmarking framework for web traversal evaluation
        
        **4. WebShaper** 🎨
        - **Architecture**: Formalization-driven data synthesis
        - **Process**: Question generation, validation, information mapping
        - **Key Innovation**: Systematic data synthesis for information-seeking tasks
        """)
    
    with tabs[2]:
        st.subheader("💡 Best Practices")
        
        st.markdown("""
        ### Query Optimization
        
        **✅ Do:**
        - Use specific, actionable queries
        - Provide context when necessary
        - Break complex questions into parts
        - Specify information sources if relevant
        
        **❌ Avoid:**
        - Overly broad or vague questions
        - Ambiguous terminology
        - Contradictory requirements
        - Unrealistic expectations
        
        ### Agent Selection Guide
        
        **Choose WebDancer for:**
        - General research tasks
        - Autonomous information discovery
        - Multi-step reasoning requirements
        
        **Choose WebSailor for:**
        - Complex, uncertain problems
        - Multi-source information synthesis
        - High-accuracy requirements
        
        **Choose WebWalker for:**
        - Systematic website exploration
        - Structured data extraction
        - Benchmark evaluation
        
        **Choose WebShaper for:**
        - Dataset creation
        - Question formalization
        - Information structuring
        """)
    
    with tabs[3]:
        st.subheader("🚀 Getting Started")
        
        st.markdown("""
        ### Quick Setup Guide
        
        **1. Environment Setup**
        ```bash
        conda create -n webagent python=3.12
        conda activate webagent
        pip install -r requirements.txt
        ```
        
        **2. API Configuration**
        ```bash
        export OPENAI_API_KEY="your-openai-key"
        export DASHSCOPE_API_KEY="your-dashscope-key"
        export GOOGLE_SEARCH_KEY="your-google-search-key"
        export JINA_API_KEY="your-jina-key"
        ```
        
        **3. Run Demos**
        ```bash
        # WebWalker demo
        cd WebWalker/src && streamlit run app.py
        
        # WebDancer demo  
        cd WebDancer && python demos/assistant_qwq_chat.py
        
        # Unified demo
        streamlit run unified_demo.py
        ```
        
        **4. Integration Examples**
        ```python
        from WebDancer.demos.agents import SearchAgent
        from WebWalker.src.agent import WebWalker
        
        # Initialize agents
        dancer = SearchAgent(llm=llm_config, function_list=['search', 'visit'])
        walker = WebWalker(llm=llm_config, function_list=['visit_page'])
        
        # Run queries
        dancer_result = dancer.run(messages=[{'role': 'user', 'content': query}])
        walker_result = walker.run(messages=[{'role': 'user', 'content': query}])
        ```
        
        ### Troubleshooting
        
        **Common Issues:**
        - **API Key Errors**: Ensure all required API keys are set
        - **Import Errors**: Check Python environment and dependencies
        - **Performance Issues**: Monitor API rate limits and timeouts
        - **Content Extraction**: Verify website accessibility and structure
        """)

def main():
    """Main application function"""
    # Initialize playground
    playground = WebAgentPlayground()
    
    # Create main header
    create_main_header()
    
    # Navigation menu
    menu_options = ["🎮 Interactive Demo", "🌟 Agent Overview", "📈 Performance Analytics", "📚 Educational Content"]
    selected_tab = st.selectbox("Choose a section:", menu_options, label_visibility="collapsed")
    
    # Route to appropriate section
    if selected_tab == "🎮 Interactive Demo":
        create_interactive_demo(playground)
    elif selected_tab == "🌟 Agent Overview":
        create_agent_overview_cards(playground)
    elif selected_tab == "📈 Performance Analytics":
        create_performance_analytics(playground)
    elif selected_tab == "📚 Educational Content":
        create_educational_content()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 2rem;">
        <p>🤖 WebAgent Interactive Playground | Built with ❤️ using Streamlit</p>
        <p>For more information, visit the <a href="https://github.com/Alibaba-NLP/WebAgent">WebAgent GitHub Repository</a></p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()