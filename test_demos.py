"""
Test script to validate WebAgent demo functionality
"""

import sys
import traceback
from pathlib import Path

def test_imports():
    """Test that all required modules can be imported"""
    print("🧪 Testing imports...")
    
    # Test basic imports
    try:
        import streamlit as st
        print(f"✅ Streamlit {st.__version__}")
    except ImportError as e:
        print(f"❌ Streamlit import failed: {e}")
        return False
    
    try:
        import pandas as pd
        print(f"✅ Pandas {pd.__version__}")
    except ImportError as e:
        print(f"❌ Pandas import failed: {e}")
        return False
    
    try:
        import plotly
        print(f"✅ Plotly {plotly.__version__}")
    except ImportError as e:
        print(f"❌ Plotly import failed: {e}")
        return False
    
    return True

def test_demo_files():
    """Test that demo files exist and are valid Python"""
    print("\n📁 Testing demo files...")
    
    demo_files = [
        "interactive_playground.py",
        "unified_demo.py", 
        "enhanced_webwalker_demo.py",
        "launch_demo.py"
    ]
    
    root_dir = Path(__file__).parent
    
    for demo_file in demo_files:
        file_path = root_dir / demo_file
        
        if not file_path.exists():
            print(f"❌ {demo_file} not found")
            return False
        
        try:
            # Try to compile the file
            with open(file_path, 'r') as f:
                code = f.read()
            compile(code, file_path, 'exec')
            print(f"✅ {demo_file} is valid Python")
        except SyntaxError as e:
            print(f"❌ {demo_file} has syntax error: {e}")
            return False
        except Exception as e:
            print(f"⚠️  {demo_file} compile warning: {e}")
    
    return True

def test_playground_components():
    """Test WebAgent playground components"""
    print("\n🎮 Testing playground components...")
    
    try:
        # Import the playground class without running Streamlit
        sys.path.append(str(Path(__file__).parent))
        
        # Test the WebAgentPlayground class
        from interactive_playground import WebAgentPlayground
        
        playground = WebAgentPlayground()
        
        # Test agent data
        assert len(playground.agents) == 4
        print(f"✅ {len(playground.agents)} agents loaded")
        
        # Test demo scenarios
        assert len(playground.demo_scenarios) > 0
        print(f"✅ {len(playground.demo_scenarios)} demo scenarios loaded")
        
        # Test chart creation (without displaying)
        chart = playground.create_agent_comparison_chart()
        assert chart is not None
        print("✅ Performance chart generation works")
        
        # Test response simulation
        test_query = "What is artificial intelligence?"
        test_scenario = {
            "complexity": "Medium",
            "expected_steps": 5,
            "domains": ["Technology", "AI"]
        }
        
        response = playground.simulate_agent_response("WebDancer", test_query, test_scenario)
        assert 'processing_time' in response
        assert 'response_data' in response
        print("✅ Response simulation works")
        
        return True
        
    except Exception as e:
        print(f"❌ Playground test failed: {e}")
        traceback.print_exc()
        return False

def test_launcher():
    """Test the demo launcher"""
    print("\n🚀 Testing launcher...")
    
    try:
        from launch_demo import WebAgentLauncher
        
        launcher = WebAgentLauncher()
        
        # Test demo listing
        assert len(launcher.demos) > 0
        print(f"✅ {len(launcher.demos)} demos configured in launcher")
        
        # Test dependency checking (should work without actual imports)
        # We'll just check the method exists and is callable
        assert hasattr(launcher, 'check_dependencies')
        assert callable(launcher.check_dependencies)
        print("✅ Dependency checking method available")
        
        return True
        
    except Exception as e:
        print(f"❌ Launcher test failed: {e}")
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("🔬 WebAgent Demo Validation Tests")
    print("=" * 40)
    
    tests = [
        ("Imports", test_imports),
        ("Demo Files", test_demo_files), 
        ("Playground Components", test_playground_components),
        ("Launcher", test_launcher)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🧪 Running {test_name} test...")
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} test PASSED")
            else:
                print(f"❌ {test_name} test FAILED")
        except Exception as e:
            print(f"❌ {test_name} test ERROR: {e}")
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Demos are ready to use.")
        print("\n🚀 You can now run:")
        print("   python launch_demo.py playground")
        return True
    else:
        print("⚠️  Some tests failed. Check the output above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)