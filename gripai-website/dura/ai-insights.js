/**
 * Dura AI Insights Component
 * Fetches AI insights from backend and renders them on all pages.
 * Include this script on every page.
 */
(function() {
    const API_BASE = window.DURA_API_BASE;
    const API_HEADERS = window.DURA_API_HEADERS;

    // Geen API credentials? Dan is auth.js niet geladen — skip AI insights
    if (!API_BASE || !API_HEADERS) return;

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
    
    // Type-to-color mapping for insight bullets
    const TYPE_COLORS = {
        warning: { dot: '#f59e0b', bg: '#fffbeb' },
        success: { dot: '#22c55e', bg: '#f0fdf4' },
        info:    { dot: '#2563eb', bg: '#eff6ff' }
    };

    // Create and inject the AI insight element
    function injectAIBlock() {
        const existing = document.getElementById('ai-insight-block');
        if (existing) return; // Already injected

        if (isDashboard) {
            // Dashboard: update existing ai-briefing block
            return;
        }

        // Other pages: inject 🤖 block after nav/header
        const main = document.querySelector('main') || document.querySelector('.main');
        if (!main) return;

        const block = document.createElement('div');
        block.id = 'ai-insight-block';
        block.style.cssText = `
            background: linear-gradient(135deg, #eff6ff 0%, #f0f4ff 100%);
            border: 1px solid rgba(37, 99, 235, 0.1);
            border-radius: 14px; padding: 16px 20px;
            margin-bottom: 20px; transition: opacity 0.3s;
        `;

        // Header row with icon + title + time
        const header = document.createElement('div');
        header.style.cssText = 'display:flex;align-items:center;gap:10px;margin-bottom:8px;';
        const icon = document.createElement('div');
        icon.style.cssText = 'width:32px;height:32px;background:#2563eb;border-radius:8px;display:flex;align-items:center;justify-content:center;flex-shrink:0;';
        const iconEmoji = document.createElement('span');
        iconEmoji.style.fontSize = '16px';
        iconEmoji.textContent = '\uD83E\uDD16';
        icon.appendChild(iconEmoji);
        header.appendChild(icon);
        const label = document.createElement('span');
        label.style.cssText = 'font-size:11px;font-weight:600;color:#2563eb;text-transform:uppercase;letter-spacing:0.5px;';
        label.textContent = 'AI Insights';
        header.appendChild(label);
        const timeSpan = document.createElement('span');
        timeSpan.id = 'ai-insight-time';
        timeSpan.style.cssText = 'font-size:11px;color:#6b7084;margin-left:auto;';
        header.appendChild(timeSpan);
        block.appendChild(header);

        // Items container
        const items = document.createElement('div');
        items.id = 'ai-insight-items';
        items.style.cssText = 'display:flex;flex-direction:column;gap:6px;';
        const loading = document.createElement('p');
        loading.style.cssText = 'font-size:14px;color:#6b7084;margin:0;';
        loading.textContent = 'AI-inzichten worden geladen...';
        items.appendChild(loading);
        block.appendChild(items);

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
        if (text) text.textContent = insights.summary || '';
        if (time) time.textContent = `Gegenereerd om ${formatTime(data.generated_at)}`;
        
        if (actions && insights.actions && insights.actions.length > 0) {
            actions.textContent = '';
            insights.actions.forEach(a => {
                const cls = a.type === 'warning' ? 'warning' : a.type === 'success' ? 'info' : 'info';
                const span = document.createElement('span');
                span.className = 'ai-action ' + cls;
                span.textContent = a.text;
                actions.appendChild(span);
            });
        }
    }
    
    function updatePageInsight(data) {
        const insights = data.insights;
        if (!insights || !insights.page_insights) return;

        const pageData = insights.page_insights[currentPage];
        if (!pageData) return;

        const container = document.getElementById('ai-insight-items');
        const timeEl = document.getElementById('ai-insight-time');
        if (timeEl) timeEl.textContent = formatTime(data.generated_at);
        if (!container) return;

        container.textContent = '';

        // Normalize: backend can send string, array of strings, or object with items[]
        let items = [];
        if (typeof pageData === 'string') {
            items = [{ type: 'info', text: pageData }];
        } else if (Array.isArray(pageData)) {
            items = pageData.map(function(item) {
                return typeof item === 'string' ? { type: 'info', text: item } : item;
            });
        } else if (pageData.items && Array.isArray(pageData.items)) {
            items = pageData.items;
        } else if (pageData.text) {
            items = [{ type: pageData.type || 'info', text: pageData.text }];
        }

        if (items.length === 0) return;

        items.forEach(function(item) {
            const row = document.createElement('div');
            row.style.cssText = 'display:flex;align-items:flex-start;gap:8px;padding:6px 8px;border-radius:8px;';
            const colors = TYPE_COLORS[item.type] || TYPE_COLORS.info;
            row.style.background = colors.bg;

            const dot = document.createElement('span');
            dot.style.cssText = 'width:8px;height:8px;border-radius:50%;flex-shrink:0;margin-top:5px;';
            dot.style.background = colors.dot;
            row.appendChild(dot);

            const text = document.createElement('span');
            text.style.cssText = 'font-size:13px;color:#0f1117;line-height:1.5;';
            text.textContent = item.text || '';
            row.appendChild(text);

            container.appendChild(row);
        });
    }
    
    async function fetchAndRender() {
        try {
            const res = await fetch(`${API_BASE}/api/ai-insights`, { headers: API_HEADERS });
            if (!res.ok) return;
            const json = await res.json();
            const data = json.data;
            
            if (data.status === 'pending') {
                // Show friendly pending message
                const nextGen = data.next_generation_at;
                let timeStr = '';
                if (nextGen) {
                    const d = new Date(nextGen);
                    timeStr = ` om ${d.toLocaleTimeString('nl-NL', { hour: '2-digit', minute: '2-digit' })}`;
                }
                const pendingMsg = `AI briefing wordt${timeStr} gegenereerd...`;
                const itemsContainer = document.getElementById('ai-insight-items');
                const briefText = document.querySelector('.ai-briefing-text');
                if (itemsContainer) {
                    itemsContainer.textContent = '';
                    const p = document.createElement('p');
                    p.style.cssText = 'font-size:14px;color:#6b7084;margin:0;';
                    p.textContent = pendingMsg;
                    itemsContainer.appendChild(p);
                }
                if (briefText) briefText.textContent = pendingMsg;
                return;
            }
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
    
    // Refresh every 5 minutes
    setInterval(fetchAndRender, 300000);
})();
