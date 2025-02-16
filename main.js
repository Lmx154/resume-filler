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

function getSubmenuContent(submenu) {
  const contents = {
    'Upload Resume': `
      <div class="max-w-2xl p-6">
        <p class="text-lemon_chiffon-500 mb-4">Upload your resume to begin. The file will be processed and stored locally on your machine.</p>
        <div class="border-2 border-dashed border-yale_blue-400 rounded-lg p-8 text-center bg-yale_blue-300">
          <button class="bg-tomato-500 text-white px-6 py-3 rounded-lg hover:bg-tomato-600 transition-colors">
            Choose File
          </button>
          <p class="mt-2 text-sm text-lemon_chiffon-400">PDF, DOCX, or TXT files accepted</p>
        </div>
      </div>
    `,
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
    'API Key': `
      <div class="max-w-2xl p-6">
        <p class="text-lemon_chiffon-500 mb-4">Configure your OpenAI API key for enhanced response generation.</p>
        <div class="bg-yale_blue-300 p-4 rounded-lg border border-yale_blue-400">
          <h3 class="font-semibold text-naples_yellow-500">OpenAI API Key</h3>
          <input type="password" class="w-full mt-2 p-2 border border-yale_blue-500 rounded bg-yale_blue-200 text-lemon_chiffon-500" placeholder="Enter your OpenAI API key">
          <p class="mt-2 text-sm text-lemon_chiffon-400">Your API key is stored locally and used only for generating responses.</p>
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
};

// Initial render
document.querySelector('#app').innerHTML = renderContent();