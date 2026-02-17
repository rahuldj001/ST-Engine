// ===== CONFIGURATION =====
const API_BASE_URL = 'http://localhost:8000';  // Update this to your FastAPI backend URL

// ===== NAVBAR SCROLL EFFECT =====
const navbar = document.querySelector('.navbar');
let lastScroll = 0;

window.addEventListener('scroll', () => {
    const currentScroll = window.pageYOffset;

    if (currentScroll > 100) {
        navbar.classList.add('scrolled');
    } else {
        navbar.classList.remove('scrolled');
    }

    lastScroll = currentScroll;
});

// ===== MOBILE MENU =====
const mobileMenuBtn = document.getElementById('mobileMenuBtn');
const navLinks = document.querySelector('.nav-links');

if (mobileMenuBtn) {
    mobileMenuBtn.addEventListener('click', () => {
        navLinks.classList.toggle('active');
        mobileMenuBtn.classList.toggle('active');
    });
}

// ===== SMOOTH SCROLL =====
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));

        if (target) {
            const offsetTop = target.offsetTop - 80;
            window.scrollTo({
                top: offsetTop,
                behavior: 'smooth'
            });

            // Close mobile menu if open
            if (navLinks.classList.contains('active')) {
                navLinks.classList.remove('active');
                mobileMenuBtn.classList.remove('active');
            }
        }
    });
});

// ===== FORM SUBMISSION =====
const ideaForm = document.getElementById('ideaForm');
const loadingModal = document.getElementById('loadingModal');

if (ideaForm) {
    ideaForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        // Get form data
        const formData = {
            idea: document.getElementById('idea').value.trim(),
            industry: document.getElementById('industry').value.trim() || 'general',
            target_market: document.getElementById('market').value.trim() || 'global'
        };

        // Validate
        if (!formData.idea) {
            showNotification('Please describe your startup idea', 'error');
            return;
        }

        // Show loading modal
        showLoadingModal();

        try {
            // Call API
            const response = await fetch(`${API_BASE_URL}/api/analyze`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const result = await response.json();

            // Hide loading modal
            hideLoadingModal();

            // Show results
            displayResults(result);

            // Reset form
            ideaForm.reset();

        } catch (error) {
            console.error('Error:', error);
            hideLoadingModal();
            showNotification('Failed to analyze idea. Please try again.', 'error');
        }
    });
}

// ===== LOADING MODAL =====
function showLoadingModal() {
    loadingModal.classList.add('active');
    document.body.style.overflow = 'hidden';

    // Animate progress steps
    const steps = document.querySelectorAll('.progress-step');
    steps.forEach((step, index) => {
        setTimeout(() => {
            step.classList.add('active');
        }, index * 2000);
    });
}

function hideLoadingModal() {
    loadingModal.classList.remove('active');
    document.body.style.overflow = '';

    // Reset progress steps
    const steps = document.querySelectorAll('.progress-step');
    steps.forEach(step => {
        step.classList.remove('active');
    });
}

// ===== DISPLAY RESULTS =====
function displayResults(data) {
    // Create results page or modal
    const resultsHTML = `
        <div class="results-modal modal active">
            <div class="results-content glass-card">
                <button class="close-btn" onclick="closeResults()">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                        <path d="M18 6L6 18M6 6L18 18" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                    </svg>
                </button>
                
                <div class="results-header">
                    <h2>Feasibility Report</h2>
                    <p class="results-idea">${data.idea}</p>
                </div>
                
                <div class="results-score">
                    <div class="score-circle">
                        <svg width="200" height="200">
                            <circle cx="100" cy="100" r="90" fill="none" stroke="rgba(255,255,255,0.1)" stroke-width="12"/>
                            <circle cx="100" cy="100" r="90" fill="none" stroke="url(#scoreGradient)" stroke-width="12" 
                                    stroke-dasharray="${2 * Math.PI * 90}" 
                                    stroke-dashoffset="${2 * Math.PI * 90 * (1 - data.report.success_probability / 100)}"
                                    stroke-linecap="round"
                                    transform="rotate(-90 100 100)"/>
                            <defs>
                                <linearGradient id="scoreGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                                    <stop offset="0%" stop-color="#43e97b"/>
                                    <stop offset="100%" stop-color="#38f9d7"/>
                                </linearGradient>
                            </defs>
                        </svg>
                        <div class="score-text">
                            <div class="score-number">${data.report.success_probability}%</div>
                            <div class="score-label">Success Probability</div>
                        </div>
                    </div>
                    <div class="score-location">
                        <div class="location-icon">📍</div>
                        <div class="location-text">
                            <div class="location-label">Best Location</div>
                            <div class="location-value">${data.report.best_location}</div>
                        </div>
                    </div>
                </div>
                
                <div class="results-tabs">
                    <button class="tab-btn active" data-tab="market">Market Analysis</button>
                    <button class="tab-btn" data-tab="audience">Target Audience</button>
                    <button class="tab-btn" data-tab="revenue">Revenue Model</button>
                    <button class="tab-btn" data-tab="competition">Competition</button>
                    <button class="tab-btn" data-tab="costs">Cost Structure</button>
                    <button class="tab-btn" data-tab="gtm">Go-to-Market</button>
                </div>
                
                <div class="results-panels">
                    <div class="tab-panel active" data-panel="market">
                        <div class="panel-content">${formatText(data.report.market_analysis)}</div>
                    </div>
                    <div class="tab-panel" data-panel="audience">
                        <div class="panel-content">${formatText(data.report.target_audience)}</div>
                    </div>
                    <div class="tab-panel" data-panel="revenue">
                        <div class="panel-content">${formatText(data.report.revenue_model)}</div>
                    </div>
                    <div class="tab-panel" data-panel="competition">
                        <div class="panel-content">${formatText(data.report.competition_analysis)}</div>
                    </div>
                    <div class="tab-panel" data-panel="costs">
                        <div class="panel-content">${formatText(data.report.cost_structure)}</div>
                    </div>
                    <div class="tab-panel" data-panel="gtm">
                        <div class="panel-content">${formatText(data.report.go_to_market)}</div>
                    </div>
                </div>
                
                ${data.critique ? `
                    <div class="critique-section">
                        <h3>Expert Critique</h3>
                        <div class="critique-content">${formatText(data.critique)}</div>
                    </div>
                ` : ''}
                
                <div class="results-actions">
                    <button class="btn btn-primary" onclick="downloadReport()">
                        <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                            <path d="M10 14L6 10M10 14L14 10M10 14V2M18 14V18H2V14" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                        </svg>
                        <span>Download Report</span>
                    </button>
                    <button class="btn btn-secondary" onclick="closeResults()">
                        <span>Analyze Another Idea</span>
                    </button>
                </div>
            </div>
        </div>
    `;

    // Add to body
    document.body.insertAdjacentHTML('beforeend', resultsHTML);

    // Add tab switching functionality
    setupTabs();

    // Store data for download
    window.currentReport = data;
}

// ===== TAB SWITCHING =====
function setupTabs() {
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabPanels = document.querySelectorAll('.tab-panel');

    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const tabName = btn.dataset.tab;

            // Remove active class from all
            tabBtns.forEach(b => b.classList.remove('active'));
            tabPanels.forEach(p => p.classList.remove('active'));

            // Add active class to clicked
            btn.classList.add('active');
            document.querySelector(`[data-panel="${tabName}"]`).classList.add('active');
        });
    });
}

// ===== FORMAT TEXT =====
function formatText(text) {
    if (!text) return '';

    // Convert markdown-style formatting to HTML
    return text
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.*?)\*/g, '<em>$1</em>')
        .replace(/\n\n/g, '</p><p>')
        .replace(/\n/g, '<br>')
        .replace(/^(.+)$/, '<p>$1</p>');
}

// ===== CLOSE RESULTS =====
function closeResults() {
    const resultsModal = document.querySelector('.results-modal');
    if (resultsModal) {
        resultsModal.remove();
    }
}

// ===== DOWNLOAD REPORT =====
function downloadReport() {
    if (!window.currentReport) return;

    const report = window.currentReport;
    const reportText = `
STARTUP FEASIBILITY REPORT
Generated: ${new Date().toLocaleDateString()}

IDEA: ${report.idea}

SUCCESS PROBABILITY: ${report.report.success_probability}%
BEST LOCATION: ${report.report.best_location}

=== MARKET ANALYSIS ===
${report.report.market_analysis}

=== TARGET AUDIENCE ===
${report.report.target_audience}

=== REVENUE MODEL ===
${report.report.revenue_model}

=== COMPETITION ANALYSIS ===
${report.report.competition_analysis}

=== COST STRUCTURE ===
${report.report.cost_structure}

=== GO-TO-MARKET STRATEGY ===
${report.report.go_to_market}

${report.critique ? `=== EXPERT CRITIQUE ===\n${report.critique}` : ''}
    `.trim();

    // Create blob and download
    const blob = new Blob([reportText], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `feasibility-report-${Date.now()}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);

    showNotification('Report downloaded successfully!', 'success');
}

// ===== NOTIFICATIONS =====
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.innerHTML = `
        <div class="notification-content glass-card">
            <span>${message}</span>
            <button onclick="this.parentElement.parentElement.remove()">×</button>
        </div>
    `;

    document.body.appendChild(notification);

    // Auto remove after 5 seconds
    setTimeout(() => {
        notification.remove();
    }, 5000);
}

// ===== INTERSECTION OBSERVER FOR ANIMATIONS =====
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -100px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('animate-in');
        }
    });
}, observerOptions);

// Observe all feature cards and step cards
document.querySelectorAll('.feature-card, .step-card').forEach(el => {
    observer.observe(el);
});

// ===== DEMO VIDEO MODAL =====
const demoLinks = document.querySelectorAll('a[href="#demo"]');
demoLinks.forEach(link => {
    link.addEventListener('click', (e) => {
        e.preventDefault();
        showNotification('Demo video coming soon!', 'info');
    });
});

// ===== CONSOLE EASTER EGG =====
console.log('%c🚀 Feasibility AI', 'font-size: 24px; font-weight: bold; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;');
console.log('%cBuilt with ❤️ using AI-powered multi-agent architecture', 'font-size: 14px; color: #667eea;');
console.log('%cInterested in the tech stack? Check out our GitHub!', 'font-size: 12px; color: #a0aec0;');

// ===== INITIALIZE =====
document.addEventListener('DOMContentLoaded', () => {
    console.log('Feasibility AI initialized');

    // Add any initialization code here
    // For example, check if API is available
    checkAPIStatus();
});

// ===== CHECK API STATUS =====
async function checkAPIStatus() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`, {
            method: 'GET',
        });

        if (response.ok) {
            console.log('✅ API is online');
        } else {
            console.warn('⚠️ API returned non-OK status');
        }
    } catch (error) {
        console.warn('⚠️ API is offline. Make sure the backend is running.');
        console.log('Run: uvicorn main:app --reload');
    }
}
