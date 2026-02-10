/**
 * Dura AI Insights Component
 * Fetches AI insights from backend and renders them on all pages.
 * Include this script on every page.
 */
(function() {
    const API_BASE = 'https://dura-backend-production.up.railway.app';
    
    // Detect current page
    const path = window.location.pathname;
    const isDashboard = path.endsWith('/') || path.endsWith('index.html');
    const currentPage = isDashboard ? 'dashboard' 
        : path.includes('orders') ? 'orders'
        : path.includes('voorraad') ? 'voorraad'
        : path.includes('verzendingen') ? 'verzendingen'
        : path.includes('rapportages') ? 'rapportages'
        : path.includes('warehouse') ? 'warehouse'
        : 'other';
    
    // Create and inject the AI insight element
    function injectAIBlock() {
        const existing = document.getElementById('ai-insight-block');
        if (existing) return; // Already injected
        
        if (isDashboard) {
            // Dashboard: update existing ai-briefing block
            return;
        }
        
        // Other pages: inject small 🤖 block after nav/header
        const main = document.querySelector('main') || document.querySelector('.main');
        if (!main) return;
        
        const block = document.createElement('div');
        block.id = 'ai-insight-block';
        block.style.cssText = `
            display: flex; align-items: center; gap: 14px;
            background: linear-gradient(135deg, #eff6ff 0%, #f0f4ff 100%);
            border: 1px solid rgba(37, 99, 235, 0.1);
            border-radius: 14px; padding: 16px 20px;
            margin-bottom: 20px; transition: opacity 0.3s;
        `;
        block.innerHTML = `
            <div style="width:36px;height:36px;background:#2563eb;border-radius:10px;display:flex;align-items:center;justify-content:center;flex-shrink:0;">
                <span style="font-size:18px;">🤖</span>
            </div>
            <div style="flex:1;min-width:0;">
                <div style="display:flex;align-items:center;gap:8px;margin-bottom:2px;">
                    <span style="font-size:11px;font-weight:600;color:#2563eb;text-transform:uppercase;letter-spacing:0.5px;">AI Insight</span>
                    <span id="ai-insight-time" style="font-size:11px;color:#6b7084;"></span>
                </div>
                <p id="ai-insight-text" style="font-size:14px;color:#0f1117;line-height:1.5;margin:0;">
                    AI-inzicht wordt geladen...
                </p>
            </div>
        `;
        
        // Insert as first child of main content
        const firstChild = main.querySelector('.header') || main.firstElementChild;
        if (firstChild && firstChild.nextSibling) {
            main.insertBefore(block, firstChild.nextSibling);
        } else {
            main.prepend(block);
        }
    }
    
    function formatTime(isoStr) {
        if (!isoStr) return '';
        const d = new Date(isoStr);
        return d.toLocaleTimeString('nl-NL', { hour: '2-digit', minute: '2-digit' });
    }
    
    function updateDashboardBriefing(data) {
        const insights = data.insights;
        if (!insights) return;
        
        const title = document.querySelector('.ai-briefing-title');
        const text = document.querySelector('.ai-briefing-text');
        const time = document.querySelector('.ai-briefing-time');
        const actions = document.querySelector('.ai-briefing-actions');
        
        if (title) title.textContent = insights.title || 'AI Briefing';
        if (text) text.innerHTML = insights.summary || '';
        if (time) time.textContent = `Gegenereerd om ${formatTime(data.generated_at)}`;
        
        if (actions && insights.actions && insights.actions.length > 0) {
            actions.innerHTML = insights.actions.map(a => {
                const cls = a.type === 'warning' ? 'warning' : a.type === 'success' ? 'info' : 'info';
                return `<span class="ai-action ${cls}">${a.text}</span>`;
            }).join('');
        }
    }
    
    function updatePageInsight(data) {
        const insights = data.insights;
        if (!insights || !insights.page_insights) return;
        
        const pageText = insights.page_insights[currentPage];
        if (!pageText) return;
        
        const textEl = document.getElementById('ai-insight-text');
        const timeEl = document.getElementById('ai-insight-time');
        
        if (textEl) textEl.textContent = pageText;
        if (timeEl) timeEl.textContent = formatTime(data.generated_at);
    }
    
    async function fetchAndRender() {
        try {
            const res = await fetch(`${API_BASE}/api/ai-insights`);
            if (!res.ok) return;
            const json = await res.json();
            const data = json.data;
            
            if (data.status !== 'ok') return;
            
            if (isDashboard) {
                updateDashboardBriefing(data);
            } else {
                updatePageInsight(data);
            }
        } catch (e) {
            console.log('AI Insights niet beschikbaar:', e.message);
        }
    }
    
    // Init
    if (!isDashboard) {
        injectAIBlock();
    }
    
    // Fetch on load
    fetchAndRender();
    
    // Refresh every 60 seconds
    setInterval(fetchAndRender, 60000);
})();
