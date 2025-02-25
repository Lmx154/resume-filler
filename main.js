import './style.css'

// Create the main navigation state
let currentPage = 'resume';
let currentSubmenu = '';
let openDropdown = ''; // new global variable for dropdown state

const pages = {
  resume: { title: 'Resume', submenus: ['Upload Resume'] },
  application: { title: 'Application', submenus: ['Upload Application'] },
  settings: { title: 'Settings', submenus: ['API Key', 'Ollama'] }
};

function renderContent() {
  const welcomeContent = `
    <div class="p-12 max-w-4xl mx-auto">
      <div class="bg-yale_blue-300 rounded-lg p-8 shadow-xl border border-yale_blue-400">
        <h2 class="text-4xl font-bold text-lemon_chiffon-500 mb-6">Welcome to Resume Filler!</h2>
        <p class="text-lg text-lemon_chiffon-400 mb-6">
          Auto-fill job application forms scraped from the web using your resume data, processed securely on your local machine.
        </p>
        <div class="grid grid-cols-2 gap-6 mb-8">
          <div class="bg-yale_blue-400 p-6 rounded-lg border border-yale_blue-500">
            <h3 class="text-xl font-semibold text-naples_yellow-500 mb-3">Local Processing</h3>
            <p class="text-lemon_chiffon-500">Your data stays on your computer, ensuring privacy.</p>
          </div>
          <div class="bg-yale_blue-400 p-6 rounded-lg border border-yale_blue-500">
            <h3 class="text-xl font-semibold text-naples_yellow-500 mb-3">AI Auto-Fill</h3>
            <p class="text-lemon_chiffon-500">Leverage AI to complete forms based on your resume.</p>
          </div>
        </div>
      </div>
    </div>
  `;

  const topNavbar = `
    <nav class="bg-yale_blue-400 text-white px-4 py-2 flex items-center gap-4">
      ${Object.entries(pages).map(([key, value]) => `
        <div class="relative">
          <button onclick="window.toggleDropdown('${key}')" class="menu-button hover:font-bold">
            ${value.title} ${value.submenus && value.submenus.length ? '<span class="ml-1">▼</span>' : ''}
          </button>
          ${value.submenus && value.submenus.length ? `
            <div class="dropdown ${openDropdown === key ? 'block' : 'hidden'} absolute left-0 mt-1 bg-yale_blue-300 text-lemon_chiffon-500 shadow-md">
              ${value.submenus.map(submenu => `
                <div onclick="window.handleSubmenu('${submenu}')" class="px-4 py-2 hover:bg-yale_blue-400 cursor-pointer">
                  ${submenu}
                </div>
              `).join('')}
            </div>
          ` : ''}
        </div>
      `).join('')}
    </nav>
  `;

  return `
    <div class="min-h-screen bg-yale_blue-200">
      <header class="bg-yale_blue-500 text-white py-4 px-6 shadow-lg">
        <h1 class="text-2xl font-bold">Resume Filler</h1>
      </header>
      ${topNavbar}
      <main class="p-6">
        ${currentSubmenu ? `
          <div>
            <h2 class="text-2xl font-semibold mb-4 text-lemon_chiffon-500">${currentSubmenu}</h2>
            ${getSubmenuContent(currentSubmenu)}
          </div>
        ` : welcomeContent}
      </main>
    </div>
  `;
}

async function processResumeFile(file) {
  try {
    const formData = new FormData();
    formData.append('file', file);

    // Collect customization options
    const enhancementFocus = document.getElementById('enhancement-focus')?.value || 'Clarity & Conciseness';
    const industryFocus = document.getElementById('industry-focus')?.value || 'Technology';
    const targetKeywords = document.getElementById('target-keywords')?.value || '';
    const companyCulture = document.getElementById('company-culture')?.value || '';

    const additionalInfoItems = document.querySelectorAll('#additional-info-container > div');
    let additionalInfo = {};
    additionalInfoItems.forEach(item => {
      const keyInput = item.children[0];
      const valueInput = item.children[1];
      if (keyInput.value && valueInput.value) {
        additionalInfo[keyInput.value] = valueInput.value;
      }
    });

    // Add customization options to form data
    formData.append('enhancement_focus', enhancementFocus);
    formData.append('industry_focus', industryFocus);
    formData.append('target_keywords', targetKeywords);
    formData.append('company_culture', companyCulture);
    formData.append('additional_info', JSON.stringify(additionalInfo));

    const response = await fetch('http://localhost:8000/api/resume/upload', { method: 'POST', body: formData });
    const result = await response.json();
    if (result.status === 'success') await handleRefreshResumeData();
  } catch (error) {
    console.error('Error processing resume:', error);
    alert('Error processing resume. Please try again.');
  }
}

function createFileInput() {
  const input = document.createElement('input');
  input.type = 'file';
  input.accept = '.pdf,.docx,.txt';
  input.style.display = 'none';
  input.onchange = async (e) => { if (e.target.files[0]) await processResumeFile(e.target.files[0]); };
  return input;
}

function getSubmenuContent(submenu) {
  const contents = {
    'Upload Resume': `
      <div class="w-full p-6">
        <div class="grid grid-cols-2 gap-6">
          <div class="space-y-4">
            <p class="text-lemon_chiffon-500 mb-4">Upload your resume and configure enhancement options.</p>
            <div class="bg-yale_blue-300 p-4 rounded-lg border border-yale_blue-400">
              <h3 class="font-semibold text-naples_yellow-500">Enhancement Focus</h3>
              <select id="enhancement-focus" class="w-full mt-2 p-2 border border-yale_blue-500 rounded bg-yale_blue-200 text-lemon_chiffon-500">
                <option>Clarity & Conciseness</option>
                <option>Professional Tone</option>
                <option>Keywords Optimization</option>
                <option>Impact & Achievement Focus</option>
              </select>
            </div>
            <div class="bg-yale_blue-300 p-4 rounded-lg border border-yale_blue-400">
              <h3 class="font-semibold text-naples_yellow-500">Industry Focus</h3>
              <select id="industry-focus" class="w-full mt-2 p-2 border border-yale_blue-500 rounded bg-yale_blue-200 text-lemon_chiffon-500">
                <option>Technology</option>
                <option>Healthcare</option>
                <option>Finance</option>
                <option>Education</option>
                <option>Other</option>
              </select>
            </div>
            <div class="bg-yale_blue-300 p-4 rounded-lg border border-yale_blue-400">
              <h3 class="font-semibold text-naples_yellow-500">Target Keywords</h3>
              <textarea id="target-keywords" class="w-full mt-2 p-2 border border-yale_blue-500 rounded bg-yale_blue-200 text-lemon_chiffon-500" rows="3" placeholder="Enter relevant keywords from the job"></textarea>
            </div>
            <div class="bg-yale_blue-300 p-4 rounded-lg border border-yale_blue-400">
              <h3 class="font-semibold text-naples_yellow-500">Company Culture Notes</h3>
              <textarea id="company-culture" class="w-full mt-2 p-2 border border-yale_blue-500 rounded bg-yale_blue-200 text-lemon_chiffon-500" rows="2" placeholder="Enter notes about the company culture"></textarea>
            </div>
            <div class="bg-yale_blue-300 p-4 rounded-lg border border-yale_blue-400">
              <h3 class="font-semibold text-naples_yellow-500">Additional Information</h3>
              <div id="additional-info-container" class="max-h-32 overflow-y-auto space-y-2">
                <!-- additional info items will be added here -->
              </div>
              <button id="add-additional-info" class="mt-2 bg-tomato-500 text-white px-4 py-2 rounded hover:bg-tomato-600">
                New Item
              </button>
            </div>
            <div class="border-2 border-dashed border-yale_blue-400 rounded-lg p-8 text-center bg-yale_blue-300 w-full mt-4">
              <button onclick="window.handleFileSelect()" class="bg-tomato-500 text-white px-6 py-3 rounded-lg hover:bg-tomato-600">Choose File</button>
              <p class="mt-2 text-sm text-lemon_chiffon-400">PDF, DOCX, or TXT files accepted</p>
            </div>
          </div>
          <div class="bg-yale_blue-300 rounded-lg p-6 border border-yale_blue-400">
            <div class="flex justify-between items-center mb-4">
              <h3 class="text-xl font-semibold text-naples_yellow-500">Parsed Resume</h3>
              <div>
                <button onclick="window.handleRefreshResumeData()" class="mr-2 text-sm text-lemon_chiffon-500 hover:text-lemon_chiffon-400">↻ Refresh</button>
                <button onclick="window.clearResumeData()" class="text-sm text-tomato-500 hover:text-tomato-600">Clear</button>
              </div>
            </div>
            <div id="resume-data" class="bg-yale_blue-200 rounded-lg p-4 h-[70vh] w-full overflow-auto">
              <p class="text-lemon_chiffon-500 text-center">No resume loaded yet...</p>
            </div>
          </div>
        </div>
      </div>
    `,
    'Upload Application': `
      <div class="w-full p-6">
        <div class="grid grid-cols-2 gap-6">
          <div class="bg-yale_blue-300 rounded-lg p-6 border border-yale_blue-400">
            <p class="text-lemon_chiffon-500 mb-4">Upload your scraped job application data.</p>
            <div class="border-2 border-dashed border-yale_blue-400 rounded-lg p-8 text-center bg-yale_blue-300 w-full">
              <button onclick="window.handleFileSelect()" class="bg-tomato-500 text-white px-6 py-3 rounded-lg hover:bg-tomato-600">Choose File</button>
              <p class="mt-2 text-sm text-lemon_chiffon-400">PDF, DOCX, or TXT files accepted</p>
            </div>
          </div>
          <div class="bg-yale_blue-300 rounded-lg p-6 border border-yale_blue-400">
            <div class="flex justify-between items-center mb-4">
              <h3 class="text-xl font-semibold text-naples_yellow-500">Application Data</h3>
              <div>
                <button onclick="window.handleRefreshData()" class="mr-2 text-sm text-lemon_chiffon-500 hover:text-lemon_chiffon-400">↻ Refresh</button>
                <button onclick="window.clearExtensionData()" class="text-sm text-tomato-500 hover:text-tomato-600">Clear</button>
              </div>
            </div>
            <div id="extension-data" class="bg-yale_blue-200 rounded-lg p-4 h-[70vh] w-full overflow-auto">
              <p class="text-lemon_chiffon-500 text-center">Waiting for application data...</p>
            </div>
          </div>
        </div>
      </div>
    `,
    'API Key': `
      <div class="max-w-2xl p-6">
        <p class="text-lemon_chiffon-500 mb-4">Configure your OpenAI API settings.</p>
        <div class="space-y-4">
          <div class="bg-yale_blue-300 p-4 rounded-lg border border-yale_blue-400">
            <h3 class="font-semibold text-naples_yellow-500">OpenAI API Base URL</h3>
            <input type="text" id="api-base" class="w-full mt-2 p-2 border border-yale_blue-500 rounded bg-yale_blue-200 text-lemon_chiffon-500" placeholder="e.g., https://rgvaiclass.com/chat/api/v1">
          </div>
          <div class="bg-yale_blue-300 p-4 rounded-lg border border-yale_blue-400">
            <h3 class="font-semibold text-naples_yellow-500">OpenAI API Key</h3>
            <input type="password" id="api-key" class="w-full mt-2 p-2 border border-yale_blue-500 rounded bg-yale_blue-200 text-lemon_chiffon-500" placeholder="Enter your OpenAI API key">
            <p class="mt-2 text-sm text-lemon_chiffon-400">Settings are stored locally.</p>
          </div>
          <div class="bg-yale_blue-300 p-4 rounded-lg border border-yale_blue-400">
            <h3 class="font-semibold text-naples_yellow-500">OpenAI Model</h3>
            <select id="api-model" class="w-full mt-2 p-2 border border-yale_blue-500 rounded bg-yale_blue-200 text-lemon_chiffon-500">
              <option value="gpt-3.5-turbo-16k">gpt-3.5-turbo-16k</option>
              <option value="gpt-4.0">gpt-4.0</option>
              <option value="gpt-4.0-mini">gpt-4.0-mini</option>
            </select>
          </div>
          <button onclick="window.handleApplyAPISettings()" class="bg-tomato-500 text-white px-6 py-3 rounded-lg hover:bg-tomato-600 transition-colors w-full">
            Apply Settings
          </button>
        </div>
      </div>
    `,
    'Ollama': `
      <div class="max-w-2xl p-6">
        <p class="text-lemon_chiffon-500 mb-4">Configure local Ollama settings for offline AI processing.</p>
        <div class="space-y-4">
          <div class="bg-yale_blue-300 p-4 rounded-lg border border-yale_blue-400">
            <h3 class="font-semibold text-naples_yellow-500">Ollama Endpoint</h3>
            <input type="text" class="w-full mt-2 p-2 border border-yale_blue-500 rounded bg-yale_blue-200 text-lemon_chiffon-500" placeholder="http://localhost:11434">
          </div>
          <div class="bg-yale_blue-300 p-4 rounded-lg border border-yale_blue-400">
            <h3 class="font-semibold text-naples_yellow-500">Model Selection</h3>
            <select class="w-full mt-2 p-2 border border-yale_blue-500 rounded bg-yale_blue-200 text-lemon_chiffon-500">
              <option>llama2</option>
              <option>mistral</option>
              <option>codellama</option>
            </select>
          </div>
          <div class="bg-yale_blue-300 p-4 rounded-lg border border-yale_blue-400">
            <h3 class="font-semibold text-naples_yellow-500">Model Parameters</h3>
            <div class="grid grid-cols-2 gap-4 mt-2">
              <div>
                <label class="text-sm text-lemon_chiffon-400">Temperature</label>
                <input type="number" step="0.1" min="0" max="2" class="w-full p-2 border border-yale_blue-500 rounded bg-yale_blue-200 text-lemon_chiffon-500" value="0.7">
              </div>
              <div>
                <label class="text-sm text-lemon_chiffon-400">Max Tokens</label>
                <input type="number" step="100" min="100" max="4000" class="w-full p-2 border border-yale_blue-500 rounded bg-yale_blue-200 text-lemon_chiffon-500" value="1000">
              </div>
            </div>
          </div>
        </div>
      </div>
    `
  };
  return contents[submenu] || `<p class="text-lemon_chiffon-500">Content for ${submenu} is being developed...</p>`;
}

// Navigation handlers
window.handleNavigation = (page) => {
  currentPage = page;
  currentSubmenu = '';
  document.querySelector('#app').innerHTML = renderContent();
  initAdditionalInfo();
};

window.handleSubmenu = (submenu) => {
  currentSubmenu = submenu;
  openDropdown = '';
  document.querySelector('#app').innerHTML = renderContent();
  initAdditionalInfo();
  if (submenu === 'Upload Application') setTimeout(() => window.handleRefreshData(), 500);
  else if (submenu === 'Upload Resume') setTimeout(() => window.handleRefreshResumeData(), 500);
};

// File selection handler
window.handleFileSelect = () => {
  const fileInput = createFileInput();
  document.body.appendChild(fileInput);
  fileInput.click();
  fileInput.addEventListener('change', () => setTimeout(() => document.body.removeChild(fileInput), 1000));
};

window.handleApplyAPISettings = async () => {
  const apiBase = document.getElementById('api-base').value;
  const apiKey = document.getElementById('api-key').value;
  const apiModel = document.getElementById('api-model').value;
  try {
    if (apiKey) {
      const response = await fetch('http://localhost:8000/api/settings/openai', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ api_base: apiBase, api_key: apiKey, model: apiModel })
      });
      const result = await response.json();
      if (result.status === 'success') alert('API settings updated successfully!');
      else throw new Error(result.message);
    }
  } catch (error) {
    console.error('Error updating API settings:', error);
    alert('Error updating API settings. Please check your connection.');
  }
};

window.clearExtensionData = () => {
  const dataContainer = document.getElementById('extension-data');
  if (dataContainer) dataContainer.innerHTML = '<p class="text-lemon_chiffon-500 text-center">Waiting for application data...</p>';
};

window.clearResumeData = () => {
  const dataContainer = document.getElementById('resume-data');
  if (dataContainer) dataContainer.innerHTML = '<p class="text-lemon_chiffon-500 text-center">No resume loaded yet...</p>';
};

window.handleExtensionData = (data) => {
  const dataContainer = document.getElementById('extension-data');
  if (dataContainer && data.display_text) {
    const metrics = data.metadata;
    dataContainer.innerHTML = `
      <div class="text-lemon_chiffon-500">
        <div class="mb-4 grid grid-cols-2 gap-4">
          <div><span class="font-semibold">Words:</span> ${metrics.word_count}<span class="ml-4 font-semibold">Paragraphs:</span> ${metrics.paragraph_count}</div>
          <div><span class="font-semibold">Sentences:</span> ${metrics.sentence_count}<span class="ml-4 font-semibold">Read Time:</span> ${metrics.estimated_read_time}m</div>
        </div>
        <div class="whitespace-pre-wrap font-mono text-sm bg-yale_blue-300 p-4 rounded-lg max-h-[400px] overflow-y-auto">${data.display_text}</div>
      </div>
    `;
  } else dataContainer.innerHTML = '<p class="text-lemon_chiffon-500 text-center">No data available</p>';
};

window.handleRefreshData = async () => {
  try {
    const dataContainer = document.getElementById('extension-data');
    if (!dataContainer) return;
    const response = await fetch('http://localhost:8000/api/application/last_extract');
    const data = await response.json();
    if (data.status === 'success' && data.display_text) window.handleExtensionData(data);
    else dataContainer.innerHTML = `<p class="text-lemon_chiffon-500 text-center">${data.message || 'No data available'}</p>`;
  } catch (error) { console.error('Error fetching data:', error); }
};

window.handleResumeData = (data) => {
  const dataContainer = document.getElementById('resume-data');
  if (dataContainer && data.parsed_sections) {
    const metrics = data.metadata;
    dataContainer.innerHTML = `
      <div class="text-lemon_chiffon-500">
        <div class="mb-4 grid grid-cols-2 gap-4">
          <div><span class="font-semibold">Words:</span> ${metrics.word_count}<span class="ml-4 font-semibold">Read Time:</span> ${metrics.estimated_read_time}m</div>
          <div><span class="font-semibold">Sentences:</span> ${metrics.sentence_count}</div>
        </div>
        <div class="whitespace-pre-wrap font-mono text-sm bg-yale_blue-300 p-4 rounded-lg max-h-[400px] overflow-y-auto">${JSON.stringify(data.parsed_sections, null, 2)}</div>
      </div>
    `;
  } else dataContainer.innerHTML = '<p class="text-lemon_chiffon-500 text-center">No resume loaded yet...</p>';
};

window.handleRefreshResumeData = async () => {
  try {
    const dataContainer = document.getElementById('resume-data');
    if (!dataContainer) return;
    const response = await fetch('http://localhost:8000/api/resume/upload', { method: 'GET' });
    const data = await response.json();
    if (data.status === 'success' && data.parsed_sections) window.handleResumeData(data);
    else dataContainer.innerHTML = `<p class="text-lemon_chiffon-500 text-center">${data.message || 'No resume loaded yet...'}</p>`;
  } catch (error) { console.error('Error fetching resume data:', error); }
};

function addAdditionalInfoItem(key = '', value = '') {
  const container = document.getElementById('additional-info-container');
  if (!container) return;
  const item = document.createElement('div');
  item.className = "flex gap-2";
  item.innerHTML = `
    <input type="text" class="flex-1 p-2 border border-yale_blue-500 rounded bg-yale_blue-200 text-lemon_chiffon-500" placeholder="e.g. GPA" value="${key}">
    <input type="text" class="flex-1 p-2 border border-yale_blue-500 rounded bg-yale_blue-200 text-lemon_chiffon-500" placeholder="e.g. 3.4" value="${value}">
    <button class="bg-tomato-500 text-white px-2 rounded delete-additional-info">Delete</button>
  `;
  container.appendChild(item);
  item.querySelector('.delete-additional-info').addEventListener('click', () => {
    container.removeChild(item);
  });
}

function initAdditionalInfo() {
  const addBtn = document.getElementById('add-additional-info');
  if (addBtn) {
    addBtn.addEventListener('click', () => addAdditionalInfoItem());
  }
}

window.toggleDropdown = (page) => {
  if (pages[page].submenus && pages[page].submenus.length) {
    openDropdown = openDropdown === page ? '' : page;
  } else {
    currentPage = page;
    currentSubmenu = '';
    openDropdown = '';
  }
  document.querySelector('#app').innerHTML = renderContent();
  initAdditionalInfo();
};

document.querySelector('#app').innerHTML = renderContent();
initAdditionalInfo();