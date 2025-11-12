        alert('Kunde inte generera prompt: ' + error.message);
    } finally {
        hideLoading();
    }
}

function showAgentPromptDialog(agentData) {
    const modal = document.getElementById('customer-modal');
    const details = document.getElementById('customer-details');

    details.innerHTML = `
        <h2>🤖 AI-Agent för ${agentData.customer_name}</h2>
        <p style="color: var(--text-light); margin-bottom: 20px;">
            ${agentData.links_to_process} länkar - ${agentData.needs_target} behöver målsida, ${agentData.needs_anchor} behöver ankartext
        </p>
        
        <div style="margin: 20px 0;">
            <button onclick="copyAgentPrompt()" class="btn-primary">📋 Kopiera Prompt</button>
            <button onclick="downloadAgentPrompt()" class="btn-secondary">💾 Ladda ner som TXT</button>
        </div>
        
        <div style="background: var(--light); padding: 20px; border-radius: 12px; max-height: 500px; overflow-y: auto;">
            <pre id="agent-prompt-content" style="white-space: pre-wrap; font-size: 0.85em; line-height: 1.6;">${agentData.prompt}</pre>
        </div>
        
        <textarea id="agent-prompt-hidden" style="display: none;">${agentData.prompt}</textarea>
        
        <div style="display: flex; gap: 10px; justify-content: flex-end; margin-top: 20px;">
            <button onclick="loadNovemberPlan(); closeModal();" class="btn-secondary">← Tillbaka till översikt</button>
            <button onclick="closeModal()" class="btn-primary">Stäng</button>
        </div>
    `;
}

function copyAgentPrompt() {
    const textarea = document.getElementById('agent-prompt-hidden');
    if (textarea) {
        textarea.style.display = 'block';
        textarea.select();
        document.execCommand('copy');
        textarea.style.display = 'none';
        alert('✅ AI-Agent prompt kopierad! Klistra in i ChatGPT/Claude för att komplettera länkarna.');
    }
}

function downloadAgentPrompt() {
    const content = document.getElementById('agent-prompt-hidden').value;
    const blob = new Blob([content], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'ai-agent-prompt.txt';
    a.click();
    URL.revokeObjectURL(url);
}

function generateAllAgentPrompts() {
    alert('Funktionalitet kommer snart: Generera och exportera alla AI-prompts samtidigt!');
}

// Load Preflight from Google Sheets (OLD - KEPT FOR BACKWARDS COMPAT)
        document.getElementById('mainsheet-total').textContent = data.total.toLocaleString();
        document.getElementById('mainsheet-shown').textContent = data.showing;
        document.getElementById('mainsheet-unique-customers').textContent = data.unique_customers;
        
        // Rendera tabell
        const tbody = document.getElementById('mainsheet-tbody');
        tbody.innerHTML = '';
        
        if (data.records.length === 0) {
            tbody.innerHTML = '<tr><td colspan="8" style="text-align: center; padding: 20px;">Inga resultat hittades</td></tr>';
            return;
        }
        
        data.records.forEach((record) => {
            const row = document.createElement('tr');
            row.style.borderBottom = '1px solid #ddd';
            
            row.innerHTML = `
                <td style="padding: 8px; border: 1px solid #ddd;">${record.index + 1}</td>
                <td style="padding: 8px; border: 1px solid #ddd;">${record.canonical_root}</td>
                <td style="padding: 8px; border: 1px solid #ddd;">${record.brand}</td>
                <td style="padding: 8px; border: 1px solid #ddd; max-width: 200px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;" title="${record.pub_page_url}">
                    <a href="${record.pub_page_url}" target="_blank" style="color: var(--primary);">${record.pub_page_url}</a>
                </td>
                <td style="padding: 8px; border: 1px solid #ddd; max-width: 200px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;" title="${record.target_url}">
                    <a href="${record.target_url}" target="_blank" style="color: var(--primary);">${record.target_url}</a>
                </td>
                <td style="padding: 8px; border: 1px solid #ddd;">${record.anchor_text}</td>
                <td style="padding: 8px; border: 1px solid #ddd;">${record.link_type}</td>
                <td style="padding: 8px; border: 1px solid #ddd;">${record.published_at ? record.published_at.split(' ')[0] : ''}</td>
            `;
            
            tbody.appendChild(row);
        });
        
        // Uppdatera offset
        mainSheetData.offset = data.showing;
        
        // Visa "Ladda fler" om det finns mer
        if (data.has_more) {
            const loadMoreRow = document.createElement('tr');
            loadMoreRow.innerHTML = `
                <td colspan="8" style="text-align: center; padding: 20px;">
                    <button onclick="searchMainSheet()" class="btn-primary">Ladda fler (${data.filtered - mainSheetData.offset} kvar)</button>
                </td>
            `;
            tbody.appendChild(loadMoreRow);
        }
        
    } catch (error) {
        console.error('Error searching main sheet:', error);
        alert('Kunde inte söka: ' + error.message);
    } finally {
        hideLoading();
    }
}

// Link Planning GUI - JavaScript

let allCustomers = [];
let planningData = {};

// Initialize on load
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM loaded, initializing...');
    loadStats();
    loadCustomers();
});

// Tab switching
function showTab(tabName) {
    console.log('Switching to tab:', tabName);

    // Hide all tabs
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    document.querySelectorAll('.tab-button').forEach(btn => {
        btn.classList.remove('active');
    });

    // Show selected tab
    const tabElement = document.getElementById(tabName + '-tab');
    if (tabElement) {
        tabElement.classList.add('active');
    }

    // Find and activate the clicked button
    const buttons = document.querySelectorAll('.tab-button');
    buttons.forEach(btn => {
        if (btn.textContent.includes(tabName === 'customers' ? 'Kunder' :
                                      tabName === 'planning' ? 'Planering' : 'Historik')) {
            btn.classList.add('active');
        }
    });

    // Refresh customer selects when switching to planning or history
    if (tabName === 'planning' || tabName === 'history') {
        populateCustomerSelects();
    }
}

// Load stats
async function loadStats() {
    try {
        console.log('Loading stats...');
        const response = await fetch('/api/stats');
        const data = await response.json();

        console.log('Stats loaded:', data);

        document.getElementById('total-customers').textContent = data.total_customers;
        document.getElementById('total-links').textContent = data.total_links.toLocaleString();
        document.getElementById('unique-pub-domains').textContent = data.unique_pub_domains;
        document.getElementById('unique-target-domains').textContent = data.unique_target_domains;
    } catch (error) {
        console.error('Error loading stats:', error);
    }
}

// Load customers
async function loadCustomers() {
    try {
        console.log('Loading customers...');
        const response = await fetch('/api/customers');
        const data = await response.json();

        console.log('Customers loaded:', data.count);

        allCustomers = data.customers;
        renderCustomers(allCustomers);
        populateCustomerSelects();
    } catch (error) {
        console.error('Error loading customers:', error);
        document.getElementById('customers-list').innerHTML =
            '<p class="loading">Fel vid laddning av kunder</p>';
    }
}

// Render customers
function renderCustomers(customers) {
    const container = document.getElementById('customers-list');

    if (customers.length === 0) {
        container.innerHTML = '<p class="loading">Inga kunder hittades</p>';
        return;
    }

    container.innerHTML = customers.map(c => `
        <div class="customer-card" onclick="showCustomerDetails(${c.id})">
            <h3>${c.canonical_root}</h3>
            <p class="brand">${c.brand}</p>
            <div class="customer-stats">
                <span>🔗 ${c.total_links} länkar</span>
                <span>📰 ${c.unique_pub_domains} domäner</span>
            </div>
        </div>
    `).join('');
}

// Search customers
const searchInput = document.getElementById('customer-search');
if (searchInput) {
    searchInput.addEventListener('input', function(e) {
        const query = e.target.value.toLowerCase();
        const filtered = allCustomers.filter(c =>
            c.canonical_root.toLowerCase().includes(query) ||
            c.brand.toLowerCase().includes(query)
        );
        renderCustomers(filtered);
    });
}

// Show customer details
async function showCustomerDetails(customerId) {
    showLoading();

    try {
        console.log('Loading details for customer:', customerId);
        const [history, monthly] = await Promise.all([
            fetch(`/api/customer/${customerId}/history`).then(r => r.json()),
            fetch(`/api/customer/${customerId}/monthly`).then(r => r.json())
        ]);

        console.log('Customer details loaded');

        const modal = document.getElementById('customer-modal');
        const details = document.getElementById('customer-details');

        details.innerHTML = `
            <h2>${history.canonical_root}</h2>
            <p style="color: var(--text-light); margin-bottom: 20px;">${history.brand}</p>
            
            <div class="plan-summary">
                <div class="summary-card">
                    <div class="summary-value">${history.total_links}</div>
                    <div class="summary-label">Totalt länkar</div>
                </div>
                <div class="summary-card">
                    <div class="summary-value">${history.unique_pub_domains}</div>
                    <div class="summary-label">Pub-domäner</div>
                </div>
                <div class="summary-card">
                    <div class="summary-value">${history.unique_target_urls}</div>
                    <div class="summary-label">Målsidor</div>
                </div>
                <div class="summary-card">
                    <div class="summary-value">${history.links_per_month}</div>
                    <div class="summary-label">Per månad</div>
                </div>
            </div>
            
            <h3 style="margin: 20px 0 10px;">📊 Statistik</h3>
            <div style="background: var(--light); padding: 15px; border-radius: 8px; margin-bottom: 20px;">
                <p><strong>Anchor diversity:</strong> ${history.anchor_diversity_score} (0-1)</p>
                <p><strong>Primär strategi:</strong> ${history.primary_strategy}</p>
                <p><strong>Period:</strong> ${history.first_link_date || 'N/A'} - ${history.last_link_date || 'N/A'}</p>
            </div>
            
            <h3 style="margin: 20px 0 10px;">🎯 Anchor Types</h3>
            <div class="anchor-dist">
                ${Object.entries(history.anchor_types || {}).map(([type, count]) => `
                    <span class="badge badge-info">${type}: ${count}</span>
                `).join('')}
            </div>
            
            <h3 style="margin: 20px 0 10px;">📝 Vanligaste Ankartexter</h3>
            ${(history.most_common_anchors || []).slice(0, 5).map(([text, count]) => `
                <div class="link-preview">
                    <strong>"${text}"</strong> - ${count}x
                </div>
            `).join('')}
            
            <h3 style="margin: 20px 0 10px;">💡 Rekommendationer</h3>
            ${(history.recommendations || []).map(rec => `
                <div class="link-preview">${rec}</div>
            `).join('')}
            
            <h3 style="margin: 20px 0 10px;">📅 Månadshistorik (${monthly.count} månader)</h3>
            <div style="max-height: 300px; overflow-y: auto;">
                ${(monthly.months || []).slice(-6).reverse().map(m => `
                    <div class="month-card" style="margin-bottom: 10px;">
                        <strong>${m.display_name}</strong> - ${m.link_count} länkar
                    </div>
                `).join('')}
            </div>
        `;

        modal.style.display = 'block';
    } catch (error) {
        console.error('Error loading customer details:', error);
        alert('Kunde inte ladda kunddetaljer: ' + error.message);
    } finally {
        hideLoading();
    }
}

// Close modal
function closeModal() {
    document.getElementById('customer-modal').style.display = 'none';
}

// Populate customer selects
function populateCustomerSelects() {
    console.log('Populating customer selects with', allCustomers.length, 'customers');

    const selects = [
        document.getElementById('customer-select'),
        document.getElementById('history-customer-select')
    ];

    selects.forEach(select => {
        if (select) {
            const options = '<option value="">Välj kund...</option>' +
                allCustomers.map(c => `
                    <option value="${c.id}">${c.canonical_root} (${c.total_links} länkar)</option>
                `).join('');

            select.innerHTML = options;
            console.log('Populated select with', allCustomers.length, 'options');
        }
    });
}

// Add to plan
function addToPlan() {
    const select = document.getElementById('customer-select');
    const countInput = document.getElementById('link-count');
    const pubDomainInput = document.getElementById('pub-domain');
    const targetUrlInput = document.getElementById('target-url');
    const anchorTextInput = document.getElementById('anchor-text');

    if (!select || !countInput || !pubDomainInput) {
        console.error('Required inputs not found');
        return;
    }

    const customerId = select.value;
    const linkCount = parseInt(countInput.value);
    const pubDomain = pubDomainInput.value.trim();
    const targetUrl = targetUrlInput ? targetUrlInput.value.trim() : '';
    const anchorText = anchorTextInput ? anchorTextInput.value.trim() : '';

    console.log('Adding to plan:', customerId, linkCount, pubDomain, targetUrl, anchorText);

    // Validering
    if (!customerId || !linkCount || linkCount < 1) {
        alert('Välj kund och ange antal länkar');
        return;
    }

    if (!pubDomain) {
        alert('Publiceringssajt är obligatorisk!');
        pubDomainInput.focus();
        return;
    }

    // Skapa unik nyckel för varje post
    const planKey = `${customerId}_${Date.now()}`;

    planningData[planKey] = {
        customer_id: customerId,
        link_count: linkCount,
        pub_domain: pubDomain,
        target_url: targetUrl || null,
        anchor_text: anchorText || null
    };

    console.log('Planning data:', planningData);

    renderPlanItems();

    // Aktivera "Analysera"-knappen när länkar läggs till
    const analyzeBtn = document.getElementById('analyze-btn');
    if (analyzeBtn && Object.keys(planningData).length > 0) {
        analyzeBtn.disabled = false;
    }

    // Reset inputs
    select.value = '';
    countInput.value = '';
    pubDomainInput.value = '';
    if (targetUrlInput) targetUrlInput.value = '';
    if (anchorTextInput) anchorTextInput.value = '';
}

// Render plan items
function renderPlanItems() {
    const container = document.getElementById('plan-items');

    if (!container) {
        console.error('Plan items container not found');
        return;
    }

    if (Object.keys(planningData).length === 0) {
        container.innerHTML = '<p class="help-text">Inga kunder tillagda ännu</p>';
        return;
    }

    container.innerHTML = Object.entries(planningData).map(([key, data]) => {
        const customer = allCustomers.find(c => c.id == data.customer_id);
        if (!customer) return '';

        return `
            <div class="plan-item">
                <div class="plan-item-info">
                    <h4>${customer.canonical_root}</h4>
                    <p><strong>${data.link_count} länkar</strong> på <em>${data.pub_domain}</em></p>
                    ${data.target_url ? `<p style="font-size: 0.9em;">🎯 Målsida: ${data.target_url}</p>` : ''}
                    ${data.anchor_text ? `<p style="font-size: 0.9em;">📝 Ankar: "${data.anchor_text}"</p>` : ''}
                </div>
                <div class="plan-item-actions">
                    <button class="btn-danger" onclick="removeFromPlan('${key}')">Ta bort</button>
                </div>
            </div>
        `;
    }).join('');

    console.log('Rendered', Object.keys(planningData).length, 'plan items');
}

// Remove from plan
function removeFromPlan(planKey) {
    console.log('Removing from plan:', planKey);
    delete planningData[planKey];
    renderPlanItems();
}

// Load November Plan and create AI agents
async function loadNovemberPlan() {
    const confirmMsg = `Ladda November Plan från CSV?\n\n` +
                      `Systemet kommer att:\n` +
                      `✓ Läsa november_plan.csv\n` +
                      `✓ Analysera varje kund\n` +
                      `✓ Skapa en AI-agent per kund\n` +
                      `✓ Generera prompts för att komplettera länkar\n\n` +
                      `Fortsätt?`;

    if (!confirm(confirmMsg)) {
        return;
    }

    showLoading();

    try {
        console.log('Loading November Plan...');

        const response = await fetch('/api/load-november-plan', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        });

        const data = await response.json();

        if (data.error) {
            alert('Fel vid laddning: ' + data.error);
            return;
        }

        console.log('November Plan loaded:', data);

        // Visa AI-agents dialog
        showAIAgentsDialog(data);

    } catch (error) {
        console.error('Error loading November Plan:', error);
        alert('Kunde inte ladda November Plan: ' + error.message);
    } finally {
        hideLoading();
    }
}

// Show AI Agents Dialog
function showAIAgentsDialog(planData) {
    const modal = document.getElementById('customer-modal');
    const details = document.getElementById('customer-details');

    const readyCustomers = planData.customers.filter(c => c.status === 'ready');
    const notFoundCustomers = planData.customers.filter(c => c.status === 'not_found');

    details.innerHTML = `
        <h2>🤖 November Plan - AI Agents</h2>
        <p style="color: var(--text-light); margin-bottom: 20px;">
            Analys av ${planData.total_customers} kunder med ${planData.total_links} länkar
        </p>
        
        <div class="plan-summary">
            <div class="summary-card">
                <div class="summary-value">${readyCustomers.length}</div>
                <div class="summary-label">Redo för AI</div>
            </div>
            <div class="summary-card">
                <div class="summary-value">${planData.total_needs_target}</div>
                <div class="summary-label">Behöver målsida</div>
            </div>
            <div class="summary-card">
                <div class="summary-value">${planData.total_needs_anchor}</div>
                <div class="summary-label">Behöver ankartext</div>
            </div>
        </div>
        
        <h3 style="margin: 20px 0 10px;">👥 Kunder redo för AI-agents (${readyCustomers.length}):</h3>
        <div style="max-height: 400px; overflow-y: auto;">
            ${readyCustomers.map(customer => `
                <div style="background: var(--light); padding: 15px; border-radius: 8px; margin-bottom: 10px;">
                    <h4>${customer.customer_name} (${customer.canonical_root})</h4>
                    <p><strong>${customer.total_links} länkar</strong> - ${customer.needs_target} behöver målsida, ${customer.needs_anchor} behöver ankartext</p>
                    <p style="color: var(--text-light); font-size: 0.9em;">Marknader: ${customer.markets.join(', ')}</p>
                    <button onclick="generateCustomerAgentPrompt('${escapeQuotes(customer.customer_name)}')" class="btn-primary" style="margin-top: 10px;">
                        🤖 Generera AI-Agent Prompt
                    </button>
                </div>
            `).join('')}
        </div>
        
        ${notFoundCustomers.length > 0 ? `
            <h3 style="margin: 20px 0 10px;">⚠️ Kunder ej funna i databas (${notFoundCustomers.length}):</h3>
            <div style="background: #fff3cd; padding: 15px; border-radius: 8px; max-height: 200px; overflow-y: auto;">
                ${notFoundCustomers.map(c => `<p>• ${c.customer_name} (${c.total_links} länkar)</p>`).join('')}
            </div>
        ` : ''}
        
        <div style="display: flex; gap: 10px; justify-content: flex-end; margin-top: 20px;">
            <button onclick="closeModal()" class="btn-secondary">Stäng</button>
            <button onclick="generateAllAgentPrompts()" class="btn-success">🤖 Generera ALLA AI-Prompts</button>
        </div>
    `;

    // Spara data globalt för senare användning
    window.novemberPlanData = planData;

    modal.style.display = 'block';
}

function escapeQuotes(str) {
    return str.replace(/'/g, "\\'");
}

async function generateCustomerAgentPrompt(customerName) {
    if (!window.novemberPlanData) {
        alert('No plan data loaded');
        return;
    }

    const customer = window.novemberPlanData.customers.find(c => c.customer_name === customerName);
    if (!customer) {
        alert('Customer not found');
        return;
    }

    showLoading();

    try {
        const response = await fetch('/api/generate-customer-agent-prompt', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ customer })
        });

        const data = await response.json();

        if (data.error) {
            alert('Fel: ' + data.error);
            return;
        }

        // Visa prompt i en ny dialog
        showAgentPromptDialog(data);

    } catch (error) {
        console.error('Error generating agent prompt:', error);
async function loadPreflight() {
    const urlInput = document.getElementById('preflight-sheets-url');
    const sheetNameInput = document.getElementById('preflight-sheet-name');
    const startRowInput = document.getElementById('preflight-start-row');
    const endRowInput = document.getElementById('preflight-end-row');

    if (!urlInput || !sheetNameInput || !startRowInput || !endRowInput) {
        console.error('Preflight inputs not found');
        return;
    }

    const sheetsUrl = urlInput.value.trim();
    const sheetName = sheetNameInput.value.trim();
    const startRow = parseInt(startRowInput.value);
    const endRow = parseInt(endRowInput.value);

    if (!sheetsUrl || !sheetName) {
        alert('Ange Google Sheets URL och flik-namn');
        return;
    }

    const confirmMsg = `Ladda preflight från ${sheetName}?\n\n` +
                      `Rader: ${startRow} till ${endRow}\n` +
                      `Kolumner: Domain (pub_domain) + Kund\n\n` +
                      `Systemet kommer att:\n` +
                      `✓ Läsa pub_domains och kunder\n` +
                      `✓ Matcha mot client_index\n` +
                      `✓ Validera kund-domäner\n` +
                      `✓ Ladda in för planering\n\n` +
                      `Fortsätt?`;

    if (!confirm(confirmMsg)) {
        return;
    }

    showLoading();

    try {
        console.log('Loading preflight:', sheetName, startRow, endRow);

        const response = await fetch('/api/load-preflight', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                sheets_url: sheetsUrl,
                sheet_name: sheetName,
                start_row: startRow,
                end_row: endRow
            })
        });

        const data = await response.json();

        if (data.error) {
            alert('Fel vid generering: ' + data.error);
            return;
        }

        console.log('Preflight loaded:', data);

        // Rensa befintlig planering
        planningData = {};

        // Lägg till preflight items
        let addedCount = 0;

        data.preflight_items.forEach(item => {
            const planKey = `${item.customer_id}_${Date.now()}_${addedCount}`;
            planningData[planKey] = {
                customer_id: item.customer_id,
                link_count: 1,
                pub_domain: item.pub_domain,
                target_url: null,  // Ska fyllas i vid plangenerering
                anchor_text: null,  // Ska fyllas i vid plangenerering
                client_domain: item.client_domain  // För validering
            };
            addedCount++;
        });

        console.log('Added', addedCount, 'generated items');

        renderPlanItems();

        // Aktivera "Analysera"-knappen
        const analyzeBtn = document.getElementById('analyze-btn');
        if (analyzeBtn) {
            analyzeBtn.disabled = false;
        }

        // Visa workflow status
fa        updateWorkflowStatus('preflight_loaded', {
            sheet: sheetName,
            customers: data.total_customers,
            links: addedCount
        });

        // Bygg alert-meddelande
        let alertMsg = `✅ Preflight laddad från ${sheetName}!\n\n` +
                      `${data.total_customers} kunder\n` +
                      `${addedCount} länkar totalt\n`;

        // Visa valideringsfel om det finns
        if (data.total_errors > 0) {
            alertMsg += `\n⚠️ Valideringsfel: ${data.total_errors}\n`;
            if (data.validation_errors && data.validation_errors.length > 0) {
                alertMsg += '\nExempel:\n';
                data.validation_errors.slice(0, 3).forEach(error => {
                    alertMsg += `  • ${error}\n`;
                });
                if (data.total_errors > 3) {
                    alertMsg += `  ... och ${data.total_errors - 3} till\n`;
                }
            }
        }

        if (data.total_skipped > 0) {
            alertMsg += `\n⚠️ Skippade rader: ${data.total_skipped}\n`;
        }

        alertMsg += `\n✅ Preflight laddad och validerad!\n`;
        alertMsg += `\n➡️ Granska och redigera nedan\n` +
                    `➡️ Lägg till målsidor/ankartexter om önskat\n` +
                    `➡️ Klicka sedan "Analysera kunders planering"`;

        alert(alertMsg);

    } catch (error) {
        console.error('Error generating monthly plan:', error);
        alert('Kunde inte generera månadens planering: ' + error.message);
    } finally {
        hideLoading();
    }
}

// Update Workflow Status
function updateWorkflowStatus(stage, data) {
    const statusDiv = document.getElementById('workflow-status');
    const contentDiv = document.getElementById('status-content');

    if (!statusDiv || !contentDiv) return;

    statusDiv.style.display = 'block';

    if (stage === 'preflight_loaded') {
        contentDiv.innerHTML = `
            <div style="display: flex; gap: 10px; align-items: center;">
                <span style="font-size: 2em;">📥</span>
                <div>
                    <strong>Steg 1: Preflight laddad</strong>
                    <p style="margin: 5px 0 0 0; color: var(--text-light);">
                        ${data.sheet} - ${data.customers} kunder, ${data.links} länkar
                    </p>
                </div>
            </div>
            <p style="margin: 10px 0 0 0; color: var(--text-light);">
                ➡️ Granska planeringen nedan. Lägg till målsidor/ankartexter.<br>
                ➡️ Klicka "Analysera kunders planering" när du är klar.
            </p>
        `;
    } else if (stage === 'generated') {
        contentDiv.innerHTML = `
            <div style="display: flex; gap: 10px; align-items: center;">
                <span style="font-size: 2em;">✅</span>
                <div>
                    <strong>Steg 1: Planering genererad</strong>
                    <p style="margin: 5px 0 0 0; color: var(--text-light);">
                        ${data.month} ${data.year} - ${data.customers} kunder, ${data.links} länkar
                    </p>
                </div>
            </div>
            <p style="margin: 10px 0 0 0; color: var(--text-light);">
                ➡️ Granska planeringen nedan. Redigera om nödvändigt.<br>
                ➡️ Klicka "Analysera kunders planering" när du är klar.
            </p>
        `;
    } else if (stage === 'analyzed') {
        contentDiv.innerHTML = `
            <div style="display: flex; gap: 10px; align-items: center; margin-bottom: 10px;">
                <span style="font-size: 2em;">✅</span>
                <div>
                    <strong>Steg 1: Planering genererad</strong>
                </div>
            </div>
            <div style="display: flex; gap: 10px; align-items: center;">
                <span style="font-size: 2em;">✅</span>
                <div>
                    <strong>Steg 2: Semantisk analys klar</strong>
                    <p style="margin: 5px 0 0 0; color: var(--text-light);">
                        ${data.clusters || 0} semantiska kluster identifierade<br>
                        ${data.entities || 0} entiteter extraherade
                    </p>
                </div>
            </div>
            <p style="margin: 10px 0 0 0; color: var(--success);">
                ✨ Redo att generera plan! Klicka "Generera plan" för att slutföra.
            </p>
        `;
    }
}

// Import from Google Sheets
async function importFromSheets() {
    const urlInput = document.getElementById('sheets-url');
    const sheetNameInput = document.getElementById('sheet-name');

    if (!urlInput || !sheetNameInput) {
        console.error('Sheet inputs not found');
        return;
    }

    const sheetsUrl = urlInput.value.trim();
    const sheetName = sheetNameInput.value.trim() || 'November';

    if (!sheetsUrl) {
        alert('Ange Google Sheets URL');
        return;
    }

    showLoading();

    try {
        console.log('Importing from sheets:', sheetsUrl, sheetName);

        const response = await fetch('/api/import-sheets', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                sheets_url: sheetsUrl,
                sheet_name: sheetName
            })
        });

        const data = await response.json();

        if (data.error) {
            let errorMsg = `❌ Fel vid import:\n\n${data.error}`;
            if (data.message) {
                errorMsg += `\n\n${data.message}`;
            }
            alert(errorMsg);
            return;
        }

        console.log('Imported data:', data);

        // Lägg till varje rad i planningData
        let addedCount = 0;
        data.rows.forEach(row => {
            if (row.customer_id && row.pub_domain) {
                const planKey = `${row.customer_id}_${Date.now()}_${addedCount}`;
                planningData[planKey] = {
                    customer_id: row.customer_id,
                    link_count: 1, // En länk per rad från sheets
                    pub_domain: row.pub_domain,
                    target_url: row.target_url || null,
                    anchor_text: row.anchor_text || null
                };
                addedCount++;
            }
        });

        console.log('Added', addedCount, 'items from sheets');

        renderPlanItems();

        // Visa resultat med eventuella varningar
        let resultMsg = `✅ Importerade ${addedCount} rader från Google Sheets!`;

        if (data.total_processed) {
            resultMsg += `\n\nBearbetade: ${data.total_processed} rader`;
        }

        if (data.skipped_count > 0) {
            resultMsg += `\n⚠️ Skippade: ${data.skipped_count} rader`;

            if (data.skipped_rows && data.skipped_rows.length > 0) {
                resultMsg += `\n\nExempel på skippade rader:\n`;
                data.skipped_rows.slice(0, 5).forEach(skip => {
                    resultMsg += `- ${skip}\n`;
                });

                if (data.skipped_count > 5) {
                    resultMsg += `\n(och ${data.skipped_count - 5} till...)`;
                }
            }
        }

        alert(resultMsg);

    } catch (error) {
        console.error('Error importing from sheets:', error);
        alert('Kunde inte importera från Google Sheets: ' + error.message);
    } finally {
        hideLoading();
    }
}

// Analyze Customer Planning (Semantic Preflight)
async function analyzeCustomerPlanning() {
    if (Object.keys(planningData).length === 0) {
        alert('Lägg till kunder först');
        return;
    }

    showLoading();

    try {
        console.log('Starting semantic preflight analysis...');

        const response = await fetch('/api/semantic-preflight', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                planning_data: planningData
            })
        });

        const data = await response.json();

        if (data.error) {
            alert('Fel vid analys: ' + data.error);
            return;
        }

        console.log('Semantic analysis complete:', data);

        // Visa analys-resultat
        const resultModal = document.getElementById('customer-modal');
        const details = document.getElementById('customer-details');

        details.innerHTML = `
            <h2>🔍 Semantisk Preflight-Analys</h2>
            <p style="color: var(--text-light); margin-bottom: 20px;">
                Analys av ${data.total_customers} kunder och ${data.total_links} länkar
            </p>
            
            <div class="plan-summary">
                <div class="summary-card">
                    <div class="summary-value">${data.semantic_clusters || 0}</div>
                    <div class="summary-label">Semantiska kluster</div>
                </div>
                <div class="summary-card">
                    <div class="summary-value">${data.entities_found || 0}</div>
                    <div class="summary-label">Entiteter</div>
                </div>
                <div class="summary-card">
                    <div class="summary-value">${data.topical_authority_opportunities || 0}</div>
                    <div class="summary-label">Authority-möjligheter</div>
                </div>
            </div>
            
            <h3 style="margin: 20px 0 10px;">📊 Per Kund:</h3>
            ${data.customer_analyses.map(ca => `
                <div style="background: var(--light); padding: 15px; border-radius: 8px; margin-bottom: 10px;">
                    <h4>${ca.canonical_root}</h4>
                    <p><strong>${ca.planned_links} länkar</strong> - Strategi: ${ca.strategy}</p>
                    ${ca.semantic_analysis_possible ? 
                        '<span class="badge badge-success">✅ Semantisk analys möjlig</span>' : 
                        '<span class="badge badge-warning">⚠️ För få länkar för semantisk analys</span>'
                    }
                    ${ca.can_build_authority ? '<span class="badge badge-success">Kan bygga authority</span>' : ''}
                    ${ca.recommended_clusters ? `<p style="margin-top: 10px;">Rekommenderade kluster: ${ca.recommended_clusters.join(', ')}</p>` : ''}
                </div>
            `).join('')}
            
            <h3 style="margin: 20px 0 10px;">💡 Rekommendationer:</h3>
            <ul style="padding-left: 20px;">
                ${data.recommendations.map(rec => `<li>${rec}</li>`).join('')}
            </ul>
            
            ${data.url_validation && data.url_validation.total_errors > 0 ? `
                <div style="background: #f8d7da; padding: 15px; border-radius: 8px; margin-top: 20px; border-left: 4px solid #dc3545;">
                    <strong>❌ URL-valideringsfel (${data.url_validation.total_errors}):</strong>
                    <ul style="margin: 10px 0 0 0; padding-left: 20px;">
                        ${data.url_validation.errors.map(err => `<li>${err}</li>`).join('')}
                    </ul>
                    <p style="margin: 10px 0 0 0; color: #721c24;">
                        <strong>⚠️ Fixa dessa fel innan du fortsätter!</strong>
                    </p>
                </div>
            ` : `
                <div style="background: #d4edda; padding: 15px; border-radius: 8px; margin-top: 20px; border-left: 4px solid #28a745;">
                    <strong>✅ Analys godkänd!</strong>
                    <p style="margin: 10px 0 0 0;">
                        ${data.url_validation && data.url_validation.total_warnings > 0 ? 
                            `⚠️ ${data.url_validation.total_warnings} varningar (kan ignoreras)<br>` : ''}
                        Klicka "Fortsätt" för att aktivera "Generera plan"-knappen.
                    </p>
                </div>
            `}
            
            
            <div style="display: flex; gap: 10px; justify-content: flex-end; margin-top: 20px;">
                <button onclick="closeModal()" class="btn-secondary">Avbryt</button>
                <button onclick="confirmSemanticAnalysis()" class="btn-success">✅ Fortsätt</button>
            </div>
        `;

        resultModal.style.display = 'block';

    } catch (error) {
        console.error('Error analyzing planning:', error);
        alert('Kunde inte analysera planering: ' + error.message);
    } finally {
        hideLoading();
    }
}

// Confirm Semantic Analysis
function confirmSemanticAnalysis() {
    closeModal();

    // Aktivera "Generera plan"-knappen
    const generateBtn = document.getElementById('generate-btn');
    if (generateBtn) {
        generateBtn.disabled = false;
    }

    // Uppdatera workflow status
    updateWorkflowStatus('analyzed', {
        clusters: 3,  // Detta borde komma från API
        entities: 15
    });

    alert('✅ Semantisk analys godkänd!\n\nDu kan nu klicka "Generera plan" för att slutföra.');
}

// Detect volume
async function detectVolume() {
    if (Object.keys(planningData).length === 0) {
        alert('Lägg till kunder först');
        return;
    }

    showLoading();

    try {
        // Konvertera planningData till customer_id -> total_link_count format
        const volumeData = {};
        Object.values(planningData).forEach(item => {
            const cid = item.customer_id;
            volumeData[cid] = (volumeData[cid] || 0) + item.link_count;
        });

        console.log('Detecting volume for:', volumeData);

        const response = await fetch('/api/detect-volume', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ planning_data: volumeData })
        });

        const data = await response.json();
        console.log('Volume detection result:', data);

        const container = document.getElementById('volume-results');
        container.innerHTML = data.volumes.map(v => `
            <div class="volume-item">
                <h4>${v.canonical_root}</h4>
                <p style="color: var(--text-light); margin-bottom: 10px;">
                    ${v.planned_links} länkar planerade | ${v.historical_total} historiskt (${v.historical_monthly_avg}/mån)
                </p>
                <div>
                    <span class="badge badge-info">${v.recommended_strategy}</span>
                    ${v.semantic_planning_possible ? 
                        '<span class="badge badge-success">✅ Semantisk planering möjlig</span>' :
                        '<span class="badge badge-warning">⚠️ För få länkar för semantik</span>'
                    }
                    ${v.can_cluster ? '<span class="badge badge-success">Kan clustra</span>' : ''}
                    ${v.can_build_authority ? '<span class="badge badge-success">Kan bygga authority</span>' : ''}
                </div>
            </div>
        `).join('');

    } catch (error) {
        console.error('Error detecting volume:', error);
        alert('Kunde inte analysera volym: ' + error.message);
    } finally {
        hideLoading();
    }
}

// Generate plan
async function generatePlan() {
    if (Object.keys(planningData).length === 0) {
        alert('Lägg till kunder först');
        return;
    }

    // Visa AI-prompt dialog
    showAIPromptDialog();
}

// Show AI Prompt Dialog
function showAIPromptDialog() {
    const modal = document.getElementById('customer-modal');
    const details = document.getElementById('customer-details');

    // Sammanfatta planeringen
    const summary = generatePlanningSummary();

    details.innerHTML = `
        <h2>🤖 AI-assisterad Länkplanering</h2>
        <p style="color: var(--text-light); margin-bottom: 20px;">
            Systemet kommer att använda AI för att göra semantiska bedömningar av ankartexter och målsidor.
        </p>
        
        <div style="background: var(--light); padding: 20px; border-radius: 12px; margin-bottom: 20px;">
            <h3>📊 Planerings-sammanfattning:</h3>
            ${summary}
        </div>
        
        <div style="background: #fff3cd; padding: 15px; border-radius: 8px; margin-bottom: 20px; border-left: 4px solid #ffc107;">
            <strong>💡 AI kommer att:</strong>
            <ul style="margin: 10px 0; padding-left: 20px;">
                <li>Analysera målsidor semantiskt</li>
                <li>Generera relevanta ankartexter baserat på innehåll</li>
                <li>Distribuera länkar optimalt för SEO</li>
                <li>Bygga topical authority där möjligt</li>
                <li>Följa naturlig anchor distribution</li>
            </ul>
        </div>
        
        <div style="margin-bottom: 20px;">
            <label style="display: block; margin-bottom: 10px; font-weight: bold;">
                📝 Instruktioner till AI (valfritt):
            </label>
            <textarea id="ai-instructions" rows="4" style="width: 100%; padding: 10px; border: 2px solid var(--border); border-radius: 8px; font-family: inherit;"
                placeholder="T.ex. 'Fokusera på casino-relaterade termer' eller 'Undvik överdrivet optimerade ankartexter'"></textarea>
        </div>
        
        <div style="display: flex; gap: 10px; justify-content: flex-end;">
            <button onclick="closeModal()" class="btn-secondary">Avbryt</button>
            <button onclick="confirmAIGeneration()" class="btn-success">🚀 Starta AI-planering</button>
        </div>
    `;

    modal.style.display = 'block';
}

// Generate Planning Summary
function generatePlanningSummary() {
    const customerCounts = {};
    let totalLinks = 0;

    Object.values(planningData).forEach(item => {
        const cid = item.customer_id;
        customerCounts[cid] = (customerCounts[cid] || 0) + item.link_count;
        totalLinks += item.link_count;
    });

    const customerList = Object.entries(customerCounts).map(([cid, count]) => {
        const customer = allCustomers.find(c => c.id == cid);
        return `<li><strong>${customer.canonical_root}</strong>: ${count} länkar</li>`;
    }).join('');

    return `
        <p><strong>Totalt antal länkar:</strong> ${totalLinks}</p>
        <p><strong>Antal kunder:</strong> ${Object.keys(customerCounts).length}</p>
        <ul style="margin: 10px 0; padding-left: 20px;">
            ${customerList}
        </ul>
    `;
}

// Confirm AI Generation
async function confirmAIGeneration() {
    const aiInstructions = document.getElementById('ai-instructions').value.trim();
    const planName = document.getElementById('plan-name').value ||
        `Plan ${new Date().toLocaleDateString('sv-SE')}`;

    closeModal();
    showLoading();

    try {
        console.log('Generating plan with AI:', planName, planningData, aiInstructions);

        // Skicka full planningData med alla detaljer + AI instructions
        const response = await fetch('/api/generate-plan', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                planning_data: planningData,
                plan_name: planName,
                ai_instructions: aiInstructions || null
            })
        });

        const plan = await response.json();
        console.log('Plan generated:', plan);

        // Show results
        document.getElementById('plan-results').style.display = 'block';

        // Summary
        document.getElementById('plan-summary').innerHTML = `
            <div class="plan-summary">
                <div class="summary-card">
                    <div class="summary-value">${plan.total_customers}</div>
                    <div class="summary-label">Kunder</div>
                </div>
                <div class="summary-card">
                    <div class="summary-value">${plan.total_links}</div>
                    <div class="summary-label">Totalt länkar</div>
                </div>
                <div class="summary-card">
                    <div class="summary-value">${Object.keys(plan.strategy_summary).length}</div>
                    <div class="summary-label">Strategier</div>
                </div>
            </div>
            
            ${plan.ai_prompt ? `
                <div style="background: #e3f2fd; padding: 20px; border-radius: 12px; margin: 20px 0; border-left: 4px solid #2196f3;">
                    <h3 style="margin-top: 0;">🤖 AI-Prompt använd:</h3>
                    <button onclick="copyAIPrompt()" class="btn-secondary" style="margin-bottom: 10px;">
                        📋 Kopiera prompt
                    </button>
                    <button onclick="toggleAIPrompt()" class="btn-secondary" style="margin-bottom: 10px;">
                        👁️ Visa/Dölj prompt
                    </button>
                    <pre id="ai-prompt-content" style="display: none; background: white; padding: 15px; border-radius: 8px; overflow-x: auto; max-height: 400px; font-size: 0.9em;">${escapeHtml(plan.ai_prompt)}</pre>
                    <textarea id="ai-prompt-hidden" style="display: none;">${plan.ai_prompt}</textarea>
                </div>
            ` : ''}
            
            <div style="margin: 20px 0; text-align: center;">
                <a href="/api/download/${plan.csv_file}" class="btn-success" style="text-decoration: none; display: inline-block;">
                    📥 Ladda ner CSV
                </a>
            </div>
        `;

        // Details
        document.getElementById('plan-details').innerHTML = plan.customers.map(c => `
            <div class="plan-customer">
                <h4>${c.canonical_root} (${c.planned_links} länkar)</h4>
                <p style="color: var(--text-light);">Strategi: ${c.strategy}</p>
                
                <div class="anchor-dist">
                    ${Object.entries(c.anchor_distribution).map(([type, count]) => {
                        const pct = ((count / c.planned_links) * 100).toFixed(0);
                        return `<span class="badge badge-info">${type}: ${count} (${pct}%)</span>`;
                    }).join('')}
                </div>
                
                <h5 style="margin: 15px 0 10px;">Förhandsvisning (första 10 länkar):</h5>
                ${c.links.map((link, i) => `
                    <div class="link-preview">
                        <strong>${i + 1}. "${link.anchor_text}"</strong> (${link.anchor_type})<br>
                        → ${link.target_url}<br>
                        <small style="color: var(--text-light);">${link.reasoning}</small>
                    </div>
                `).join('')}
            </div>
        `).join('');

        // Scroll to results
        document.getElementById('plan-results').scrollIntoView({ behavior: 'smooth' });

    } catch (error) {
        console.error('Error generating plan:', error);
        alert('Kunde inte generera plan: ' + error.message);
    } finally {
        hideLoading();
    }
}

// Load history
async function loadHistory() {
    const select = document.getElementById('history-customer-select');

    if (!select) {
        console.error('History customer select not found');
        return;
    }

    const customerId = select.value;

    if (!customerId) {
        alert('Välj en kund');
        return;
    }

    showLoading();

    try {
        console.log('Loading history for customer:', customerId);

        const response = await fetch(`/api/customer/${customerId}/monthly`);
        const data = await response.json();

        console.log('History loaded:', data.count, 'months');

        const container = document.getElementById('monthly-history');
        container.innerHTML = data.months.reverse().map(m => `
            <div class="month-card">
                <h3>${m.display_name} (${m.link_count} länkar)</h3>
                
                <div class="month-stats">
                    <div class="month-stat">
                        <div class="month-stat-value">${m.unique_pub_domains}</div>
                        <div class="month-stat-label">Pub-domäner</div>
                    </div>
                    <div class="month-stat">
                        <div class="month-stat-value">${m.unique_target_urls}</div>
                        <div class="month-stat-label">Målsidor</div>
                    </div>
                </div>
                
                <h4 style="margin: 15px 0 10px;">Anchor Types:</h4>
                <div class="anchor-dist">
                    ${Object.entries(m.anchor_types || {}).map(([type, count]) => `
                        <span class="badge badge-info">${type}: ${count}</span>
                    `).join('')}
                </div>
                
                <h4 style="margin: 15px 0 10px;">Vanligaste ankartexter:</h4>
                ${(m.most_common_anchors || []).map(([text, count]) => `
                    <div class="link-preview">"${text}" - ${count}x</div>
                `).join('')}
            </div>
        `).join('');

    } catch (error) {
        console.error('Error loading history:', error);
        alert('Kunde inte ladda historik: ' + error.message);
    } finally {
        hideLoading();
    }
}

// Loading overlay
function showLoading() {
    const overlay = document.getElementById('loading-overlay');
    if (overlay) {
        overlay.style.display = 'flex';
    }
}

function hideLoading() {
    const overlay = document.getElementById('loading-overlay');
    if (overlay) {
        overlay.style.display = 'none';
    }
}

// Close modal on outside click
window.onclick = function(event) {
    const modal = document.getElementById('customer-modal');
    if (modal && event.target == modal) {
        modal.style.display = 'none';
    }
}

// Helper functions for AI prompt
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function toggleAIPrompt() {
    const content = document.getElementById('ai-prompt-content');
    if (content) {
        content.style.display = content.style.display === 'none' ? 'block' : 'none';
    }
}

function copyAIPrompt() {
    const textarea = document.getElementById('ai-prompt-hidden');
    if (textarea) {
        textarea.style.display = 'block';
        textarea.select();
        document.execCommand('copy');
        textarea.style.display = 'none';
        alert('✅ AI-prompt kopierad till urklipp! Du kan nu klistra in den i en AI-tjänst.');
    }
}

// Main Sheet Viewer
let mainSheetData = {
    offset: 0,
    limit: 100
};

async function loadMainSheet(append = false) {
    showLoading();
    
    try {
        if (!append) {
            mainSheetData.offset = 0;
        }
        
        const response = await fetch(`/api/mainsheet?limit=${mainSheetData.limit}&offset=${mainSheetData.offset}`);
        const data = await response.json();
        
        if (data.error) {
            alert('Fel: ' + data.error);
            return;
        }
        
        console.log('Main sheet loaded:', data);
        
        // Uppdatera statistik
        document.getElementById('mainsheet-total').textContent = data.total.toLocaleString();
        document.getElementById('mainsheet-shown').textContent = data.showing;
        document.getElementById('mainsheet-unique-customers').textContent = data.unique_customers;
        
        // Rendera tabell
        const tbody = document.getElementById('mainsheet-tbody');
        
        if (!append) {
            tbody.innerHTML = '';
        }
        
        data.records.forEach((record, idx) => {
            const row = document.createElement('tr');
            row.style.borderBottom = '1px solid #ddd';
            
            row.innerHTML = `
                <td style="padding: 8px; border: 1px solid #ddd;">${record.index + 1}</td>
                <td style="padding: 8px; border: 1px solid #ddd;">${record.canonical_root}</td>
                <td style="padding: 8px; border: 1px solid #ddd;">${record.brand}</td>
                <td style="padding: 8px; border: 1px solid #ddd; max-width: 200px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;" title="${record.pub_page_url}">
                    <a href="${record.pub_page_url}" target="_blank" style="color: var(--primary);">${record.pub_page_url}</a>
                </td>
                <td style="padding: 8px; border: 1px solid #ddd; max-width: 200px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;" title="${record.target_url}">
                    <a href="${record.target_url}" target="_blank" style="color: var(--primary);">${record.target_url}</a>
                </td>
                <td style="padding: 8px; border: 1px solid #ddd;">${record.anchor_text}</td>
                <td style="padding: 8px; border: 1px solid #ddd;">${record.link_type}</td>
                <td style="padding: 8px; border: 1px solid #ddd;">${record.published_at ? record.published_at.split(' ')[0] : ''}</td>
            `;
            
            tbody.appendChild(row);
        });
        
        // Uppdatera offset för nästa laddning
        mainSheetData.offset += data.showing;
        
        // Visa "Ladda fler" om det finns mer
        if (data.has_more) {
            const loadMoreRow = document.createElement('tr');
            loadMoreRow.id = 'load-more-row';
            loadMoreRow.innerHTML = `
                <td colspan="8" style="text-align: center; padding: 20px;">
                    <button onclick="loadMainSheet(true)" class="btn-primary">Ladda fler (${data.filtered - mainSheetData.offset} kvar)</button>
                </td>
            `;
            tbody.appendChild(loadMoreRow);
        }
        
    } catch (error) {
        console.error('Error loading main sheet:', error);
        alert('Kunde inte ladda main sheet: ' + error.message);
    } finally {
        hideLoading();
    }
}

async function searchMainSheet() {
    const searchInput = document.getElementById('mainsheet-search');
    const columnSelect = document.getElementById('mainsheet-filter-column');
    
    if (!searchInput) return;
    
    const search = searchInput.value.trim();
    const column = columnSelect ? columnSelect.value : '';
    
    showLoading();
    
    try {
        mainSheetData.offset = 0;
        
        let url = `/api/mainsheet?limit=${mainSheetData.limit}&offset=0`;
        if (search) {
            url += `&search=${encodeURIComponent(search)}`;
        }
        if (column) {
            url += `&column=${encodeURIComponent(column)}`;
        }
        
        const response = await fetch(url);
        const data = await response.json();
        
        if (data.error) {
            alert('Fel: ' + data.error);
            return;
        }
        
        console.log('Search results:', data);
        
        // Uppdatera statistik
console.log('App.js loaded successfully');

