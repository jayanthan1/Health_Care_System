<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Health Pathway Dashboard</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/boxicons@2.0.7/css/boxicons.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root {
            --primary-color: #2B3467;
            --secondary-color: #3E54AC;
            --accent-color: #4E67E4;
            --sidebar-width: 250px;
        }
        
        body {
            font-family: 'Inter', sans-serif;
            background: #F5F7FF;
            overflow-x: hidden;
        }
        
        .sidebar {
            width: var(--sidebar-width);
            position: fixed;
            left: 0;
            top: 0;
            height: 100vh;
            background: var(--primary-color);
            padding: 20px;
            color: white;
            transition: all 0.3s ease;
            z-index: 1000;
        }
        
        .sidebar .nav-link {
            transition: all 0.3s ease;
            border-radius: 8px;
            padding: 12px 15px;
            margin: 5px 0;
        }
        
        .sidebar .nav-link:hover {
            background: rgba(255, 255, 255, 0.1);
            transform: translateX(5px);
        }
        
        .sidebar .nav-link.active {
            background: var(--accent-color);
        }
        
        .main-content {
            margin-left: var(--sidebar-width);
            padding: 30px;
            transition: all 0.3s ease;
        }
        
        .health-card {
            background: white;
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 25px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
            transition: all 0.3s ease;
            animation: fadeInUp 0.5s ease;
        }
        
        .health-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
        }
        
        .risk-indicator {
            font-size: 2.5rem;
            font-weight: bold;
            text-align: center;
            margin: 20px 0;
            animation: pulse 2s infinite;
        }
        
        .upload-section {
            border: 2px dashed var(--accent-color);
            padding: 30px;
            border-radius: 15px;
            text-align: center;
            background: rgba(78, 103, 228, 0.05);
            transition: all 0.3s ease;
        }
        
        .upload-section:hover {
            background: rgba(78, 103, 228, 0.1);
            transform: scale(1.02);
        }
        
        .key-finding {
            background: white;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 15px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
            border-left: 4px solid var(--accent-color);
            transition: all 0.3s ease;
        }
        
        .key-finding:hover {
            transform: translateX(5px);
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        }
        
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.05); }
            100% { transform: scale(1); }
        }
        
        @keyframes slideInLeft {
            from { opacity: 0; transform: translateX(-20px); }
            to { opacity: 1; transform: translateX(0); }
        }
        
        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .stat-card {
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            color: white;
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 20px;
            animation: fadeInUp 0.5s ease;
        }
        
        .stat-value {
            font-size: 2rem;
            font-weight: bold;
            margin: 10px 0;
        }
        
        .progress-ring {
            transition: all 0.3s ease;
        }
        
        .notification-badge {
            position: absolute;
            top: -5px;
            right: -5px;
            background: #FF6B6B;
            color: white;
            border-radius: 50%;
            padding: 5px 8px;
            font-size: 0.8rem;
            animation: bounce 1s infinite;
        }
        
        @keyframes bounce {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-5px); }
        }

        .risk-assessment-card {
            background: linear-gradient(145deg, #ffffff, #f5f7ff);
            border: none;
            box-shadow: 0 8px 32px rgba(43, 52, 103, 0.1);
        }

        .risk-gauge {
            position: relative;
            width: 200px;
            height: 200px;
            margin: 0 auto;
            background: conic-gradient(from 0deg, var(--accent-color) 0%, transparent 0%);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.8s cubic-bezier(0.4, 0, 0.2, 1);
        }

        .risk-gauge::before {
            content: '';
            position: absolute;
            width: 160px;
            height: 160px;
            background: white;
            border-radius: 50%;
        }

        .risk-value {
            position: relative;
            font-size: 2.5rem;
            font-weight: bold;
            z-index: 1;
        }

        .risk-status {
            position: relative;
            font-size: 1.2rem;
            z-index: 1;
            margin-top: 5px;
        }

        .risk-factors-list {
            list-style: none;
            padding: 0;
            margin: 0;
        }

        .risk-factor-item {
            background: white;
            padding: 12px 15px;
            border-radius: 10px;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            transform: translateX(-20px);
            opacity: 0;
            animation: slideInFade 0.5s ease forwards;
        }

        .risk-factor-item i {
            font-size: 1.5rem;
            margin-right: 12px;
            color: var(--accent-color);
        }

        .recommendations-container {
            background: rgba(78, 103, 228, 0.05);
            border-radius: 15px;
            padding: 20px;
            margin-top: 20px;
            border: 1px solid rgba(78, 103, 228, 0.1);
        }

        .recommendation-item {
            padding: 10px 0;
            border-bottom: 1px solid rgba(78, 103, 228, 0.1);
            transform: translateY(10px);
            opacity: 0;
            animation: fadeUpIn 0.5s ease forwards;
        }

        .recommendation-item:last-child {
            border-bottom: none;
        }

        @keyframes slideInFade {
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }

        @keyframes fadeUpIn {
            to {
                transform: translateY(0);
                opacity: 1;
            }
        }

        .risk-level {
            display: inline-block;
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.9rem;
            font-weight: 500;
            margin-top: 10px;
        }

        .risk-level.low {
            background: rgba(40, 167, 69, 0.1);
            color: #28a745;
        }

        .risk-level.moderate {
            background: rgba(255, 193, 7, 0.1);
            color: #ffc107;
        }

        .risk-level.high {
            background: rgba(220, 53, 69, 0.1);
            color: #dc3545;
        }

        .empty-state {
            background: rgba(78, 103, 228, 0.05);
            border-radius: 10px;
            padding: 20px;
        }

        .badge {
            padding: 0.5em 0.8em;
            border-radius: 20px;
        }

        .risk-gauge {
            width: 200px;
            height: 200px;
            border-radius: 50%;
            background: #f0f0f0;
            position: relative;
            margin: 0 auto;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: background 1s ease;
        }

        .risk-value-container {
            text-align: center;
            position: relative;
            z-index: 2;
        }

        .risk-value {
            font-size: 2.5rem;
            font-weight: bold;
        }

        .risk-status {
            margin-top: 0.5rem;
        }

        .risk-level {
            padding: 0.25rem 1rem;
            border-radius: 20px;
            font-size: 0.9rem;
            font-weight: 500;
        }

        .risk-level.low-risk { background: rgba(40, 167, 69, 0.1); color: #28a745; }
        .risk-level.moderate-risk { background: rgba(255, 193, 7, 0.1); color: #ffc107; }
        .risk-level.high-risk { background: rgba(220, 53, 69, 0.1); color: #dc3545; }

        .risk-factors-list {
            margin-top: 1rem;
        }

        .recommendations-container {
            margin-top: 2rem;
            padding: 1rem;
            background: rgba(78, 103, 228, 0.05);
            border-radius: 10px;
        }

        .chart-container {
            background: white;
            border-radius: 15px;
            padding: 20px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
        }

        .health-card {
            transition: transform 0.3s ease;
            border: none;
            border-radius: 15px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
        }

        .health-card:hover {
            transform: translateY(-5px);
        }

        .card-title {
            color: #2c3e50;
            font-weight: 600;
        }

        .alert {
            border: none;
            border-radius: 10px;
        }

        .alert-warning {
            background-color: rgba(255, 193, 7, 0.1);
            color: #856404;
        }

        .alert-success {
            background-color: rgba(40, 167, 69, 0.1);
            color: #155724;
        }

        .prediction-item {
            background: rgba(37, 117, 252, 0.1);
            border-left: 4px solid #2575fc;
            padding: 15px;
            margin-bottom: 15px;
            border-radius: 8px;
            animation: slideIn 0.5s ease-out;
        }

        .prediction-item.high-risk {
            background: rgba(220, 53, 69, 0.1);
            border-left-color: #dc3545;
        }

        .prediction-item.moderate-risk {
            background: rgba(255, 193, 7, 0.1);
            border-left-color: #ffc107;
        }

        .prevention-tip {
            background: rgba(40, 167, 69, 0.1);
            border-left: 4px solid #28a745;
            padding: 15px;
            margin-bottom: 15px;
            border-radius: 8px;
            animation: slideIn 0.5s ease-out;
        }

        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateX(-20px);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }

        /* Detailed Health Summary and Recommendations */
        .summary-card {
            background: rgba(78, 103, 228, 0.05);
            padding: 1.5rem;
            border-radius: 10px;
            height: 100%;
        }

        .summary-card h5 {
            color: var(--primary-color);
            margin-bottom: 1rem;
        }

        .summary-card ul li {
            margin-bottom: 0.8rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .action-item {
            background: white;
            padding: 1rem;
            border-radius: 10px;
            border-left: 4px solid var(--accent-color);
            display: flex;
            align-items: flex-start;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        }

        .action-item i {
            font-size: 1.5rem;
            color: var(--accent-color);
        }

        .progress-list .progress {
            background-color: rgba(78, 103, 228, 0.1);
        }

        .risk-factor-item {
            display: flex;
            align-items: center;
            padding: 12px;
            margin-bottom: 10px;
            border-radius: 8px;
            animation: slideIn 0.3s ease-out forwards;
        }

        .risk-factor-item.high {
            background: rgba(220, 53, 69, 0.1);
            border-left: 4px solid #dc3545;
        }

        .risk-factor-item.moderate {
            background: rgba(255, 193, 7, 0.1);
            border-left: 4px solid #ffc107;
        }

        .risk-factor-item.low {
            background: rgba(40, 167, 69, 0.1);
            border-left: 4px solid #28a745;
        }

        .risk-factor-content {
            margin-left: 12px;
        }

        .risk-factor-title {
            font-weight: 500;
            margin-bottom: 2px;
        }

        .risk-factor-value {
            font-size: 0.9rem;
            color: #666;
        }

        .recommendation-item {
            background: rgba(37, 117, 252, 0.1);
            padding: 12px;
            margin-bottom: 8px;
            border-radius: 8px;
            display: flex;
            align-items: center;
            animation: slideIn 0.3s ease-out forwards;
        }

        .recommendation-item i {
            color: #2575fc;
            margin-right: 10px;
        }

        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateX(-20px);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }
    </style>
</head>
<body>
    <div class="sidebar">
        <h3 class="mb-4">Health Pathway</h3>
        <nav class="mt-4">
            <ul class="nav flex-column">
                <li class="nav-item">
                    <a href="{{ url_for('dashboard') }}" class="nav-link text-white {{ 'active' if active_page == 'dashboard' }}">
                        <i class="bx bxs-dashboard me-2"></i>Dashboard
                    </a>
                </li>
                <li class="nav-item">
                    <a href="{{ url_for('health_history') }}" class="nav-link text-white {{ 'active' if active_page == 'health_history' }}">
                        <i class="bx bx-history me-2"></i>Health History
                    </a>
                </li>
                <li class="nav-item">
                    <a href="{{ url_for('health_records') }}" class="nav-link text-white">
                        <i class="bx bx-file me-2"></i>Health Records
                    </a>
                </li>
                <li class="nav-item">
                    <a href="{{ url_for('profile_settings') }}" class="nav-link text-white">
                        <i class="bx bx-user me-2"></i>Profile Settings
                    </a>
                </li>
                <li class="nav-item">
                    <a href="{{ url_for('complete_profile') }}" class="nav-link text-white">
                        <i class="bx bx-user-circle me-2"></i>Complete Health Profile
                    </a>
                </li>
                <li class="nav-item mt-auto">
                    <a href="{{ url_for('logout') }}" class="nav-link text-white">
                        <i class="bx bx-log-out me-2"></i>Logout
                    </a>
                </li>
            </ul>
        </nav>
    </div>

    <div class="main-content">
        <div class="container-fluid">
            <!-- Welcome Section -->
            <div class="row mb-4">
                <div class="col-12">
                    <h2 class="animate__animated animate__fadeIn">Welcome back, {{ user.name }}!</h2>
                    <p class="text-muted animate__animated animate__fadeIn animate__delay-1s">
                        Here's your health overview for today
                    </p>
                </div>
            </div>

            <!-- Quick Stats at the top -->
            <div class="row mb-4">
                <div class="col-md-3">
                    <div class="stat-card">
                        <i class="bx bx-heart mb-2" style="font-size: 2rem;"></i>
                        <h5>Heart Rate</h5>
                        <div class="stat-value">{{ health_data.heart_rate }} BPM</div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="stat-card">
                        <i class="bx bx-line-chart mb-2" style="font-size: 2rem;"></i>
                        <h5>Blood Pressure</h5>
                        <div class="stat-value">{{ health_data.blood_pressure }}</div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="stat-card">
                        <i class="bx bx-pulse mb-2" style="font-size: 2rem;"></i>
                        <h5>BMI</h5>
                        <div class="stat-value">{{ "%.1f"|format(health_data.bmi) }}</div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="stat-card">
                        <i class="bx bx-run mb-2" style="font-size: 2rem;"></i>
                        <h5>Activity Level</h5>
                        <div class="stat-value">{{ health_data.physical_activity_level }}h/week</div>
                    </div>
                </div>
            </div>

            <!-- Add this after the Quick Stats section -->
            <div class="row mb-4">
                <div class="col-12">
                    <div class="health-card">
                        <h4 class="mb-3">Health Progress</h4>
                        <div class="d-flex justify-content-between align-items-center mb-3">
                            <span>Last Updated: {{ health_data.last_updated.strftime('%B %d, %Y at %I:%M %p') }}</span>
                            {% if health_data.improvement_percentage > 0 %}
                            <span class="badge bg-success">
                                <i class="bx bx-trending-up me-1"></i>
                                {{ "%.1f"|format(health_data.improvement_percentage) }}% Improvement
                            </span>
                            {% endif %}
                        </div>
                        <div class="progress" style="height: 10px;">
                            <div class="progress-bar bg-success" 
                                 role="progressbar" 
                                 style="width: {{ health_data.improvement_percentage }}%">
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Add this after the Health Progress section -->
            <div class="row mb-4">
                <div class="col-12">
                    <div class="health-card">
                        <h4 class="mb-3">Health History</h4>
                        <canvas id="healthHistoryChart"></canvas>
                    </div>
                </div>
            </div>

            <!-- Timeline Charts side by side -->
            <div class="row mb-4">
                <div class="col-md-6">
                    <div class="card health-card">
                        <div class="card-body">
                            <h4 class="card-title mb-3">Health Decline Projection</h4>
                            <div class="chart-container" style="position: relative; height:250px;">
                                <canvas id="healthDeclineChart"></canvas>
                            </div>
                            <div class="mt-2">
                                <div class="alert alert-warning py-2">
                                    <i class='bx bx-info-circle me-2'></i>
                                    Without intervention
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="card health-card">
                        <div class="card-body">
                            <h4 class="card-title mb-3">Health Improvement Projection</h4>
                            <div class="chart-container" style="position: relative; height:250px;">
                                <canvas id="healthImprovementChart"></canvas>
                            </div>
                            <div class="mt-2">
                                <div class="alert alert-success py-2">
                                    <i class='bx bx-trending-up me-2'></i>
                                    With recommendations
                                </div>  
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="row">
                <div class="col-md-8">
                    <div class="health-card">
                        <h4>Health Timeline Prediction</h4>
                        <canvas id="healthTimelineChart"></canvas>
                    </div>
                    <div class="health-card">
                        <h4>Recent Analysis Results</h4>
                        <div id="analysisHistory">
                            {% if analysis_history %}
                                {% for analysis in analysis_history %}
                                <div class="key-finding animate__animated animate__fadeInLeft" style="animation-delay: {{ loop.index0 * 0.1 }}s">
                                    <div class="d-flex justify-content-between align-items-center">
                                        <strong>{{ analysis.date }}</strong>
                                        {% if analysis.is_new %}
                                        <span class="badge bg-primary animate__animated animate__pulse animate__infinite">New</span>
                                        {% endif %}
                                    </div>
                                    <p class="mb-2">{{ analysis.summary }}</p>
                                    <small class="text-muted">Findings: {{ analysis.findings }}</small>
                                </div>
                                {% endfor %}
                            {% else %}
                                <div class="empty-state text-center py-4 animate__animated animate__fadeIn">
                                    <i class="bx bx-notepad" style="font-size: 3rem; color: var(--accent-color)"></i>
                                    <h5 class="mt-3">No Analysis History</h5>
                                    <p class="text-muted">Upload your medical reports to get started</p>
                                </div>
                            {% endif %}
                        </div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="health-card risk-assessment-card">
                        <h4 class="d-flex align-items-center mb-4">
                            <i class="bx bx-shield-quarter me-2"></i>
                            Risk Assessment
                        </h4>
                        <div class="risk-indicator-container">
                            <div class="risk-gauge animate__animated animate__fadeIn" id="riskScore">
                                <div class="spinner-border text-primary" role="status">
                                    <span class="visually-hidden">Loading...</span>
                                </div>
                            </div>
                            <div class="risk-details mt-4" id="riskRecommendations"></div>
                        </div>
                    </div>
                    <div class="health-card">
                        <h4>Upload Medical Reports</h4>
                        <div class="upload-section">
                            <form id="pdfUploadForm" enctype="multipart/form-data">
                                <input type="file" class="form-control mb-3" accept=".pdf" name="file" required>
                                <button type="submit" class="btn btn-primary w-100">
                                    <i class="bx bx-upload me-2"></i>Upload & Analyze
                                </button>
                            </form>
                            <div id="uploadProgress" class="progress mt-3" style="display: none;">
                                <div class="progress-bar progress-bar-striped progress-bar-animated" role="progressbar"></div>
                            </div>
                            <div id="analysisResult" class="analysis-result mt-3"></div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Detailed Health Summary and Recommendations -->
            <div class="row mb-4">
                <div class="col-12">
                    <div class="card health-card">
                        <div class="card-body">
                            <h4 class="card-title mb-4">
                                <i class="bx bx-clipboard me-2"></i>Detailed Health Summary
                            </h4>
                            <div class="row">
                                <div class="col-md-4">
                                    <div class="summary-card">
                                        <h5>Vital Statistics</h5>
                                        <ul class="list-unstyled">
                                            <li>BMI: <strong>{{ "%.1f"|format(health_data.bmi) }}</strong> 
                                                <span class="badge {{ 'bg-success' if health_data.bmi < 25 else 'bg-warning' }}">
                                                    {{ 'Normal' if health_data.bmi < 25 else 'Above Normal' }}
                                                </span>
                                            </li>
                                            <li>Blood Pressure: <strong>{{ health_data.blood_pressure }}</strong></li>
                                            <li>Heart Rate: <strong>{{ health_data.heart_rate }} BPM</strong></li>
                                        </ul>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="summary-card">
                                        <h5>Lifestyle Factors</h5>
                                        <ul class="list-unstyled">
                                            <li>Physical Activity: <strong>{{ health_data.physical_activity_level }}h/week</strong></li>
                                            <li>Sleep: <strong>{{ health_data.sleep_hours }}h/day</strong></li>
                                            <li>Stress Level: <strong>{{ health_data.stress_level }}/10</strong></li>
                                        </ul>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="summary-card">
                                        <h5>Health Goals</h5>
                                        <div class="progress-list">
                                            <div class="progress mb-3" style="height: 10px;">
                                                <div class="progress-bar bg-success" 
                                                     role="progressbar" 
                                                     style="width: {{ health_data.physical_activity_level/3 * 100 }}%" 
                                                     aria-valuenow="{{ health_data.physical_activity_level }}" 
                                                     aria-valuemin="0" 
                                                     aria-valuemax="3">
                                                </div>
                                            </div>
                                            <small>Activity Goal: {{ health_data.physical_activity_level }}/3 hours daily</small>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            
                            <!-- Action Items -->
                            <div class="mt-4">
                                <h5>Recommended Actions</h5>
                                <div class="row">
                                    {% set action_items = get_action_items(health_data) %}
                                    {% for item in action_items %}
                                    <div class="col-md-6 mb-3">
                                        <div class="action-item">
                                            <i class="bx {{ item.icon }} me-2"></i>
                                            <div>
                                                <h6 class="mb-1">{{ item.title }}</h6>
                                                <p class="mb-0 text-muted">{{ item.description }}</p>
                                            </div>
                                        </div>
                                    </div>
                                    {% endfor %}
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Disease Prediction Section -->
            <div class="row mb-4">
                <div class="col-12">
                    <div class="card health-card">
                        <div class="card-body">
                            <h4 class="card-title mb-4">
                                <i class="bx bx-radar me-2"></i>Health Risk Predictions & Recommendations
                            </h4>
                            <div class="predictions-container">
                                <div class="row">
                                    <div class="col-md-6">
                                        <div class="prediction-list">
                                            <h5>Potential Health Risks</h5>
                                            <div id="healthRisks" class="mt-3">
                                                <!-- Predictions will be populated dynamically -->
                                            </div>
                                        </div>
                                    </div>
                                    <div class="col-md-6">
                                        <div class="prevention-tips">
                                            <h5>Preventive Measures</h5>
                                            <div id="preventiveMeasures" class="mt-3">
                                                <!-- Prevention tips will be populated dynamically -->
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- PDF Analysis Results Section -->
            <div id="pdfAnalysisResults" class="mt-4" style="display: none;">
                <div class="card health-card">
                    <div class="card-header bg-primary text-white">
                        <h5 class="mb-0">PDF Analysis Results</h5>
                    </div>
                    <div class="card-body">
                        <div class="row">
                            <div class="col-md-6">
                                <h6 class="mb-3">Health Metrics</h6>
                                <div id="metricsContainer"></div>
                            </div>
                            <div class="col-md-6">
                                <h6 class="mb-3">Key Findings</h6>
                                <div id="findingsContainer"></div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        // Initialize Health Timeline Chart
        const timelineCtx = document.getElementById('healthTimelineChart').getContext('2d');
        let healthChart = new Chart(timelineCtx, {
            type: 'line',
            data: {
                labels: ['Now', '3 months', '6 months', '1 year', '2 years'],
                datasets: [{
                    label: 'Predicted Health Score',
                    data: JSON.parse('{{ health_predictions|tojson|safe }}'),
                    borderColor: '#4E67E4',
                    tension: 0.4,
                    fill: false
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100,
                        ticks: {
                            callback: function(value) {
                                return value + '%';
                            }
                        }
                    }
                },
                animation: {
                    duration: 2000,
                    easing: 'easeInOutQuart'
                }
            }
        });

        // Handle PDF Upload and Analysis
        document.getElementById('pdfUploadForm').addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            const progressBar = document.getElementById('uploadProgress');
            const progressBarInner = progressBar.querySelector('.progress-bar');
            const analysisResult = document.getElementById('analysisResult');
            const pdfResults = document.getElementById('pdfAnalysisResults');
            
            // Show progress bar
            progressBar.style.display = 'block';
            progressBarInner.style.width = '50%';
            
            fetch('/upload_pdf', {
                method: 'POST',
                body: formData
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                progressBarInner.style.width = '100%';
                
                if (data.success) {
                    // Show results container
                    pdfResults.style.display = 'block';
                    
                    // Display metrics
                    const metricsHtml = Object.entries(data.metrics)
                        .map(([key, value]) => `
                            <div class="metric-item mb-2 p-2 border-bottom">
                                <strong>${key.replace(/_/g, ' ').toUpperCase()}:</strong> 
                                <span class="float-end">${value}</span>
                            </div>
                        `).join('');
                    document.getElementById('metricsContainer').innerHTML = metricsHtml;
                    
                    // Display findings
                    const findingsHtml = data.findings
                        .map(finding => `
                            <div class="finding-item mb-2 p-2 border-left border-primary">
                                <i class="bx bx-check-circle text-success me-2"></i>
                                ${finding}
                            </div>
                        `).join('');
                    document.getElementById('findingsContainer').innerHTML = findingsHtml;
                    
                    // Show success message
                    analysisResult.innerHTML = `
                        <div class="alert alert-success mt-3">
                            <i class="bx bx-check-circle me-2"></i>
                            PDF analyzed successfully!
                        </div>
                    `;
                } else {
                    throw new Error(data.error || 'Analysis failed');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                analysisResult.innerHTML = `
                    <div class="alert alert-danger mt-3">
                        <i class="bx bx-error-circle me-2"></i>
                        ${error.message}
                    </div>
                `;
            })
            .finally(() => {
                // Hide progress bar after a delay
                setTimeout(() => {
                    progressBar.style.display = 'none';
                    progressBarInner.style.width = '0%';
                }, 1000);
            });
        });

        // Update Risk Score with animation
        async function updateRiskScore() {
            const riskElement = document.getElementById('riskScore');
            const recommendationsElement = document.getElementById('riskRecommendations');

            try {
                // Show loading state
                riskElement.innerHTML = `
                    <div class="text-center">
                        <div class="spinner-border text-primary" role="status">
                            <span class="visually-hidden">Loading...</span>
                        </div>
                    </div>
                `;

                const response = await fetch('/get_risk_score');
                console.log('Risk score response:', response); // Debug log
                
                const data = await response.json();
                console.log('Risk score data:', data); // Debug log
                
                if (!data.success) {
                    throw new Error(data.error || 'Failed to fetch risk score');
                }
                
                // Determine color based on risk level
                let color;
                if (data.risk_score < 30) {
                    color = '#28a745'; // green for low risk
                } else if (data.risk_score < 70) {
                    color = '#ffc107'; // yellow for moderate risk
                } else {
                    color = '#dc3545'; // red for high risk
                }
                
                // Update risk gauge with animation
                riskElement.style.transition = 'background 1s ease';
                riskElement.style.background = `conic-gradient(from 0deg, ${color} ${data.risk_score}%, transparent ${data.risk_score}%)`;
                riskElement.innerHTML = `
                    <div class="risk-value-container text-center animate__animated animate__fadeIn">
                        <div class="risk-value" style="color: ${color}">${data.risk_score}%</div>
                        <div class="risk-status">
                            <span class="risk-level ${data.status.toLowerCase().replace(' ', '-')}">${data.status}</span>
                        </div>
                    </div>
                `;
                
                // Update recommendations
                if (data.risk_factors && data.risk_factors.length > 0) {
                    recommendationsElement.innerHTML = `
                        <div class="mt-4 animate__animated animate__fadeIn">
                            <h5>Risk Factors</h5>
                            <div class="risk-factors-list">
                                ${data.risk_factors.map(factor => `
                                    <div class="risk-factor-item ${factor.severity}">
                                        <i class="bx ${getRiskIcon(factor.severity)}"></i>
                                        <div class="risk-factor-content">
                                            <div class="risk-factor-title">${factor.factor}</div>
                                            <div class="risk-factor-value">${factor.value}</div>
                                        </div>
                                    </div>
                                `).join('')}
                            </div>
                            
                            <h5 class="mt-4">Recommendations</h5>
                            <div class="recommendations-container">
                                ${data.recommendations.map((rec, index) => `
                                    <div class="recommendation-item" style="animation-delay: ${index * 0.1}s">
                                        <i class="bx bx-check"></i>
                                        ${rec}
                                    </div>
                                `).join('')}
                            </div>
                        </div>
                    `;
                } else {
                    recommendationsElement.innerHTML = `
                        <div class="alert alert-info mt-4 animate__animated animate__fadeIn">
                            Complete your health profile for personalized recommendations
                        </div>
                    `;
                }
            } catch (error) {
                console.error('Error updating risk score:', error);
                showErrorState(riskElement, recommendationsElement);
            }
        }

        // Add event listener for when the page loads
        document.addEventListener('DOMContentLoaded', function() {
            updateRiskScore();
            
            // Refresh risk score every 5 minutes
            setInterval(updateRiskScore, 300000);
        });

        // Update Health Timeline with animation
        function updateHealthTimeline(predictions) {
            if (predictions && predictions.length) {
                healthChart.data.datasets[0].data = predictions;
                healthChart.update('active');
            }
        }

        // Add to Analysis History with animation
        function addToAnalysisHistory(analysis) {
            const historyElement = document.getElementById('analysisHistory');
            const historyItem = document.createElement('div');
            historyItem.className = 'key-finding animate__animated animate__fadeInLeft';
            historyItem.innerHTML = `
                <div class="d-flex justify-content-between align-items-center">
                    <strong>${analysis.date}</strong>
                    <span class="badge bg-primary">New</span>
                </div>
                <p class="mb-2">${analysis.summary}</p>
                <small class="text-muted">Findings: ${analysis.findings}</small>
            `;
            historyElement.insertBefore(historyItem, historyElement.firstChild);
        }

        // Add scroll reveal animation
        document.addEventListener('DOMContentLoaded', function() {
            const cards = document.querySelectorAll('.health-card');
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add('animate__animated', 'animate__fadeInUp');
                    }
                });
            });
            
            cards.forEach(card => observer.observe(card));
        });

        // Initialize Decline Timeline Chart
        const declineCtx = document.getElementById('healthDeclineChart').getContext('2d');
        const declineChart = new Chart(declineCtx, {
            type: 'line',
            data: {
                labels: ['Now', '3 Months', '6 Months', '1 Year', '2 Years'],
                datasets: [{
                    label: 'Health Decline Rate',
                    data: {{ health_decline_predictions|tojson|safe }},
                    borderColor: '#dc3545',
                    backgroundColor: 'rgba(220, 53, 69, 0.1)',
                    tension: 0.4,
                    fill: true,
                    pointRadius: 5,
                    pointHoverRadius: 8
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: false,
                        min: 40,
                        max: 100,
                        grid: {
                            color: 'rgba(0,0,0,0.05)'
                        }
                    },
                    x: {
                        grid: {
                            display: false
                        }
                    }
                },
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        backgroundColor: 'rgba(0,0,0,0.8)',
                        padding: 12,
                        titleFont: {
                            size: 14
                        },
                        bodyFont: {
                            size: 13
                        }
                    }
                }
            }
        });

        // Initialize Improvement Timeline Chart
        const improvementCtx = document.getElementById('healthImprovementChart').getContext('2d');
        const improvementChart = new Chart(improvementCtx, {
            type: 'line',
            data: {
                labels: ['Now', '3 Months', '6 Months', '1 Year', '2 Years'],
                datasets: [{
                    label: 'With Recommendations',
                    data: (function() {
                        const currentScore = {{ health_predictions[0]|tojson|safe }};
                        const maxScore = 100;
                        const improvement = [currentScore];
                        
                        for (let i = 1; i < 5; i++) {
                            const monthsElapsed = i === 4 ? 24 : i * 3;
                            const improvementRate = monthsElapsed <= 12 ? 0.15 : 0.08;
                            
                            const previousScore = improvement[i-1];
                            const roomForImprovement = maxScore - previousScore;
                            const nextScore = previousScore + (roomForImprovement * improvementRate);
                            
                            improvement.push(Math.min(maxScore, nextScore));
                        }
                        return improvement;
                    })(),
                    borderColor: '#28a745',
                    backgroundColor: 'rgba(40, 167, 69, 0.1)',
                    tension: 0.4,
                    fill: true,
                    pointRadius: 5,
                    pointHoverRadius: 8
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: false,
                        min: Math.max(30, {{ health_predictions[0] - 10 }}),
                        max: 100,
                        grid: {
                            color: 'rgba(0,0,0,0.05)'
                        },
                        ticks: {
                            callback: function(value) {
                                return value + '%';
                            }
                        }
                    },
                    x: {
                        grid: {
                            display: false
                        }
                    }
                },
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        backgroundColor: 'rgba(0,0,0,0.8)',
                        padding: 12,
                        titleFont: {
                            size: 14
                        },
                        bodyFont: {
                            size: 13
                        },
                        callbacks: {
                            label: function(context) {
                                return `Health Score: ${context.parsed.y.toFixed(1)}%`;
                            },
                            afterLabel: function(context) {
                                const improvement = (context.parsed.y - {{ health_predictions[0] }}).toFixed(1);
                                return improvement > 0 ? `Improvement: +${improvement}%` : '';
                            }
                        }
                    }
                }
            }
        });

        // Function to update disease predictions
        async function updateDiseasePredictions() {
            try {
                const response = await fetch('/get_disease_predictions');
                const data = await response.json();
                
                if (data.success) {
                    const risksContainer = document.getElementById('healthRisks');
                    const preventionContainer = document.getElementById('preventiveMeasures');
                    
                    // Update health risks
                    risksContainer.innerHTML = data.predictions.map(pred => `
                        <div class="prediction-item ${pred.risk_level.toLowerCase()}-risk">
                            <h6 class="mb-2">${pred.condition}</h6>
                            <div class="risk-level mb-2">
                                Risk Level: <span class="badge bg-${pred.risk_level === 'High' ? 'danger' : 
                                                                   pred.risk_level === 'Moderate' ? 'warning' : 'info'}">
                                    ${pred.risk_level}
                                </span>
                            </div>
                            <small class="text-muted">${pred.description}</small>
                        </div>
                    `).join('');
                    
                    // Update prevention tips
                    preventionContainer.innerHTML = data.preventive_measures.map(measure => `
                        <div class="prevention-tip">
                            <i class="bx bx-check-circle me-2"></i>
                            ${measure}
                        </div>
                    `).join('');
                }
            } catch (error) {
                console.error('Error fetching disease predictions:', error);
            }
        }

        // Call the function when page loads
        document.addEventListener('DOMContentLoaded', function() {
            updateDiseasePredictions();
            // Update predictions every 5 minutes
            setInterval(updateDiseasePredictions, 300000);
        });

        // Initialize Health History Chart
        const healthHistoryCtx = document.getElementById('healthHistoryChart').getContext('2d');
        const healthHistory = new Chart(healthHistoryCtx, {
            type: 'line',
            data: {
                labels: {{ health_history|map(attribute='date')|list|tojson|safe }},
                datasets: [{
                    label: 'Health Improvement',
                    data: {{ health_history|map(attribute='improvement_percentage')|list|tojson|safe }},
                    borderColor: '#28a745',
                    tension: 0.4,
                    fill: false
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'bottom'
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return `Improvement: ${context.parsed.y.toFixed(1)}%`;
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100,
                        ticks: {
                            callback: function(value) {
                                return value + '%';
                            }
                        }
                    }
                }
            }
        });
    </script>
</body>
</html>
