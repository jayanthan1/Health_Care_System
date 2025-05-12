import PyPDF2
import re
import nltk
from nltk.tokenize import sent_tokenize
import json
import os

def download_nltk_data():
    """Download required NLTK data packages"""
    try:
        # Create nltk_data directory in the project folder
        nltk_data_dir = os.path.join(os.path.dirname(__file__), 'nltk_data')
        os.makedirs(nltk_data_dir, exist_ok=True)
        
        # Set NLTK data path
        nltk.data.path.append(nltk_data_dir)
        
        # Download required NLTK data
        required_packages = ['punkt']
        for package in required_packages:
            try:
                nltk.data.find(f'tokenizers/{package}')
            except LookupError:
                print(f"Downloading {package}...")
                nltk.download(package, download_dir=nltk_data_dir, quiet=True)
                
        return True
    except Exception as e:
        print(f"Error downloading NLTK data: {str(e)}")
        return False

# Initialize NLTK data at module import
if not download_nltk_data():
    raise RuntimeError("Failed to download required NLTK data")

def analyze_pdf(file_path):
    try:
        # Extract text from PDF
        text = extract_text(file_path)
        
        # Extract key health metrics
        metrics = extract_health_metrics(text)
        
        # Extract key findings
        findings = extract_key_findings(text)
        
        analysis = {
            'success': True,
            'analysis': {
                'summary': generate_summary(metrics, findings),
                'key_findings': findings,
                'metrics': metrics,
                'recommendations': generate_recommendations(metrics, findings),
                'diagnoses': extract_diagnoses(text)
            }
        }
        
        return analysis
        
    except Exception as e:
        print(f"PDF Analysis Error: {str(e)}")
        return {
            'success': False,
            'error': str(e)
        }

def extract_text(file_path):
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    return text

def extract_health_metrics(text):
    metrics = {}
    
    # Regular expressions for common health metrics
    patterns = {
        'blood_pressure': r'(?:BP|blood pressure)[:\s]+(\d{2,3}\/\d{2,3})',
        'heart_rate': r'(?:HR|heart rate|pulse)[:\s]+(\d{2,3})',
        'glucose': r'(?:glucose|blood sugar)[:\s]+(\d{2,3})',
        'cholesterol': r'(?:cholesterol)[:\s]+(\d{2,3})',
        'bmi': r'(?:BMI)[:\s]+(\d{1,2}\.?\d{0,2})',
        'weight': r'(?:weight)[:\s]+(\d{2,3}\.?\d{0,2})',
        'height': r'(?:height)[:\s]+(\d{1,3})',
    }
    
    for metric, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            metrics[metric] = match.group(1)
    
    return metrics

def extract_key_findings(text):
    findings = []
    sentences = sent_tokenize(text)
    
    # Keywords that might indicate important findings
    keywords = [
        'diagnosis', 'condition', 'finding', 'observed',
        'abnormal', 'normal', 'elevated', 'low', 'high',
        'recommended', 'treatment', 'prescribed'
    ]
    
    for sentence in sentences:
        if any(keyword in sentence.lower() for keyword in keywords):
            findings.append(sentence.strip())
    
    return findings[:5]  # Return top 5 findings

def extract_diagnoses(text):
    diagnoses = []
    diagnosis_patterns = [
        r'diagnosis[:\s]+([^\.]+)',
        r'diagnosed with[:\s]+([^\.]+)',
        r'assessment[:\s]+([^\.]+)'
    ]
    
    for pattern in diagnosis_patterns:
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            diagnoses.append(match.group(1).strip())
    
    return list(set(diagnoses))  # Remove duplicates

def generate_summary(metrics, findings):
    summary = "Medical report analysis completed. "
    if metrics:
        summary += f"Found {len(metrics)} health metrics. "
    if findings:
        summary += f"Identified {len(findings)} key findings."
    return summary

def generate_recommendations(metrics, findings):
    recommendations = []
    
    # Add recommendations based on metrics
    if metrics.get('blood_pressure'):
        bp_sys, bp_dia = map(int, metrics['blood_pressure'].split('/'))
        if bp_sys > 120 or bp_dia > 80:
            recommendations.append("Monitor blood pressure regularly")
    
    if metrics.get('glucose'):
        glucose = float(metrics['glucose'])
        if glucose > 100:
            recommendations.append("Follow up with glucose monitoring")
    
    # Add general recommendations
    recommendations.extend([
        "Schedule regular check-ups",
        "Maintain a healthy diet and exercise routine",
        "Keep track of any new symptoms"
    ])
    
    return recommendations

nltk.download('punkt')