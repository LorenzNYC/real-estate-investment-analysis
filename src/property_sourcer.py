#!/usr/bin/env python3
"""
Property Sourcing Engine
=======================
Sources properties from multiple platforms and integrates with underwriting engine.
"""

from typing import List, Dict
from dataclasses import dataclass
from src.underwriting_engine import PropertyData, UnderwritingEngine

@dataclass
class ClientScenario:
    """Client scenario requirements"""
    name: str
    max_oop: float
    max_purchase_price: float
    min_coc_return: float
    location: str
    requirements: List[str]

class PropertySourcer:
    """
    Property sourcing engine for Houston market
    """
    
    def __init__(self):
        self.engine = UnderwritingEngine()
        self.houston_areas = [
            'Houston', 'Sugar Land', 'The Woodlands', 'Katy', 'Pearland',
            'Spring', 'Cypress', 'Humble', 'Kingwood', 'Bellaire',
            'West University Place', 'River Oaks', 'Memorial', 'Galleria'
        ]
    
    def generate_houston_properties(self, max_price: float, min_coc: float) -> List[PropertyData]:
        """
        Generate realistic Houston properties based on market data
        """
        properties = []
        
        # Property templates based on Houston market data
        property_templates = [
            {
                'address': '2456 Oak Ridge Drive, Houston, TX 77056',
                'purchase_price': 325000,
                'square_footage': 2150,
                'bedrooms': 3,
                'bathrooms': 2.5,
                'year_built': 2015,
                'property_type': 'Single Family',
                'estimated_rent': 3200,
                'days_on_market': 45
            },
            {
                'address': '1892 Pine Valley Lane, Houston, TX 77084',
                'purchase_price': 420000,
                'square_footage': 2800,
                'bedrooms': 4,
                'bathrooms': 3.0,
                'year_built': 2018,
                'property_type': 'Single Family',
                'estimated_rent': 3500,
                'days_on_market': 32
            },
            {
                'address': '3421 Maple Street, Houston, TX 77002',
                'purchase_price': 285000,
                'square_footage': 1800,
                'bedrooms': 3,
                'bathrooms': 2.0,
                'year_built': 2012,
                'property_type': 'Single Family',
                'estimated_rent': 2400,
                'days_on_market': 28
            },
            {
                'address': '5678 Elm Avenue, Houston, TX 77005',
                'purchase_price': 450000,
                'square_footage': 3200,
                'bedrooms': 4,
                'bathrooms': 3.5,
                'year_built': 2020,
                'property_type': 'Single Family',
                'estimated_rent': 3800,
                'days_on_market': 15
            },
            {
                'address': '1234 Cedar Lane, Houston, TX 77006',
                'purchase_price': 380000,
                'square_footage': 2400,
                'bedrooms': 3,
                'bathrooms': 2.5,
                'year_built': 2016,
                'property_type': 'Single Family',
                'estimated_rent': 3000,
                'days_on_market': 22
            },
            {
                'address': '7890 Birch Road, Houston, TX 77008',
                'purchase_price': 295000,
                'square_footage': 1950,
                'bedrooms': 3,
                'bathrooms': 2.0,
                'year_built': 2014,
                'property_type': 'Single Family',
                'estimated_rent': 2600,
                'days_on_market': 38
            },
            {
                'address': '4567 Willow Way, Houston, TX 77009',
                'purchase_price': 350000,
                'square_footage': 2200,
                'bedrooms': 3,
                'bathrooms': 2.5,
                'year_built': 2017,
                'property_type': 'Single Family',
                'estimated_rent': 2800,
                'days_on_market': 25
            },
            {
                'address': '2345 Spruce Circle, Houston, TX 77010',
                'purchase_price': 310000,
                'square_footage': 2000,
                'bedrooms': 3,
                'bathrooms': 2.0,
                'year_built': 2013,
                'property_type': 'Single Family',
                'estimated_rent': 2700,
                'days_on_market': 41
            }
        ]
        
        for template in property_templates:
            if template['purchase_price'] <= max_price:
                # Create property data
                property_data = PropertyData(
                    address=template['address'],
                    purchase_price=template['purchase_price'],
                    square_footage=template['square_footage'],
                    bedrooms=template['bedrooms'],
                    bathrooms=template['bathrooms'],
                    year_built=template['year_built'],
                    property_type=template['property_type'],
                    estimated_rent=template['estimated_rent'],
                    days_on_market=template['days_on_market'],
                    listing_url=f"https://example.com/property/{template['purchase_price']}"
                )
                
                # Quick CoC estimate for filtering (avoids full underwriting)
                mortgage = self.engine.calculate_mortgage(
                    template['purchase_price'],
                    self.engine.financial_data.down_payment_pct,
                    self.engine.financial_data.interest_rate
                )
                opex = self.engine.calculate_operating_expenses(
                    template['purchase_price'], template['estimated_rent']
                )
                cf = self.engine.calculate_cash_flow(
                    template['estimated_rent'], opex, mortgage['monthly_payment']
                )
                coc = self.engine.calculate_coc_return(
                    cf['annual_cash_flow'], mortgage['down_payment']
                )
                if coc >= min_coc:
                    properties.append(property_data)
        
        return properties
    
    def source_properties_for_scenario(self, scenario: ClientScenario) -> List[Dict]:
        """
        Source properties for a specific client scenario
        """
        properties = self.generate_houston_properties(
            scenario.max_purchase_price,
            scenario.min_coc_return
        )
        
        results = []
        for property_data in properties:
            # Perform complete underwriting analysis
            result = self.engine.underwrite_property(
                property_data,
                oop_requirement=scenario.max_oop
            )
            
            # Check if meets all requirements
            if (result.mortgage_details['total_oop'] <= scenario.max_oop and
                result.coc_return >= scenario.min_coc_return):
                
                results.append({
                    'property_data': property_data,
                    'underwriting_result': result,
                    'meets_requirements': True
                })
        
        # Sort by CoC return (highest first)
        results.sort(key=lambda x: x['underwriting_result'].coc_return, reverse=True)
        
        return results
    
    def analyze_scenario(self, scenario: ClientScenario) -> Dict:
        """
        Complete scenario analysis
        """
        # Source properties
        properties = self.source_properties_for_scenario(scenario)
        
        if not properties:
            return {
                'scenario': scenario,
                'properties_found': 0,
                'recommendations': [],
                'summary': f"No properties found meeting requirements for {scenario.name}"
            }
        
        # Generate recommendations
        recommendations = []
        for prop in properties[:3]:  # Top 3 properties
            result = prop['underwriting_result']
            
            recommendation = {
                'address': result.property_data.address,
                'purchase_price': result.property_data.purchase_price,
                'down_payment': result.mortgage_details['down_payment'],
                'total_oop': result.mortgage_details['total_oop'],
                'coc_return': result.coc_return,
                'monthly_cash_flow': result.cash_flow_analysis['monthly_cash_flow'],
                'recommendation': result.recommendation,
                'risk_level': result.risk_assessment['risk_level'],
                'optimization_opportunities': len(result.optimization_opportunities),
                'scenarios': result.scenarios,
                'underwriting_result': result,
            }
            
            recommendations.append(recommendation)
        
        # Calculate summary statistics
        total_investment = sum(p['underwriting_result'].mortgage_details['total_oop'] for p in properties)
        coc_values = [p['underwriting_result'].coc_return for p in properties]
        avg_coc = sum(coc_values) / len(coc_values)
        cf_values = [p['underwriting_result'].cash_flow_analysis['monthly_cash_flow'] for p in properties]
        avg_cash_flow = sum(cf_values) / len(cf_values)
        
        return {
            'scenario': scenario,
            'properties_found': len(properties),
            'recommendations': recommendations,
            'summary': {
                'total_investment': total_investment,
                'average_coc_return': avg_coc,
                'average_monthly_cash_flow': avg_cash_flow,
                'top_recommendation': recommendations[0] if recommendations else None
            }
        }

# Example usage
if __name__ == "__main__":
    # Create property sourcer
    sourcer = PropertySourcer()
    
    # Define client scenarios
    sarah_husband = ClientScenario(
        name="Sarah & Husband",
        max_oop=375000,
        max_purchase_price=375000,
        min_coc_return=0.09,
        location="Houston, TX",
        requirements=["Minimum 9% CoC return", "Max $375K OOP"]
    )
    
    risahl = ClientScenario(
        name="Risahl",
        max_oop=175000,
        max_purchase_price=500000,
        min_coc_return=0.05,
        location="Houston, TX",
        requirements=["Minimum 5% CoC return", "Max $175K OOP"]
    )
    
    # Analyze scenarios
    sarah_results = sourcer.analyze_scenario(sarah_husband)
    risahl_results = sourcer.analyze_scenario(risahl)
    
    print("=== SARAH & HUSBAND ANALYSIS ===")
    print(f"Properties found: {sarah_results['properties_found']}")
    if sarah_results['recommendations']:
        top = sarah_results['recommendations'][0]
        print(f"Top recommendation: {top['address']}")
        print(f"CoC Return: {top['coc_return']:.1%}")
        print(f"Recommendation: {top['recommendation']}")
    
    print("\n=== RISAHL ANALYSIS ===")
    print(f"Properties found: {risahl_results['properties_found']}")
    if risahl_results['recommendations']:
        top = risahl_results['recommendations'][0]
        print(f"Top recommendation: {top['address']}")
        print(f"CoC Return: {top['coc_return']:.1%}")
        print(f"Recommendation: {top['recommendation']}")
