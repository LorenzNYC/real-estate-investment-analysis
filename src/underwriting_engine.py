#!/usr/bin/env python3
"""
Real Estate Underwriting Engine
===============================
Implements exact Google Sheets formulas and calculation methodology
for comprehensive property underwriting analysis.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional
from datetime import datetime

@dataclass
class PropertyData:
    """Property information data model"""
    address: str
    purchase_price: float
    square_footage: int
    bedrooms: int
    bathrooms: float
    year_built: int
    property_type: str
    estimated_rent: float
    days_on_market: int
    listing_url: str

@dataclass
class FinancialData:
    """Financial constants and assumptions from Google Sheets"""
    down_payment_pct: float = 0.20
    interest_rate: float = 0.065
    loan_term: int = 30
    property_tax_rate: float = 0.025
    insurance_rate: float = 0.008
    maintenance_rate: float = 0.015
    management_rate: float = 0.08
    vacancy_rate: float = 0.05
    closing_costs_pct: float = 0.03
    annual_appreciation_rate: float = 0.035

@dataclass
class OperatingExpenses:
    """Monthly operating expenses from Google Sheets"""
    internet: float = 100.0
    water: float = 60.0
    electricity: float = 300.0
    natural_gas: float = 0.0
    pest_control: float = 50.0
    pool_maintenance: float = 150.0
    property_tax: float = 0.0  # Calculated
    insurance: float = 0.0      # Calculated
    maintenance: float = 0.0    # Calculated
    management: float = 0.0     # Calculated
    vacancy: float = 0.0        # Calculated

@dataclass
class UnderwritingResult:
    """Complete underwriting analysis result"""
    property_data: PropertyData
    financial_data: FinancialData
    mortgage_details: Dict
    cash_flow_analysis: Dict
    coc_return: float
    roi: float
    scenarios: Dict
    optimization_opportunities: List[Dict]
    risk_assessment: Dict
    recommendation: str

class UnderwritingEngine:
    """
    Automated underwriting engine implementing exact Google Sheets formulas
    """
    
    def __init__(self):
        self.financial_data = FinancialData()
        self.opex = OperatingExpenses()
    
    def validate_inputs(self, purchase_price: float, down_payment_pct: float, interest_rate: float) -> None:
        """
        Validate inputs using Google Sheets standards
        """
        if purchase_price <= 0:
            raise ValueError("Purchase price must be positive")
        if down_payment_pct < 0.20:
            raise ValueError("Down payment must be at least 20%")
        if interest_rate <= 0:
            raise ValueError("Interest rate must be positive")
        if interest_rate > 0.20:
            raise ValueError("Interest rate seems unrealistic")
    
    def calculate_mortgage(self, purchase_price: float, down_payment_pct: float, interest_rate: float) -> Dict:
        """
        Calculate mortgage details using exact Google Sheets formulas
        Formula: =PMT(Interest_Rate/12, Loan_Term*12, -Loan_Amount)
        """
        self.validate_inputs(purchase_price, down_payment_pct, interest_rate)
        
        # Down Payment: =Purchase_Price * Down_Payment_Percentage
        down_payment = purchase_price * down_payment_pct
        
        # Loan Amount: =Purchase_Price - Down_Payment
        loan_amount = purchase_price - down_payment
        
        # Monthly Rate: =Interest_Rate/12
        monthly_rate = interest_rate / 12
        
        # Number of Payments: =Loan_Term*12
        num_payments = self.financial_data.loan_term * 12
        
        # Monthly Payment: =PMT(Interest_Rate/12, Loan_Term*12, -Loan_Amount)
        # Using the PMT formula: P = L[c(1 + c)^n]/[(1 + c)^n - 1]
        if monthly_rate == 0:
            monthly_payment = loan_amount / num_payments
        else:
            monthly_payment = (loan_amount * monthly_rate * (1 + monthly_rate)**num_payments) / ((1 + monthly_rate)**num_payments - 1)
        
        # Closing Costs: =Purchase_Price * Closing_Costs_Percentage
        closing_costs = purchase_price * self.financial_data.closing_costs_pct
        
        return {
            'down_payment': down_payment,
            'loan_amount': loan_amount,
            'monthly_payment': monthly_payment,
            'closing_costs': closing_costs,
            'total_oop': down_payment + closing_costs,
            'monthly_rate': monthly_rate,
            'num_payments': num_payments
        }
    
    def calculate_operating_expenses(self, purchase_price: float, estimated_rent: float) -> OperatingExpenses:
        """
        Calculate operating expenses using Google Sheets methodology
        """
        opex = OperatingExpenses()
        
        # Property Tax: =Purchase_Price * Property_Tax_Rate / 12
        opex.property_tax = (purchase_price * self.financial_data.property_tax_rate) / 12
        
        # Insurance: =Purchase_Price * Insurance_Rate / 12
        opex.insurance = (purchase_price * self.financial_data.insurance_rate) / 12
        
        # Maintenance: =Purchase_Price * Maintenance_Rate / 12
        opex.maintenance = (purchase_price * self.financial_data.maintenance_rate) / 12
        
        # Management: =Estimated_Rent * Management_Rate
        opex.management = estimated_rent * self.financial_data.management_rate
        
        # Vacancy: =Estimated_Rent * Vacancy_Rate
        opex.vacancy = estimated_rent * self.financial_data.vacancy_rate
        
        # Adjust for more realistic expenses based on Google Sheets
        # From the Google Sheets: Internet $100, Water $60, Electricity $300, etc.
        opex.internet = 100
        opex.water = 60
        opex.electricity = 300
        opex.natural_gas = 0
        opex.pest_control = 50
        opex.pool_maintenance = 150
        
        return opex
    
    def calculate_cash_flow(self, estimated_rent: float, opex: OperatingExpenses, monthly_mortgage: float) -> Dict:
        """
        Calculate cash flow using exact Google Sheets formula
        Formula: =Monthly_Rent - Monthly_Expenses - Monthly_Mortgage_Payment
        """
        # Total Monthly Expenses (including vacancy allowance)
        total_monthly_expenses = (
            opex.internet + opex.water + opex.electricity + opex.natural_gas +
            opex.pest_control + opex.pool_maintenance + opex.property_tax +
            opex.insurance + opex.maintenance + opex.management + opex.vacancy
        )
        
        # Net Operating Income: =Monthly_Rent - Monthly_Expenses
        net_operating_income = estimated_rent - total_monthly_expenses
        
        # Monthly Cash Flow: =Net_Operating_Income - Monthly_Mortgage_Payment
        monthly_cash_flow = net_operating_income - monthly_mortgage
        
        # Annual Cash Flow: =Monthly_Cash_Flow * 12
        annual_cash_flow = monthly_cash_flow * 12
        
        return {
            'monthly_rent': estimated_rent,
            'monthly_expenses': total_monthly_expenses,
            'monthly_mortgage': monthly_mortgage,
            'net_operating_income': net_operating_income,
            'monthly_cash_flow': monthly_cash_flow,
            'annual_cash_flow': annual_cash_flow,
            'expense_breakdown': {
                'utilities': opex.internet + opex.water + opex.electricity + opex.natural_gas,
                'maintenance': opex.pest_control + opex.pool_maintenance + opex.maintenance,
                'taxes_insurance': opex.property_tax + opex.insurance,
                'management': opex.management,
                'vacancy': opex.vacancy
            }
        }
    
    def calculate_coc_return(self, annual_cash_flow: float, down_payment: float) -> float:
        """
        Calculate cash-on-cash return using exact Google Sheets formula
        Formula: =Annual_Cash_Flow / Down_Payment
        """
        if down_payment <= 0:
            return 0.0
        return annual_cash_flow / down_payment
    
    def analyze_scenarios(self, base_rent: float, base_expenses: float, scenario_type: str) -> Dict:
        """
        Analyze scenarios using exact Google Sheets methodology
        """
        if scenario_type == 'low':
            # Low Scenario: Base rent * 0.90, Base expenses * 1.10
            adjusted_rent = base_rent * 0.90
            adjusted_expenses = base_expenses * 1.10
            vacancy_rate = 0.08
        elif scenario_type == 'mid':
            # Mid Scenario: Base rent (no adjustment), Base expenses (no adjustment)
            adjusted_rent = base_rent
            adjusted_expenses = base_expenses
            vacancy_rate = 0.05
        elif scenario_type == 'high':
            # High Scenario: Base rent * 1.10, Base expenses * 0.90
            adjusted_rent = base_rent * 1.10
            adjusted_expenses = base_expenses * 0.90
            vacancy_rate = 0.03
        else:
            raise ValueError(f"Invalid scenario type: {scenario_type}")
        
        return {
            'rent': adjusted_rent,
            'expenses': adjusted_expenses,
            'vacancy_rate': vacancy_rate,
            'scenario_type': scenario_type
        }
    
    def generate_optimization_opportunities(self, property_data: PropertyData, cash_flow: Dict) -> List[Dict]:
        """
        Generate optimization opportunities with ROI calculations
        """
        opportunities = []
        
        # 1. Rental Rate Optimization
        current_rent = cash_flow['monthly_rent']
        market_rent = current_rent * 1.10  # 10% increase potential
        rent_increase = market_rent - current_rent
        
        if rent_increase > 0:
            opportunities.append({
                'category': 'Revenue',
                'title': 'Rental Rate Optimization',
                'description': f'Increase rent from ${current_rent:,.0f} to ${market_rent:,.0f}/month',
                'investment': 0,
                'annual_benefit': rent_increase * 12,
                'roi': float('inf') if rent_increase > 0 else 0,
                'implementation_time': 'Immediate',
                'priority': 'High',
                'risk_level': 'Low'
            })
        
        # 2. Property Management Optimization
        current_management = cash_flow['expense_breakdown']['management']
        if current_management > 0:
            opportunities.append({
                'category': 'Expense',
                'title': 'Self-Management',
                'description': f'Save ${current_management:,.0f}/month by self-managing',
                'investment': 0,
                'annual_benefit': current_management * 12,
                'roi': float('inf'),
                'implementation_time': 'Immediate',
                'priority': 'High',
                'risk_level': 'Medium'
            })
        
        # 3. Energy Efficiency Improvements
        energy_investment = 500
        energy_savings = 50  # $50/month savings
        opportunities.append({
            'category': 'Improvement',
            'title': 'Energy Efficiency',
            'description': 'Install smart thermostat and LED lighting',
            'investment': energy_investment,
            'annual_benefit': energy_savings * 12,
            'roi': (energy_savings * 12) / energy_investment,
            'implementation_time': '1 month',
            'priority': 'Medium',
            'risk_level': 'Low'
        })
        
        # 4. Curb Appeal Enhancement
        curb_investment = 2000
        curb_rent_increase = 100  # $100/month rent increase
        opportunities.append({
            'category': 'Improvement',
            'title': 'Curb Appeal Enhancement',
            'description': 'Landscaping and exterior improvements',
            'investment': curb_investment,
            'annual_benefit': curb_rent_increase * 12,
            'roi': (curb_rent_increase * 12) / curb_investment,
            'implementation_time': '2 months',
            'priority': 'Medium',
            'risk_level': 'Low'
        })
        
        # 5. Kitchen Updates
        kitchen_investment = 5000
        kitchen_rent_increase = 150  # $150/month rent increase
        opportunities.append({
            'category': 'Improvement',
            'title': 'Kitchen Updates',
            'description': 'Minor kitchen refresh and updates',
            'investment': kitchen_investment,
            'annual_benefit': kitchen_rent_increase * 12,
            'roi': (kitchen_rent_increase * 12) / kitchen_investment,
            'implementation_time': '3 months',
            'priority': 'Low',
            'risk_level': 'Medium'
        })
        
        return opportunities
    
    def assess_risk(self, property_data: PropertyData, cash_flow: Dict, coc_return: float) -> Dict:
        """
        Comprehensive risk assessment
        """
        risk_factors = []
        risk_score = 0
        
        # Market Risk
        if property_data.days_on_market > 90:
            risk_factors.append("High days on market")
            risk_score += 2
        elif property_data.days_on_market > 60:
            risk_factors.append("Moderate days on market")
            risk_score += 1
        
        # Cash Flow Risk
        if cash_flow['monthly_cash_flow'] < 0:
            risk_factors.append("Negative cash flow")
            risk_score += 3
        elif cash_flow['monthly_cash_flow'] < 200:
            risk_factors.append("Low cash flow")
            risk_score += 1
        
        # CoC Return Risk
        if coc_return < 0.05:
            risk_factors.append("Low CoC return")
            risk_score += 2
        elif coc_return < 0.08:
            risk_factors.append("Moderate CoC return")
            risk_score += 1
        
        # Property Age Risk
        current_year = datetime.now().year
        property_age = current_year - property_data.year_built
        if property_age > 30:
            risk_factors.append("Older property")
            risk_score += 1
        
        # Determine Risk Level
        if risk_score >= 5:
            risk_level = "High"
        elif risk_score >= 3:
            risk_level = "Medium"
        else:
            risk_level = "Low"
        
        return {
            'risk_score': risk_score,
            'risk_level': risk_level,
            'risk_factors': risk_factors,
            'mitigation_strategies': self._generate_mitigation_strategies(risk_factors)
        }
    
    def _generate_mitigation_strategies(self, risk_factors: List[str]) -> List[str]:
        """
        Generate risk mitigation strategies
        """
        strategies = []
        
        for factor in risk_factors:
            if "Negative cash flow" in factor:
                strategies.append("Implement optimization strategies to improve cash flow")
            elif "Low CoC return" in factor:
                strategies.append("Consider alternative properties or financing options")
            elif "High days on market" in factor:
                strategies.append("Conduct thorough market analysis and price optimization")
            elif "Older property" in factor:
                strategies.append("Budget for increased maintenance and potential renovations")
        
        return strategies
    
    def generate_recommendation(self, coc_return: float, risk_assessment: Dict, oop_requirement: float, total_oop: float) -> str:
        """
        Generate investment recommendation
        """
        if total_oop > oop_requirement:
            return "PASS - Exceeds OOP requirement"
        
        if risk_assessment['risk_level'] == "High":
            return "PASS - High risk level"
        
        if coc_return >= 0.09:
            return "STRONG BUY - Excellent CoC return"
        elif coc_return >= 0.07:
            return "BUY - Good CoC return"
        elif coc_return >= 0.05:
            return "HOLD - Acceptable CoC return"
        else:
            return "PASS - Insufficient CoC return"
    
    def underwrite_property(self, property_data: PropertyData, oop_requirement: float = float('inf')) -> UnderwritingResult:
        """
        Complete underwriting analysis using exact Google Sheets methodology
        """
        # Calculate mortgage details
        mortgage_details = self.calculate_mortgage(
            property_data.purchase_price,
            self.financial_data.down_payment_pct,
            self.financial_data.interest_rate
        )
        
        # Calculate operating expenses
        opex = self.calculate_operating_expenses(
            property_data.purchase_price,
            property_data.estimated_rent
        )
        
        # Calculate cash flow
        cash_flow = self.calculate_cash_flow(
            property_data.estimated_rent,
            opex,
            mortgage_details['monthly_payment']
        )
        
        # Calculate CoC return
        coc_return = self.calculate_coc_return(
            cash_flow['annual_cash_flow'],
            mortgage_details['down_payment']
        )
        
        # ROI includes CoC return plus estimated appreciation and year-1 principal paydown
        annual_appreciation = property_data.purchase_price * self.financial_data.annual_appreciation_rate
        # Year-1 principal paydown via amortization: sum of (payment - interest) each month
        balance = mortgage_details['loan_amount']
        annual_principal_paydown = 0.0
        for _ in range(12):
            month_interest = balance * mortgage_details['monthly_rate']
            month_principal = mortgage_details['monthly_payment'] - month_interest
            annual_principal_paydown += month_principal
            balance -= month_principal
        total_annual_return = cash_flow['annual_cash_flow'] + annual_appreciation + annual_principal_paydown
        roi = total_annual_return / mortgage_details['total_oop'] if mortgage_details['total_oop'] > 0 else 0.0
        
        # Analyze scenarios
        scenarios = {}
        for scenario_type in ['low', 'mid', 'high']:
            scenario_rent = self.analyze_scenarios(
                cash_flow['monthly_rent'],
                cash_flow['monthly_expenses'],
                scenario_type
            )
            
            # Recalculate cash flow for scenario
            scenario_cash_flow = self.calculate_cash_flow(
                scenario_rent['rent'],
                opex,
                mortgage_details['monthly_payment']
            )
            
            scenario_coc = self.calculate_coc_return(
                scenario_cash_flow['annual_cash_flow'],
                mortgage_details['down_payment']
            )
            
            scenarios[scenario_type] = {
                'rent': scenario_rent['rent'],
                'expenses': scenario_rent['expenses'],
                'cash_flow': scenario_cash_flow,
                'coc_return': scenario_coc
            }
        
        # Generate optimization opportunities
        optimization_opportunities = self.generate_optimization_opportunities(
            property_data,
            cash_flow
        )
        
        # Assess risk
        risk_assessment = self.assess_risk(
            property_data,
            cash_flow,
            coc_return
        )
        
        # Generate recommendation
        recommendation = self.generate_recommendation(
            coc_return,
            risk_assessment,
            oop_requirement,
            mortgage_details['total_oop']
        )
        
        return UnderwritingResult(
            property_data=property_data,
            financial_data=self.financial_data,
            mortgage_details=mortgage_details,
            cash_flow_analysis=cash_flow,
            coc_return=coc_return,
            roi=roi,
            scenarios=scenarios,
            optimization_opportunities=optimization_opportunities,
            risk_assessment=risk_assessment,
            recommendation=recommendation
        )

# Example usage
if __name__ == "__main__":
    # Create underwriting engine
    engine = UnderwritingEngine()
    
    # Example property data
    property_data = PropertyData(
        address="2456 Oak Ridge Drive, Houston, TX 77056",
        purchase_price=325000,
        square_footage=2150,
        bedrooms=3,
        bathrooms=2.5,
        year_built=2015,
        property_type="Single Family",
        estimated_rent=2200,
        days_on_market=45,
        listing_url="https://example.com"
    )
    
    # Perform underwriting analysis
    result = engine.underwrite_property(property_data, oop_requirement=375000)
    
    print(f"Property: {result.property_data.address}")
    print(f"Purchase Price: ${result.property_data.purchase_price:,.0f}")
    print(f"Down Payment: ${result.mortgage_details['down_payment']:,.0f}")
    print(f"Monthly Payment: ${result.mortgage_details['monthly_payment']:,.0f}")
    print(f"Monthly Cash Flow: ${result.cash_flow_analysis['monthly_cash_flow']:,.0f}")
    print(f"CoC Return: {result.coc_return:.1%}")
    print(f"Recommendation: {result.recommendation}")
    print(f"Risk Level: {result.risk_assessment['risk_level']}")
