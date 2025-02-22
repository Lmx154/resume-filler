import './style.css'

// Create the main navigation state
let currentPage = 'resume';
let currentSubmenu = '';

const pages = {
  resume: {
    title: 'Resume Tools',
    submenus: [
      'Upload Resume',
      'Enhance Resume',
      'Resume Context'
    ]
  },
  application: {
    title: 'Application Tools',
    submenus: [
      'Upload Application',
      'Enhance Application',
      'Application Context'
    ]
  },
  settings: {
    title: 'Settings',
    submenus: [
      'API Key',
      'Ollama'
    ]
  }
};

function renderContent() {
  const welcomeContent = `
    <div class="p-12 max-w-4xl mx-auto">
      <div class="bg-yale_blue-300 rounded-lg p-8 shadow-xl border border-yale_blue-400">
        <h2 class="text-4xl font-bold text-lemon_chiffon-500 mb-6">Welcome to Resume Filler!</h2>
        <p class="text-lg text-lemon_chiffon-400 mb-6">
          Transform your job application process using AI assistance. This tool helps you generate tailored responses 
          for job applications while keeping your data private and secure on your local machine.
        </p>
        <div class="grid grid-cols-2 gap-6 mb-8">
          <div class="bg-yale_blue-400 p-6 rounded-lg border border-yale_blue-500">
            <h3 class="text-xl font-semibold text-naples_yellow-500 mb-3">Local Processing</h3>
            <p class="text-lemon_chiffon-500">Your resume data stays on your computer. The application processes everything locally, ensuring your sensitive information remains private.</p>
          </div>
          <div class="bg-yale_blue-400 p-6 rounded-lg border border-yale_blue-500">
            <h3 class="text-xl font-semibold text-naples_yellow-500 mb-3">AI Integration</h3>
            <p class="text-lemon_chiffon-500">Choose between OpenAI API or local AI models like Ollama to generate tailored responses for job applications.</p>
          </div>
        </div>
        <div class="bg-yale_blue-400 p-6 rounded-lg border border-yale_blue-500">
          <h3 class="text-xl font-semibold text-naples_yellow-500 mb-3">Key Features</h3>
          <ul class="list-disc list-inside text-lemon_chiffon-500 space-y-2">
            <li>Local data processing for privacy</li>
            <li>Flexible AI model selection</li>
            <li>Customizable response generation</li>
            <li>Secure resume storage</li>
          </ul>
        </div>
      </div>
    </div>
  `;

  const submenuContent = currentSubmenu ? `
    <div class="p-6">
      <h2 class="text-2xl font-semibold mb-4 text-lemon_chiffon-500">${currentSubmenu}</h2>
      ${getSubmenuContent(currentSubmenu)}
    </div>
  ` : welcomeContent;

  return `
    <div class="min-h-screen bg-yale_blue-200">
      <header class="bg-yale_blue-500 text-white py-4 px-6 shadow-lg">
        <h1 class="text-2xl font-bold">Resume Filler</h1>
      </header>
      
      <div class="flex">
        <!-- Main Navigation -->
        <nav class="w-48 bg-yale_blue-400 h-[calc(100vh-64px)]">
          ${Object.entries(pages).map(([key, value]) => `
            <div class="menu-item ${currentPage === key ? 'active' : ''}"
                 onclick="window.handleNavigation('${key}')">
              ${value.title}
            </div>
          `).join('')}
        </nav>

        <!-- Submenu -->
        <nav class="w-56 bg-yale_blue-300 h-[calc(100vh-64px)] border-r border-yale_blue-400">
          ${pages[currentPage].submenus.map(submenu => `
            <div class="submenu-item ${currentSubmenu === submenu ? 'bg-yale_blue-400' : ''}"
                 onclick="window.handleSubmenu('${submenu}')">
              ${submenu}
            </div>
          `).join('')}
        </nav>

        <!-- Content Area -->
        <main class="flex-1 bg-yale_blue-200">
          ${submenuContent}
        </main>
      </div>
    </div>
  `;
}

async function processResumeFile(file) {
  try {
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await fetch('http://localhost:8000/api/resume/upload', {
      method: 'POST',
      body: formData
    });
    
    const result = await response.json();
    if (result.status === 'success') {
      // Refresh the parsed resume display after upload
      await handleRefreshResumeData();
      // Optionally update the AI response container if needed
      const aiResponse = document.getElementById('ai-response');
      if (aiResponse) {
        const formattedContent = `
          <div class="text-lemon_chiffon-500">
            <div class="mb-4 grid grid-cols-2 gap-4">
              <div>
                <span class="font-semibold">Words:</span> ${result.metadata.word_count}
                <span class="ml-4 font-semibold">Read Time:</span> ${result.metadata.estimated_read_time}m
              </div>
              <div>
                <span class="font-semibold">Sentences:</span> ${result.metadata.sentence_count}
              </div>
            </div>
            <div class="whitespace-pre-wrap font-mono text-sm bg-yale_blue-300 p-4 rounded-lg max-h-[400px] overflow-y-auto">
              ${JSON.stringify(result.parsed_sections, null, 2)}
            </div>
          </div>
        `;
        aiResponse.innerHTML = formattedContent;
      }
    }
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
  input.onchange = async (e) => {
    const file = e.target.files[0];
    if (file) {
      await processResumeFile(file);
    }
  };
  return input;
}

function getSubmenuContent(submenu) {
  const contents = {
    'Upload Resume': `
      <div class="max-w-4xl p-6">
        <div class="grid grid-cols-2 gap-6">
          <!-- File Upload Section -->
          <div class="bg-yale_blue-300 rounded-lg p-6 border border-yale_blue-400">
            <p class="text-lemon_chiffon-500 mb-4">Upload your resume to begin. The file will be processed and stored locally on your machine.</p>
            <div class="border-2 border-dashed border-yale_blue-400 rounded-lg p-8 text-center bg-yale_blue-300">
              <button onclick="window.handleFileSelect()" class="bg-tomato-500 text-white px-6 py-3 rounded-lg hover:bg-tomato-600 transition-colors">
                Choose File
              </button>
              <p class="mt-2 text-sm text-lemon_chiffon-400">PDF, DOCX, or TXT files accepted</p>
            </div>
          </div>

          <!-- Parsed Resume Section -->
          <div class="bg-yale_blue-300 rounded-lg p-6 border border-yale_blue-400">
            <div class="flex justify-between items-center mb-4">
              <h3 class="text-xl font-semibold text-naples_yellow-500">Parsed Resume</h3>
              <div>
                <button onclick="window.handleRefreshResumeData()" class="mr-2 text-sm text-lemon_chiffon-500 hover:text-lemon_chiffon-400">
                  ↻ Refresh
                </button>
                <button onclick="window.clearResumeData()" class="text-sm text-tomato-500 hover:text-tomato-600">
                  Clear
                </button>
              </div>
            </div>
            <div id="resume-data" class="bg-yale_blue-200 rounded-lg p-4 h-[300px] overflow-auto">
              <p class="text-lemon_chiffon-500 text-center">No resume loaded yet...</p>
            </div>
          </div>
        </div>
      </div>
    `,
    // ... (other submenu contents unchanged) ...
    'Enhance Resume': `
      <div class="max-w-2xl p-6">
        <p class="text-lemon_chiffon-500 mb-4">Generate tailored responses for job applications using AI assistance.</p>
        <div class="space-y-4">
          <div class="bg-yale_blue-300 p-4 rounded-lg border border-yale_blue-400">
            <h3 class="font-semibold text-naples_yellow-500">Target Job Title</h3>
            <input type="text" class="w-full mt-2 p-2 border border-yale_blue-500 rounded bg-yale_blue-200 text-lemon_chiffon-500" placeholder="e.g., Senior Software Engineer">
          </div>
          <div class="bg-yale_blue-300 p-4 rounded-lg border border-yale_blue-400">
            <h3 class="font-semibold text-naples_yellow-500">Company</h3>
            <input type="text" class="w-full mt-2 p-2 border border-yale_blue-500 rounded bg-yale_blue-200 text-lemon_chiffon-500" placeholder="e.g., Tech Corp">
          </div>
          <div class="bg-yale_blue-300 p-4 rounded-lg border border-yale_blue-400">
            <h3 class="font-semibold text-naples_yellow-500">Application Field</h3>
            <select class="w-full mt-2 p-2 border border-yale_blue-500 rounded bg-yale_blue-200 text-lemon_chiffon-500">
              <option>Cover Letter</option>
              <option>Professional Summary</option>
              <option>Work Experience</option>
              <option>Skills Description</option>
            </select>
          </div>
          <button class="bg-tomato-500 text-white px-6 py-3 rounded-lg hover:bg-tomato-600 transition-colors w-full">
            Generate Response
          </button>
        </div>
      </div>
    `,
    'Resume Context': `
      <div class="max-w-2xl p-6">
        <p class="text-lemon_chiffon-500 mb-4">Provide additional context to improve the AI-generated responses for your applications.</p>
        <div class="space-y-4">
          <div class="bg-yale_blue-300 p-4 rounded-lg border border-yale_blue-400">
            <h3 class="font-semibold text-naples_yellow-500">Career Level</h3>
            <select class="w-full mt-2 p-2 border border-yale_blue-500 rounded bg-yale_blue-200 text-lemon_chiffon-500">
              <option>Entry Level</option>
              <option>Mid Level</option>
              <option>Senior Level</option>
              <option>Executive</option>
            </select>
          </div>
          <div class="bg-yale_blue-300 p-4 rounded-lg border border-yale_blue-400">
            <h3 class="font-semibold text-naples_yellow-500">Key Skills</h3>
            <textarea class="w-full mt-2 p-2 border border-yale_blue-500 rounded bg-yale_blue-200 text-lemon_chiffon-500" rows="3" placeholder="Enter your key skills, separated by commas"></textarea>
          </div>
          <div class="bg-yale_blue-300 p-4 rounded-lg border border-yale_blue-400">
            <h3 class="font-semibold text-naples_yellow-500">Preferred Industries</h3>
            <textarea class="w-full mt-2 p-2 border border-yale_blue-500 rounded bg-yale_blue-200 text-lemon_chiffon-500" rows="2" placeholder="e.g., Technology, Healthcare, Finance"></textarea>
          </div>
        </div>
      </div>
    `,
    'Upload Application': `
      <div class="max-w-4xl p-6">
        <div class="grid grid-cols-2 gap-6">
          <!-- File Upload Section -->
          <div class="bg-yale_blue-300 rounded-lg p-6 border border-yale_blue-400">
            <p class="text-lemon_chiffon-500 mb-4">Upload your job application to begin. The file will be processed and stored locally on your machine.</p>
            <div class="border-2 border-dashed border-yale_blue-400 rounded-lg p-8 text-center bg-yale_blue-300">
              <button onclick="window.handleFileSelect()" class="bg-tomato-500 text-white px-6 py-3 rounded-lg hover:bg-tomato-600 transition-colors">
                Choose File
              </button>
              <p class="mt-2 text-sm text-lemon_chiffon-400">PDF, DOCX, or TXT files accepted</p>
            </div>
          </div>

          <!-- Extension Data Section -->
          <div class="bg-yale_blue-300 rounded-lg p-6 border border-yale_blue-400">
            <div class="flex justify-between items-center mb-4">
              <h3 class="text-xl font-semibold text-naples_yellow-500">Extension Data</h3>
              <div>
                <button onclick="window.handleRefreshData()" class="mr-2 text-sm text-lemon_chiffon-500 hover:text-lemon_chiffon-400">
                  ↻ Refresh
                </button>
                <button onclick="window.clearExtensionData()" class="text-sm text-tomato-500 hover:text-tomato-600">
                  Clear
                </button>
              </div>
            </div>
            <div id="extension-data" class="bg-yale_blue-200 rounded-lg p-4 h-[300px] overflow-auto">
              <p class="text-lemon_chiffon-500 text-center">Waiting for data from extension...</p>
            </div>
          </div>
        </div>
      </div>
    `,
    'Enhance Application': `
      <div class="max-w-4xl p-6">
        <div class="grid grid-cols-2 gap-6">
          <!-- Input Section -->
          <div class="space-y-4">
            <p class="text-lemon_chiffon-500 mb-4">Generate tailored improvements for your job application using AI assistance.</p>
            <div class="bg-yale_blue-300 p-4 rounded-lg border border-yale_blue-400">
              <h3 class="font-semibold text-naples_yellow-500">Application Type</h3>
              <select id="application-type" class="w-full mt-2 p-2 border border-yale_blue-500 rounded bg-yale_blue-200 text-lemon_chiffon-500">
                <option>Cover Letter</option>
                <option>Personal Statement</option>
                <option>Project Description</option>
                <option>Job Description Response</option>
              </select>
            </div>
            <div class="bg-yale_blue-300 p-4 rounded-lg border border-yale_blue-400">
              <h3 class="font-semibold text-naples_yellow-500">Company</h3>
              <input id="company" type="text" class="w-full mt-2 p-2 border border-yale_blue-500 rounded bg-yale_blue-200 text-lemon_chiffon-500" placeholder="e.g., Tech Corp">
            </div>
            <div class="bg-yale_blue-300 p-4 rounded-lg border border-yale_blue-400">
              <h3 class="font-semibold text-naples_yellow-500">Enhancement Focus</h3>
              <select id="enhancement-focus" class="w-full mt-2 p-2 border border-yale_blue-500 rounded bg-yale_blue-200 text-lemon_chiffon-500">
                <option>Clarity & Conciseness</option>
                <option>Professional Tone</option>
                <option>Keywords Optimization</option>
                <option>Impact & Achievement Focus</option>
              </select>
            </div>
            <button onclick="window.handleGenerateImprovements()" class="bg-tomato-500 text-white px-6 py-3 rounded-lg hover:bg-tomato-600 transition-colors w-full">
              Generate Improvements
            </button>
          </div>

          <!-- Response Section -->
          <div class="bg-yale_blue-300 rounded-lg p-6 border border-yale_blue-400">
            <div class="flex justify-between items-center mb-4">
              <h3 class="text-xl font-semibold text-naples_yellow-500">AI Response</h3>
              <div>
                <button onclick="window.clearAIResponse()" class="text-sm text-tomato-500 hover:text-tomato-600">
                  Clear
                </button>
              </div>
            </div>
            <div id="ai-response" class="bg-yale_blue-200 rounded-lg p-4 h-[400px] overflow-auto">
              <p class="text-lemon_chiffon-500 text-center">AI response will appear here...</p>
            </div>
          </div>
        </div>
      </div>
    `,
    'Application Context': `
      <div class="max-w-2xl p-6">
        <p class="text-lemon_chiffon-500 mb-4">Provide additional context to improve the AI-generated suggestions for your application materials.</p>
        <div class="space-y-4">
          <div class="bg-yale_blue-300 p-4 rounded-lg border border-yale_blue-400">
            <h3 class="font-semibold text-naples_yellow-500">Industry Focus</h3>
            <select class="w-full mt-2 p-2 border border-yale_blue-500 rounded bg-yale_blue-200 text-lemon_chiffon-500">
              <option>Technology</option>
              <option>Healthcare</option>
              <option>Finance</option>
              <option>Education</option>
              <option>Other</option>
            </select>
          </div>
          <div class="bg-yale_blue-300 p-4 rounded-lg border border-yale_blue-400">
            <h3 class="font-semibold text-naples_yellow-500">Target Keywords</h3>
            <textarea class="w-full mt-2 p-2 border border-yale_blue-500 rounded bg-yale_blue-200 text-lemon_chiffon-500" rows="3" placeholder="Enter relevant keywords for your application"></textarea>
          </div>
          <div class="bg-yale_blue-300 p-4 rounded-lg border border-yale_blue-400">
            <h3 class="font-semibold text-naples_yellow-500">Company Culture Notes</h3>
            <textarea class="w-full mt-2 p-2 border border-yale_blue-500 rounded bg-yale_blue-200 text-lemon_chiffon-500" rows="2" placeholder="Enter notes about the company culture and values"></textarea>
          </div>
        </div>
      </div>
    `,
    'API Key': `
      <div class="max-w-2xl p-6">
        <p class="text-lemon_chiffon-500 mb-4">Configure your OpenAI API settings for enhanced response generation.</p>
        <div class="space-y-4">
          <div class="bg-yale_blue-300 p-4 rounded-lg border border-yale_blue-400">
            <h3 class="font-semibold text-naples_yellow-500">OpenAI API Base URL</h3>
            <input type="text" id="api-base" class="w-full mt-2 p-2 border border-yale_blue-500 rounded bg-yale_blue-200 text-lemon_chiffon-500" placeholder="Enter your OpenAI API base URL (e.g., https://rgvaiclass.com/chat/api/v1)">
          </div>
          <div class="bg-yale_blue-300 p-4 rounded-lg border border-yale_blue-400">
            <h3 class="font-semibold text-naples_yellow-500">OpenAI API Key</h3>
            <input type="password" id="api-key" class="w-full mt-2 p-2 border border-yale_blue-500 rounded bg-yale_blue-200 text-lemon_chiffon-500" placeholder="Enter your OpenAI API key">
            <p class="mt-2 text-sm text-lemon_chiffon-400">Your API settings are stored locally and used only for generating responses.</p>
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
};

window.handleSubmenu = (submenu) => {
  currentSubmenu = submenu;
  document.querySelector('#app').innerHTML = renderContent();
  if (submenu === 'Upload Application') {
    setTimeout(() => {
      window.handleRefreshData();
    }, 500);
  } else if (submenu === 'Upload Resume') {
    setTimeout(() => {
      window.handleRefreshResumeData();
    }, 500);
  }
};

// Add file selection handler
window.handleFileSelect = () => {
  const fileInput = createFileInput();
  document.body.appendChild(fileInput);
  fileInput.click();
  fileInput.addEventListener('change', () => {
    setTimeout(() => {
      document.body.removeChild(fileInput);
    }, 1000);
  });
};

window.handleApplyAPISettings = async () => {
  const apiBase = document.getElementById('api-base').value;
  const apiKey = document.getElementById('api-key').value;

  try {
    if (apiKey) {
      ai_service.init_openai(apiKey, apiBase);
      alert('API settings updated successfully!');
    }
  } catch (error) {
    console.error('Error updating API settings:', error);
    alert('Error updating API settings. Please check your connection.');
  }
};

window.clearExtensionData = () => {
  const dataContainer = document.getElementById('extension-data');
  if (dataContainer) {
    dataContainer.innerHTML = '<p class="text-lemon_chiffon-500 text-center">Waiting for data from extension...</p>';
  }
};

window.clearResumeData = () => {
  const dataContainer = document.getElementById('resume-data');
  if (dataContainer) {
    dataContainer.innerHTML = '<p class="text-lemon_chiffon-500 text-center">No resume loaded yet...</p>';
  }
};

window.handleExtensionData = (data) => {
  console.log("handleExtensionData called with:", data);
  const dataContainer = document.getElementById('extension-data');
  console.log("dataContainer found:", !!dataContainer);
  
  if (dataContainer && data.display_text) {
    console.log("Updating container HTML");
    const metrics = data.metadata;
    
    dataContainer.innerHTML = `
      <div class="text-lemon_chiffon-500">
        <div class="mb-4 grid grid-cols-2 gap-4">
          <div>
            <span class="font-semibold">Words:</span> ${metrics.word_count}
            <span class="ml-4 font-semibold">Paragraphs:</span> ${metrics.paragraph_count}
          </div>
          <div>
            <span class="font-semibold">Sentences:</span> ${metrics.sentence_count}
            <span class="ml-4 font-semibold">Read Time:</span> ${metrics.estimated_read_time}m
          </div>
        </div>
        <div class="whitespace-pre-wrap font-mono text-sm bg-yale_blue-300 p-4 rounded-lg max-h-[400px] overflow-y-auto">
          ${data.display_text}
        </div>
      </div>
    `;
  } else {
    dataContainer.innerHTML = '<p class="text-lemon_chiffon-500 text-center">No data available</p>';
  }
};

window.handleRefreshData = async () => {
  try {
    const dataContainer = document.getElementById('extension-data');
    if (!dataContainer) {
      console.log("No extension-data container found");
      return;
    }

    console.log("Fetching latest extraction...");
    const response = await fetch('http://localhost:8000/api/application/last_extract');
    const data = await response.json();
    console.log("GET last_extract full response:", JSON.stringify(data, null, 2));
    
    if (data.status === 'success' && data.display_text) {
      console.log("Updating UI with data");
      window.handleExtensionData(data);
    } else {
      console.log("Data not in expected format:", data);
      dataContainer.innerHTML = `<p class="text-lemon_chiffon-500 text-center">
        ${data.message || 'No data available'}
      </p>`;
    }
  } catch (error) {
    console.error('Error fetching data:', error);
  }
};

// New function to handle parsed resume data
window.handleResumeData = (data) => {
  console.log("handleResumeData called with:", data);
  const dataContainer = document.getElementById('resume-data');
  console.log("dataContainer found:", !!dataContainer);
  
  if (dataContainer && data.parsed_sections) {
    console.log("Updating resume data container HTML");
    const metrics = data.metadata;
    
    dataContainer.innerHTML = `
      <div class="text-lemon_chiffon-500">
        <div class="mb-4 grid grid-cols-2 gap-4">
          <div>
            <span class="font-semibold">Words:</span> ${metrics.word_count}
            <span class="ml-4 font-semibold">Read Time:</span> ${metrics.estimated_read_time}m
          </div>
          <div>
            <span class="font-semibold">Sentences:</span> ${metrics.sentence_count}
          </div>
        </div>
        <div class="whitespace-pre-wrap font-mono text-sm bg-yale_blue-300 p-4 rounded-lg max-h-[400px] overflow-y-auto">
          ${JSON.stringify(data.parsed_sections, null, 2)}
        </div>
      </div>
    `;
  } else {
    dataContainer.innerHTML = '<p class="text-lemon_chiffon-500 text-center">No resume loaded yet...</p>';
  }
};

// New function to refresh parsed resume data
window.handleRefreshResumeData = async () => {
  try {
    const dataContainer = document.getElementById('resume-data');
    if (!dataContainer) {
      console.log("No resume-data container found");
      return;
    }

    console.log("Fetching latest resume upload...");
    const response = await fetch('http://localhost:8000/api/resume/upload', {
      method: 'GET'
    });
    const data = await response.json();
    console.log("GET last_upload full response:", JSON.stringify(data, null, 2));
    
    if (data.status === 'success' && data.parsed_sections) {
      console.log("Updating UI with resume data");
      window.handleResumeData(data);
    } else {
      console.log("Data not in expected format:", data);
      dataContainer.innerHTML = `<p class="text-lemon_chiffon-500 text-center">
        ${data.message || 'No resume loaded yet...'}
      </p>`;
    }
  } catch (error) {
    console.error('Error fetching resume data:', error);
  }
};

window.clearAIResponse = () => {
  const responseContainer = document.getElementById('ai-response');
  if (responseContainer) {
    responseContainer.innerHTML = '<p class="text-lemon_chiffon-500 text-center">AI response will appear here...</p>';
  }
};

window.handleGenerateImprovements = async () => {
  try {
    const extensionResponse = await fetch('http://localhost:8000/api/application/last_extract');
    const extensionData = await extensionResponse.json();
    if (!extensionData.display_text) {
      throw new Error('No extension data available. Please upload an application first.');
    }

    const resumeResponse = await fetch('http://localhost:8000/api/resume/last_upload', { method: 'GET' });
    const resumeData = await resumeResponse.json();
    if (!resumeData.content) {
      throw new Error('No resume data available. Please upload a resume first.');
    }

    const applicationType = document.getElementById('application-type').value;
    const company = document.getElementById('company').value;
    const enhancementFocus = document.getElementById('enhancement-focus').value;

    const requestBody = {
      application_type: applicationType,
      company: company,
      enhancement_focus: enhancementFocus,
      resume_content: resumeData.content,
      application_content: extensionData.display_text
    };

    const response = await fetch('http://localhost:8000/api/application/enhance', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(requestBody)
    });

    const result = await response.json();
    if (result.status === 'success') {
      const aiResponse = document.getElementById('ai-response');
      if (aiResponse) {
        aiResponse.innerHTML = `
          <div class="text-lemon_chiffon-500">
            <div class="whitespace-pre-wrap font-mono text-sm bg-yale_blue-300 p-4 rounded-lg max-h-[400px] overflow-y-auto">
              ${result.enhanced_content}
            </div>
          </div>
        `;
      }
    } else {
      throw new Error(result.message || 'Failed to generate improvements');
    }
  } catch (error) {
    console.error('Error generating improvements:', error);
    alert(`Error generating improvements: ${error.message}`);
  }
};

// Initial render
document.querySelector('#app').innerHTML = renderContent();