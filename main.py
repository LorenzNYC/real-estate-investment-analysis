#!/usr/bin/env python3
"""
Real Estate Underwriting Application
===================================
Main application that runs the complete automated underwriting system.
"""

import argparse

from src.underwriting_engine import UnderwritingEngine, PropertyData
from src.property_sourcer import PropertySourcer, ClientScenario

def run_analysis():
    """Run complete analysis for both client scenarios"""
    print("🚀 Starting Real Estate Underwriting Analysis...")
    print("=" * 60)
    
    # Initialize engines
    underwriting_engine = UnderwritingEngine()
    property_sourcer = PropertySourcer()
    
    # Define client scenarios
    sarah_husband = ClientScenario(
        name="Sarah & Husband",
        max_oop=375000,
        max_purchase_price=375000,
        min_coc_return=0.08,
        location="Houston, TX",
        requirements=["Minimum 8% CoC return", "Max $375K OOP"]
    )

    risahl = ClientScenario(
        name="Risahl",
        max_oop=175000,
        max_purchase_price=500000,
        min_coc_return=0.03,
        location="Houston, TX",
        requirements=["Minimum 3% CoC return", "Max $175K OOP"]
    )
    
    # Analyze scenarios
    print("\n📊 Analyzing Sarah & Husband Scenario...")
    sarah_results = property_sourcer.analyze_scenario(sarah_husband)
    
    print("\n📊 Analyzing Risahl Scenario...")
    risahl_results = property_sourcer.analyze_scenario(risahl)
    
    # Display results
    print("\n" + "=" * 60)
    print("📋 ANALYSIS RESULTS")
    print("=" * 60)
    
    # Sarah & Husband Results
    print(f"\n🏠 SARAH & HUSBAND SCENARIO")
    print(f"Properties Found: {sarah_results['properties_found']}")
    print(f"Requirements: {sarah_husband.requirements}")
    
    if sarah_results['recommendations']:
        print("\nTop Recommendations:")
        for i, rec in enumerate(sarah_results['recommendations'][:3]):
            print(f"\n{i+1}. {rec['address']}")
            print(f"   Purchase Price: ${rec['purchase_price']:,.0f}")
            print(f"   Down Payment: ${rec['down_payment']:,.0f}")
            print(f"   Total OOP: ${rec['total_oop']:,.0f}")
            print(f"   CoC Return: {rec['coc_return']:.1%}")
            print(f"   Monthly Cash Flow: ${rec['monthly_cash_flow']:,.0f}")
            print(f"   Risk Level: {rec['risk_level']}")
            print(f"   Recommendation: {rec['recommendation']}")
    else:
        print("❌ No properties found meeting requirements")
    
    # Risahl Results
    print(f"\n🏠 RISAHL SCENARIO")
    print(f"Properties Found: {risahl_results['properties_found']}")
    print(f"Requirements: {risahl.requirements}")
    
    if risahl_results['recommendations']:
        print("\nTop Recommendations:")
        for i, rec in enumerate(risahl_results['recommendations'][:3]):
            print(f"\n{i+1}. {rec['address']}")
            print(f"   Purchase Price: ${rec['purchase_price']:,.0f}")
            print(f"   Down Payment: ${rec['down_payment']:,.0f}")
            print(f"   Total OOP: ${rec['total_oop']:,.0f}")
            print(f"   CoC Return: {rec['coc_return']:.1%}")
            print(f"   Monthly Cash Flow: ${rec['monthly_cash_flow']:,.0f}")
            print(f"   Risk Level: {rec['risk_level']}")
            print(f"   Recommendation: {rec['recommendation']}")
    else:
        print("❌ No properties found meeting requirements")
    
    # Summary
    print("\n" + "=" * 60)
    print("📈 SUMMARY")
    print("=" * 60)
    
    total_properties = sarah_results['properties_found'] + risahl_results['properties_found']
    print(f"Total Properties Analyzed: {total_properties}")
    
    if sarah_results['properties_found'] > 0:
        print(f"Sarah & Husband - Properties Meeting Requirements: {sarah_results['properties_found']}")
    
    if risahl_results['properties_found'] > 0:
        print(f"Risahl - Properties Meeting Requirements: {risahl_results['properties_found']}")
    
    print("\n✅ Analysis Complete!")
    print("\nTo view detailed dashboard, run: python3 src/automated_dashboard.py")

def run_dashboard():
    """Run the automated dashboard"""
    print("🌐 Starting Automated Dashboard...")
    print("Dashboard will be available at: http://127.0.0.1:8050")
    print("Press Ctrl+C to stop the dashboard")
    
    # Import and run dashboard
    from src.automated_dashboard import app
    app.run_server(debug=True, host='0.0.0.0', port=8050)

def run_test():
    """Run test analysis on a single property"""
    print("🧪 Running Test Analysis...")
    
    # Create test property
    test_property = PropertyData(
        address="2456 Oak Ridge Drive, Houston, TX 77056",
        purchase_price=325000,
        square_footage=2150,
        bedrooms=3,
        bathrooms=2.5,
        year_built=2015,
        property_type="Single Family",
        estimated_rent=4800,
        days_on_market=45,
        listing_url="https://example.com"
    )
    
    # Run underwriting analysis
    engine = UnderwritingEngine()
    result = engine.underwrite_property(test_property, oop_requirement=375000)
    
    # Display results
    print(f"\n🏠 Test Property: {result.property_data.address}")
    print(f"Purchase Price: ${result.property_data.purchase_price:,.0f}")
    print(f"Down Payment: ${result.mortgage_details['down_payment']:,.0f}")
    print(f"Total OOP: ${result.mortgage_details['total_oop']:,.0f}")
    print(f"Monthly Payment: ${result.mortgage_details['monthly_payment']:,.0f}")
    print(f"Monthly Cash Flow: ${result.cash_flow_analysis['monthly_cash_flow']:,.0f}")
    print(f"CoC Return: {result.coc_return:.1%}")
    print(f"Recommendation: {result.recommendation}")
    print(f"Risk Level: {result.risk_assessment['risk_level']}")
    
    print(f"\nOptimization Opportunities: {len(result.optimization_opportunities)}")
    for opp in result.optimization_opportunities:
        print(f"- {opp['title']}: ROI {opp['roi']:.1%}")
    
    print("\n✅ Test Complete!")

def main():
    """Main application entry point"""
    parser = argparse.ArgumentParser(description="Real Estate Underwriting Application")
    parser.add_argument(
        '--mode',
        choices=['analysis', 'dashboard', 'test'],
        default='analysis',
        help='Application mode (default: analysis)'
    )
    
    args = parser.parse_args()
    
    if args.mode == 'analysis':
        run_analysis()
    elif args.mode == 'dashboard':
        run_dashboard()
    elif args.mode == 'test':
        run_test()
    else:
        print("Invalid mode. Use --help for options.")

if __name__ == "__main__":
    main()
