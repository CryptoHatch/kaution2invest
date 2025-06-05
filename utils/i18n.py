"""
Internationalization utilities for the Kaution2Invest application.
Provides text translation between German (default) and English.
"""

# Dictionary of all text elements in the application
# Format: 'key': {'de': 'German text', 'en': 'English text'}
TEXT = {
    # App title and description
    'app_title': {
        'de': 'Schweizer Mietkautions-Rechner',
        'en': 'Swiss Deposit Investment Calculator'
    },
    'app_description': {
        'de': 'Dieses Tool hilft Ihnen zu visualisieren, wie Ihre Mietkaution bei einer Anlage im Laufe der Zeit wachsen könnte, im Vergleich zu einer Standard-Kaution mit 0% Rendite.',
        'en': 'This tool helps you visualize how your rental deposit could grow if invested over time, compared to leaving it as a standard 0% deposit.'
    },
    
    # Input section
    'input_section_title': {
        'de': 'Geben Sie Ihre Details ein',
        'en': 'Enter Your Details'
    },
    'rent_amount_label': {
        'de': 'Monatliche Miete (CHF)',
        'en': 'Monthly Rent (CHF)'
    },
    'rent_amount_help': {
        'de': 'Ihre aktuelle monatliche Miete in Schweizer Franken',
        'en': 'Your current monthly rent in Swiss Francs'
    },
    'deposit_months_label': {
        'de': 'Kautions-Dauer (Monate)',
        'en': 'Deposit Duration (months)'
    },
    'deposit_months_help': {
        'de': 'Anzahl der Monate, die Ihre Kaution abdeckt (typischerweise 3 Monate in der Schweiz)',
        'en': 'Number of months your deposit covers (typically 3 months in Switzerland)'
    },
    'return_rate_label': {
        'de': 'Jährliche Rendite',
        'en': 'Annual Return Rate'
    },
    'return_rate_help': {
        'de': 'Erwartete jährliche Rendite für Ihre Anlage',
        'en': 'Expected annual return rate on your investment'
    },
    'total_deposit_amount': {
        'de': 'Gesamtbetrag der Kaution: {amount:,.2f} CHF',
        'en': 'Total Deposit Amount: {amount:,.2f} CHF'
    },
    
    # Compound interest explanation
    'compound_interest_title': {
        'de': '💡 Verständnis des Zinseszinseffekts',
        'en': '💡 Understanding Compound Interest'
    },
    'compound_interest_text': {
        'de': '''
        Beim Zinseszins wächst Ihre Anlage nicht nur auf den ursprünglichen Betrag, sondern auch auf die 
        bereits angesammelten Zinsen. Dies schafft einen beschleunigten Wachstumseffekt:

        - **Jahr 1**: Sie verdienen Zinsen nur auf Ihre ursprüngliche Einlage
        - **Jahr 2+**: Sie verdienen Zinsen sowohl auf Ihre ursprüngliche Einlage ALS AUCH auf die vorherigen Zinsen

        Deshalb biegt sich die Investitionswachstumskurve über längere Zeiträume nach oben.
        ''',
        'en': '''
        Compound interest makes your investment grow not just on the initial amount, but also on the accumulated interest 
        over time. This creates an accelerating growth effect:

        - **Year 1**: You earn interest only on your initial deposit
        - **Year 2+**: You earn interest on both your initial deposit AND previous interest

        This is why the investment growth curve bends upward over longer time periods.
        '''
    },
    
    # Results table
    'results_title': {
        'de': 'Vergleich des Anlagewachstums',
        'en': 'Investment Growth Comparison'
    },
    'zero_return_column': {
        'de': '0% Rendite (CHF)',
        'en': '0% Return (CHF)'
    },
    'selected_return_column': {
        'de': '{rate}% Rendite (CHF)',
        'en': '{rate}% Return (CHF)'
    },
    'difference_column': {
        'de': 'Differenz (CHF)',
        'en': 'Difference (CHF)'
    },
    'growth_column': {
        'de': 'Wachstum (%)',
        'en': 'Growth (%)'
    },
    'years_column': {
        'de': 'Jahre',
        'en': 'Years'
    },
    
    # Chart section
    'chart_title': {
        'de': 'Wachstumsvisualisierung',
        'en': 'Growth Visualization'
    },
    'chart_plot_title': {
        'de': 'Kautionswachstum: 0% vs {rate}% jährliche Rendite',
        'en': 'Deposit Growth: 0% vs {rate}% Annual Return'
    },
    'chart_xaxis_title': {
        'de': 'Jahre',
        'en': 'Years'
    },
    'chart_yaxis_title': {
        'de': 'Wert (CHF)',
        'en': 'Value (CHF)'
    },
    'chart_legend_title': {
        'de': 'Szenario',
        'en': 'Scenario'
    },
    'zero_return_name': {
        'de': '0% Rendite',
        'en': '0% Return'
    },
    'selected_return_name': {
        'de': '{rate}% Rendite',
        'en': '{rate}% Return'
    },
    'potential_gain_name': {
        'de': 'Potentieller Gewinn',
        'en': 'Potential Gain'
    },
    'avg_rental_annotation': {
        'de': 'Durchschnittliche Mietdauer<br>in der Schweiz:<br>7 Jahre<br>Potentieller Gewinn:<br>{gain:.2f} CHF',
        'en': 'Average rental<br>duration in CH:<br>7 years<br>Potential gain:<br>{gain:.2f} CHF'
    },
    'hover_year': {
        'de': 'Jahr: {year}',
        'en': 'Year: {year}'
    },
    'hover_value': {
        'de': 'Wert: {value} CHF',
        'en': 'Value: {value} CHF'
    },
    'hover_gain': {
        'de': 'Gewinn: +{gain} CHF',
        'en': 'Gain: +{gain} CHF'
    },
    
    # Explanation section
    'explanation_title': {
        'de': '📖 Wie man diese Ergebnisse interpretiert',
        'en': '📖 How to Interpret These Results'
    },
    'explanation_subtitle': {
        'de': '### Verstehen des Diagramms und der Daten',
        'en': '### Understanding the Chart and Data'
    },
    'explanation_text': {
        'de': '''
        - Die **0% Rendite** (rote Linie) stellt Ihre Kaution dar, wenn sie auf einem Standard-Mietkautionskonto ohne Zinsen belassen wird.
        - Die **Anlagerendite** (blaue Linie mit Markierungen) zeigt, wie Ihr Geld wachsen könnte, wenn es mit der gewählten Rate angelegt wird.
        - Der **hellblaue Bereich** zwischen den Linien stellt Ihren potentiellen Gewinn dar, wenn Sie investieren, anstatt die Kaution auf einem 0%-Konto zu belassen.

        **Schweizer Mietkontext:**
        - Die durchschnittliche Mietdauer in der Schweiz beträgt etwa 7 Jahre.
        - Wie im Diagramm hervorgehoben, gibt es selbst bei dieser durchschnittlichen Dauer einen bemerkenswerten finanziellen Vorteil bei der Anlage Ihrer Kaution.
        - Je länger Sie in der gleichen Mietwohnung bleiben, desto bedeutender wird der Zinseszinsvorteil.

        **Beispielberechnung:** Für eine Ersteinlage von 5.400 CHF bei 3% jährlicher Rendite:
        - Nach 1 Jahr: 5.400 CHF × (1 + 0,03) = 5.562 CHF
        - Nach 2 Jahren: 5.400 CHF × (1 + 0,03)² = 5.729 CHF (nicht nur 5.724 CHF)

        **Hinweis:** Dies ist eine vereinfachte Berechnung, die von konstanten jährlichen Renditen ausgeht und Inflation, Steuern oder Anlagegebühren nicht berücksichtigt.
        ''',
        'en': '''
        - The **0% Return** (red line) represents your deposit if left in a standard rental deposit account with no interest.
        - The **Investment Return** (blue line with markers) shows how your money could grow if invested at the selected rate.
        - The **shaded blue area** between the lines represents your potential gain by investing instead of leaving the deposit in a 0% account.

        **Swiss Rental Context:**
        - The average rental duration in Switzerland is approximately 7 years.
        - As highlighted in the chart, even at this average duration, there is a notable financial benefit to investing your deposit.
        - The longer you stay in the same rental, the more significant the compound interest advantage becomes.

        **Example calculation:** For an initial deposit of 5,400 CHF at 3% annual return:
        - After 1 year: 5,400 CHF × (1 + 0.03) = 5,562 CHF
        - After 2 years: 5,400 CHF × (1 + 0.03)² = 5,729 CHF (not just 5,724 CHF)

        **Note:** This is a simplified calculation that assumes consistent annual returns and does not account for inflation, taxes, or investment fees.
        '''
    },
    
    # Footer
    'footer_text': {
        'de': '© 2023 Kaution2Invest - Ein Tool für Schweizer Mieter zur Optimierung ihrer Mietkautionen',
        'en': '© 2023 Kaution2Invest - A tool for Swiss renters to optimize their rental deposits'
    },
    
    # Language selector
    'language_selector_label': {
        'de': 'Sprache',
        'en': 'Language'
    },
    'language_de': {
        'de': 'Deutsch',
        'en': 'German'
    },
    'language_en': {
        'de': 'Englisch',
        'en': 'English'
    }
}

def get_text(key, lang='de', **kwargs):
    """
    Get text in the specified language.
    
    Args:
        key (str): The key for the text in the TEXT dictionary
        lang (str): The language code ('de' for German, 'en' for English)
        **kwargs: Format parameters to be inserted into the text
        
    Returns:
        str: The translated text
    """
    if key not in TEXT:
        return f"Missing translation: {key}"
        
    if lang not in TEXT[key]:
        # Fallback to German if the specified language is not available
        lang = 'de'
        
    text = TEXT[key][lang]
    
    # Apply formatting if kwargs are provided
    if kwargs:
        try:
            return text.format(**kwargs)
        except KeyError:
            return text
    
    return text 