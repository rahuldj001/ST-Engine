// ===== CONFIGURATION =====
const API_BASE_URL = 'http://localhost:8000';

// ===== NAVBAR SCROLL EFFECT =====
const navbar = document.querySelector('.navbar');
window.addEventListener('scroll', () => {
    const currentScroll = window.pageYOffset;
    if (navbar) {
        navbar.classList.toggle('scrolled', currentScroll > 100);
    }
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
            window.scrollTo({ top: offsetTop, behavior: 'smooth' });
            if (navLinks?.classList.contains('active')) {
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

        const formData = {
            idea: document.getElementById('idea').value.trim(),
            industry: document.getElementById('industry').value.trim() || 'general',
            target_market: document.getElementById('market').value.trim() || 'global'
        };

        if (!formData.idea) {
            showNotification('Please describe your startup idea', 'error');
            return;
        }

        showLoadingModal();

        try {
            const response = await fetch(`${API_BASE_URL}/api/analyze`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData)
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const result = await response.json();
            hideLoadingModal();
            displayResults(result);
            ideaForm.reset();
        } catch (error) {
            console.error('Error:', error);
            hideLoadingModal();
            showNotification('Failed to analyze idea. Please try again.', 'error');
        }
    });
}

function showLoadingModal() {
    if (!loadingModal) return;
    loadingModal.classList.add('active');
    document.body.style.overflow = 'hidden';

    const steps = document.querySelectorAll('.progress-step');
    steps.forEach((step, index) => {
        setTimeout(() => step.classList.add('active'), index * 1000);
    });
}

function hideLoadingModal() {
    if (!loadingModal) return;
    loadingModal.classList.remove('active');
    document.body.style.overflow = '';

    const steps = document.querySelectorAll('.progress-step');
    steps.forEach(step => step.classList.remove('active'));
}

// ===== DASHBOARD RENDERING =====
function displayResults(data) {
    closeResults();

    const report = data.report || {};
    const metrics = data.evaluation_metrics || {};

    const successProbability = Number(report.success_probability || 0);
    const confidenceScore = toPercent(metrics.overall_confidence);
    const hallucinationRisk = getHallucinationRisk(data);
    const totalTokens = metrics.total_tokens || estimateTokensFromText([
        report.market_analysis,
        report.target_audience,
        report.revenue_model,
        report.competition_analysis,
        report.cost_structure,
        report.go_to_market,
        data.critique
    ].join('\n'));

    const revenueCost = buildRevenueCostData(report.revenue_model, report.cost_structure);
    const costBreakdown = buildCostBreakdown(report.cost_structure);
    const gtmTimeline = buildTimeline(report.go_to_market);
    const marketDataPoints = extractDataPoints([report.market_analysis, report.target_audience, report.competition_analysis].join('\n'));
    const financialDataPoints = extractDataPoints([report.revenue_model, report.cost_structure].join('\n'));
    const gtmDataPoints = extractDataPoints(report.go_to_market);
    const riskDataPoints = extractDataPoints([data.critique, JSON.stringify(data.hallucination_report || {}, null, 2)].join('\n'));

    const resultsHTML = `
        <div class="results-modal modal active">
            <div class="results-content dashboard-shell glass-card">
                <button class="close-btn" onclick="closeResults()" aria-label="Close results">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                        <path d="M18 6L6 18M6 6L18 18" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                    </svg>
                </button>

                <header class="dashboard-header">
                    <div>
                        <p class="dashboard-kicker">Startup Feasibility Dashboard</p>
                        <h2>${escapeHtml(trimIdea(data.idea))}</h2>
                    </div>
                    <div class="probability-badge ${riskClassFromProbability(successProbability)}">
                        <span>Success Probability</span>
                        <strong>${successProbability.toFixed(1)}%</strong>
                    </div>
                </header>

                <section class="kpi-grid">
                    ${kpiCard('Success Probability', `${successProbability.toFixed(1)}%`, 'Positive Outlook', 'success')}
                    ${kpiCard('Hallucination Risk', hallucinationRisk.label, 'Model Reliability', riskColorFromLabel(hallucinationRisk.label))}
                    ${kpiCard('Confidence Score', `${confidenceScore}%`, 'Cross-agent confidence', confidenceScore >= 70 ? 'success' : 'warning')}
                    ${kpiCard('Token Usage', `${Number(totalTokens).toLocaleString()}`, 'Total pipeline tokens', 'neutral')}
                </section>

                <nav class="dashboard-tabs" id="dashboardTabs">
                    ${tabButton('overview', 'Overview', true)}
                    ${tabButton('market', 'Market Intelligence')}
                    ${tabButton('financial', 'Financial Strategy')}
                    ${tabButton('gtm', 'GTM Plan')}
                    ${tabButton('risk', 'Risk & Evaluation')}
                </nav>

                <section class="dashboard-panels">
                    <div class="dash-panel active" data-panel="overview">
                        <div class="overview-grid">
                            <article class="card">
                                <h3>Success Gauge</h3>
                                <div class="gauge-wrap">
                                    <div class="gauge" style="--value:${Math.max(0, Math.min(100, successProbability))}">
                                        <div class="gauge-center">
                                            <strong>${successProbability.toFixed(1)}%</strong>
                                            <span>Feasibility</span>
                                        </div>
                                    </div>
                                </div>
                                ${highlightBox('Best Location', report.best_location || 'Not specified')}
                            </article>
                            <article class="card">
                                <h3>Revenue vs Cost (Projected)</h3>
                                ${renderBarChart(revenueCost)}
                            </article>
                            <article class="card">
                                <h3>Cost Breakdown</h3>
                                ${renderCostBreakdown(costBreakdown)}
                            </article>
                            <article class="card">
                                <h3>Key Highlights</h3>
                                ${bulletList(extractBullets([report.market_analysis, report.revenue_model, report.go_to_market].join('\n')).slice(0, 8))}
                            </article>
                        </div>
                    </div>

                    <div class="dash-panel" data-panel="market">
                        <div class="two-col">
                            <div class="card">
                                <h3>Market Demand Snapshot</h3>
                                ${sectionBody(report.market_analysis)}
                            </div>
                            <div class="card">
                                <h3>Extracted Market Data</h3>
                                ${renderDataPointGrid(marketDataPoints)}
                            </div>
                        </div>
                        ${accordion('Audience Profile', report.target_audience, true)}
                        ${accordion('Competition Landscape', report.competition_analysis)}
                        ${rawTextDetails('Complete Market Intelligence Output', [report.market_analysis, report.target_audience, report.competition_analysis].join('\n\n'))}
                    </div>

                    <div class="dash-panel" data-panel="financial">
                        <div class="two-col">
                            <div class="card">${sectionCard('Revenue Model Summary', report.revenue_model)}</div>
                            <div class="card">${sectionCard('Cost Structure Summary', report.cost_structure)}</div>
                        </div>
                        <div class="card mt-16">
                            <h3>Extracted Financial Data</h3>
                            ${renderDataPointGrid(financialDataPoints)}
                        </div>
                        <div class="card mt-16">${alertBox('Financial Risks', extractRiskLines([report.revenue_model, report.cost_structure].join('\n')))}</div>
                        ${rawTextDetails('Complete Financial Strategy Output', [report.revenue_model, report.cost_structure].join('\n\n'))}
                    </div>

                    <div class="dash-panel" data-panel="gtm">
                        <div class="card">
                            <h3>Timeline Roadmap</h3>
                            ${renderTimeline(gtmTimeline)}
                        </div>
                        <div class="card mt-16">
                            <h3>Extracted GTM Data</h3>
                            ${renderDataPointGrid(gtmDataPoints)}
                        </div>
                        <div class="card mt-16">${sectionCard('Detailed GTM Notes', report.go_to_market)}</div>
                        ${rawTextDetails('Complete GTM Output', report.go_to_market)}
                    </div>

                    <div class="dash-panel" data-panel="risk">
                        <div class="two-col">
                            <div class="card">
                                <h3>Critique & Consistency</h3>
                                ${sectionBody(data.critique || 'No critique returned by backend.')}
                            </div>
                            <div class="card">
                                <h3>Risk Indicator</h3>
                                <div class="risk-indicator ${riskColorFromLabel(hallucinationRisk.label)}">
                                    <span>${hallucinationRisk.label}</span>
                                </div>
                                <div class="mini-kpis">
                                    <div><label>Overall Confidence</label><strong>${confidenceScore}%</strong></div>
                                    <div><label>Total Tokens</label><strong>${Number(totalTokens).toLocaleString()}</strong></div>
                                    <div><label>Sources Used</label><strong>${(data.sources_used || []).length}</strong></div>
                                    <div><label>Similar Ideas</label><strong>${(data.similar_ideas || []).length}</strong></div>
                                </div>
                            </div>
                        </div>
                        <div class="card mt-16">
                            <h3>Validation Data Points</h3>
                            ${renderDataPointGrid(riskDataPoints)}
                        </div>
                        <div class="two-col mt-16">
                            <div class="card">
                                <h3>Retrieved Similar Ideas</h3>
                                ${bulletList((data.similar_ideas || []).map((idea, idx) => `${idx + 1}. ${idea}`))}
                            </div>
                            <div class="card">
                                <h3>Sources Used</h3>
                                ${bulletList((data.sources_used || []).map((source, idx) => `${idx + 1}. ${source}`))}
                            </div>
                        </div>
                        ${rawTextDetails('Raw Hallucination Report', JSON.stringify(data.hallucination_report || {}, null, 2))}
                    </div>
                </section>

                <div class="results-actions">
                    <button class="btn btn-primary" onclick="downloadReport()">Download Report</button>
                    <button class="btn btn-secondary" onclick="closeResults()">Analyze Another Idea</button>
                </div>
            </div>
        </div>
    `;

    document.body.insertAdjacentHTML('beforeend', resultsHTML);
    setupDashboardTabs();
    window.currentReport = data;
}

function setupDashboardTabs() {
    const tabBtns = document.querySelectorAll('.dashboard-tab-btn');
    const panels = document.querySelectorAll('.dash-panel');

    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const name = btn.dataset.tab;
            tabBtns.forEach(b => b.classList.remove('active'));
            panels.forEach(p => p.classList.remove('active'));
            btn.classList.add('active');
            document.querySelector(`.dash-panel[data-panel="${name}"]`)?.classList.add('active');
        });
    });
}

// ===== COMPONENT HELPERS =====
function tabButton(key, label, active = false) {
    return `<button class="dashboard-tab-btn ${active ? 'active' : ''}" data-tab="${key}">${label}</button>`;
}

function kpiCard(label, value, hint, tone = 'neutral') {
    return `<article class="kpi-card ${tone}"><p>${label}</p><h3>${escapeHtml(String(value))}</h3><span>${escapeHtml(hint)}</span></article>`;
}

function sectionCard(title, text) {
    return `<h3>${escapeHtml(title)}</h3>${sectionBody(text)}`;
}

function sectionBody(text) {
    return `<div class="section-body">${bulletList(extractBullets(text))}</div>`;
}

function accordion(title, text, open = false) {
    return `
        <details class="accordion" ${open ? 'open' : ''}>
            <summary>${escapeHtml(title)}</summary>
            <div class="accordion-body">
                ${sectionBody(text)}
                ${alertBox('Signals to Watch', extractRiskLines(text))}
            </div>
        </details>
    `;
}

function highlightBox(label, value) {
    return `<div class="highlight"><span>${escapeHtml(label)}</span><strong>${escapeHtml(value || 'N/A')}</strong></div>`;
}

function alertBox(title, lines) {
    const items = lines.length ? lines : ['No explicit risks identified; validate assumptions with live market tests.'];
    return `
        <div class="alert-box">
            <h4>${escapeHtml(title)}</h4>
            ${bulletList(items)}
        </div>
    `;
}

function renderBarChart(data) {
    const maxValue = Math.max(...data.map(d => d.value), 1);
    const bars = data.map(item => {
        const height = Math.max(8, (item.value / maxValue) * 180);
        return `
            <div class="bar-col">
                <div class="bar ${item.type}" style="height:${height}px"></div>
                <strong>$${Math.round(item.value).toLocaleString()}k</strong>
                <span>${item.label}</span>
            </div>
        `;
    }).join('');

    return `<div class="bar-chart">${bars}</div>`;
}

function renderCostBreakdown(breakdown) {
    const gradient = breakdown
        .map((slice, i, arr) => {
            const start = arr.slice(0, i).reduce((acc, cur) => acc + cur.percent, 0);
            const end = start + slice.percent;
            return `${slice.color} ${start}% ${end}%`;
        })
        .join(', ');

    const legend = breakdown
        .map(item => `<li><span style="background:${item.color}"></span>${escapeHtml(item.label)} <strong>${item.percent}%</strong></li>`)
        .join('');

    return `
        <div class="pie-wrap">
            <div class="pie" style="background: conic-gradient(${gradient});"></div>
            <ul class="pie-legend">${legend}</ul>
        </div>
    `;
}

function renderTimeline(items) {
    const mapped = items.map((item, i) => `
        <div class="timeline-item">
            <div class="timeline-dot">${i + 1}</div>
            <div class="timeline-content">
                <h4>${escapeHtml(item.phase)}</h4>
                ${bulletList(item.points)}
            </div>
        </div>
    `).join('');

    return `<div class="timeline">${mapped}</div>`;
}

function bulletList(lines) {
    const content = (lines || []).filter(Boolean).slice(0, 12);
    if (!content.length) return '<p class="muted">No structured output available.</p>';
    return `<ul class="bullets">${content.map(line => `<li>${escapeHtml(line)}</li>`).join('')}</ul>`;
}

function renderDataPointGrid(points) {
    const items = (points || []).slice(0, 24);
    if (!items.length) {
        return '<p class="muted">No explicit numeric or key-value data found. Run with more structured assumptions to extract richer signals.</p>';
    }

    return `<div class="data-grid">${items.map(item => `
        <article class="data-point">
            <p>${escapeHtml(item.label)}</p>
            <strong>${escapeHtml(item.value)}</strong>
        </article>
    `).join('')}</div>`;
}

function rawTextDetails(title, text) {
    return `
        <details class="accordion mt-16">
            <summary>${escapeHtml(title)}</summary>
            <div class="accordion-body">
                <pre class="raw-output">${escapeHtml(text || 'No raw output available.')}</pre>
            </div>
        </details>
    `;
}

// ===== DATA UTILITIES =====
function extractBullets(text) {
    if (!text) return [];
    return text
        .split(/\n+/)
        .map(line => line.replace(/^[-*\d.\s]+/, '').trim())
        .filter(line => line.length > 10)
        .slice(0, 14);
}

function extractRiskLines(text) {
    const candidates = extractBullets(text);
    const riskTerms = /(risk|threat|challenge|barrier|competition|cost|burn|uncertain|constraint|assumption)/i;
    const hits = candidates.filter(line => riskTerms.test(line));
    return (hits.length ? hits : candidates).slice(0, 5);
}

function extractDataPoints(text) {
    if (!text) return [];

    const lines = text.split(/\n+/).map(line => line.trim()).filter(Boolean);
    const points = [];

    lines.forEach(line => {
        const clean = line.replace(/^[-*\d.\s]+/, '').trim();
        if (!clean) return;

        const kvMatch = clean.match(/^([^:]{2,60}):\s*(.+)$/);
        if (kvMatch) {
            points.push({ label: kvMatch[1], value: kvMatch[2] });
            return;
        }

        const percentMatch = clean.match(/([\w\s]{3,50})\b(\d+(?:\.\d+)?)%/);
        if (percentMatch) {
            points.push({ label: percentMatch[1].trim(), value: `${percentMatch[2]}%` });
            return;
        }

        const moneyMatch = clean.match(/([\w\s]{3,50})\s(\$?[\d,.]+\s?[kKmMbB]?)/);
        if (moneyMatch) {
            points.push({ label: moneyMatch[1].trim(), value: moneyMatch[2].trim() });
        }
    });

    const deduped = [];
    const seen = new Set();
    points.forEach(point => {
        const key = `${point.label.toLowerCase()}|${point.value.toLowerCase()}`;
        if (seen.has(key)) return;
        seen.add(key);
        deduped.push(point);
    });

    return deduped;
}

function estimateTokensFromText(text) {
    return Math.round((text || '').length / 4);
}

function toPercent(value) {
    if (value === null || value === undefined || Number.isNaN(Number(value))) return 0;
    const numeric = Number(value);
    return numeric <= 1 ? Math.round(numeric * 100) : Math.round(numeric);
}

function getHallucinationRisk(data) {
    const risk =
        data?.hallucination_report?.risk_level ||
        data?.hallucination_report?.overall_risk ||
        data?.evaluation_metrics?.hallucination_risk ||
        'MEDIUM';
    const label = String(risk).toUpperCase();
    return { label };
}

function riskClassFromProbability(prob) {
    if (prob >= 70) return 'good';
    if (prob >= 45) return 'medium';
    return 'high';
}

function riskColorFromLabel(label) {
    const normalized = String(label || '').toUpperCase();
    if (normalized.includes('LOW')) return 'success';
    if (normalized.includes('MED')) return 'warning';
    return 'danger';
}

function buildRevenueCostData(revenueText, costText) {
    const revenue = extractFirstMoneyNumber(revenueText) || 180;
    const cost = extractFirstMoneyNumber(costText) || 120;

    return [
        { label: 'Revenue', value: revenue, type: 'revenue' },
        { label: 'Cost', value: cost, type: 'cost' }
    ];
}

function extractFirstMoneyNumber(text) {
    if (!text) return null;
    const withK = text.match(/\$?([\d,.]+)\s?k/i);
    if (withK) return Number(withK[1].replace(/,/g, ''));

    const withM = text.match(/\$?([\d,.]+)\s?m/i);
    if (withM) return Number(withM[1].replace(/,/g, '')) * 1000;

    const plain = text.match(/\$([\d,.]+)/);
    if (plain) return Number(plain[1].replace(/,/g, '')) / 1000;

    return null;
}

function buildCostBreakdown(costText) {
    const text = (costText || '').toLowerCase();
    const buckets = [
        { label: 'Operations', key: /(infra|hosting|ops|operations|server|cloud)/, base: 30, color: '#22c55e' },
        { label: 'Team', key: /(salary|team|engineering|staff|hiring|payroll)/, base: 35, color: '#eab308' },
        { label: 'Marketing', key: /(marketing|acquisition|ads|growth|sales)/, base: 20, color: '#ef4444' },
        { label: 'Other', key: /(legal|admin|compliance|misc)/, base: 15, color: '#6366f1' }
    ];

    let total = 0;
    const weighted = buckets.map(bucket => {
        const weight = bucket.base + (bucket.key.test(text) ? 5 : 0);
        total += weight;
        return { ...bucket, weight };
    });

    return weighted.map((w, index) => ({
        label: w.label,
        percent: index === weighted.length - 1
            ? 100 - weighted.slice(0, -1).reduce((acc, cur) => acc + Math.round((cur.weight / total) * 100), 0)
            : Math.round((w.weight / total) * 100),
        color: w.color
    }));
}

function buildTimeline(gtmText) {
    const bullets = extractBullets(gtmText);
    const defaults = [
        { phase: '0-3 Months', points: bullets.slice(0, 3) },
        { phase: '3-12 Months', points: bullets.slice(3, 6) },
        { phase: '12-24 Months', points: bullets.slice(6, 9) }
    ];

    return defaults.map(d => ({
        ...d,
        points: d.points.length ? d.points : ['Define milestones and owner accountability for this phase.']
    }));
}

function trimIdea(idea) {
    if (!idea) return 'Untitled Startup Idea';
    return idea.length > 80 ? `${idea.slice(0, 80)}...` : idea;
}

function escapeHtml(value) {
    return String(value || '')
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#39;');
}

// ===== CLOSE RESULTS =====
function closeResults() {
    const resultsModal = document.querySelector('.results-modal');
    if (resultsModal) {
        resultsModal.remove();
        document.body.style.overflow = '';
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
            <span>${escapeHtml(message)}</span>
            <button onclick="this.parentElement.parentElement.remove()">×</button>
        </div>
    `;

    document.body.appendChild(notification);
    setTimeout(() => notification.remove(), 5000);
}

// ===== INTERSECTION OBSERVER =====
const observerOptions = { threshold: 0.1, rootMargin: '0px 0px -100px 0px' };
const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) entry.target.classList.add('animate-in');
    });
}, observerOptions);

document.querySelectorAll('.feature-card, .step-card').forEach(el => observer.observe(el));

// ===== DEMO VIDEO MODAL =====
document.querySelectorAll('a[href="#demo"]').forEach(link => {
    link.addEventListener('click', (e) => {
        e.preventDefault();
        showNotification('Demo video coming soon!', 'info');
    });
});

console.log('%c🚀 Feasibility AI', 'font-size: 24px; font-weight: bold; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;');

// ===== INITIALIZE =====
document.addEventListener('DOMContentLoaded', () => {
    checkAPIStatus();
});

async function checkAPIStatus() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`, { method: 'GET' });
        if (response.ok) {
            console.log('✅ API is online');
        } else {
            console.warn('⚠️ API returned non-OK status');
        }
    } catch (error) {
        console.warn('⚠️ API is offline. Make sure the backend is running.');
    }
}
