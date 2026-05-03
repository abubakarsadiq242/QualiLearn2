// Register Service Worker
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('./sw.js')
      .then((registration) => {
        console.log('[PWA] Service Worker registered with scope:', registration.scope);
      })
      .catch((error) => {
        console.error('[PWA] Service Worker registration failed:', error);
      });
  });
}

// Handle Install Prompt
let deferredPrompt;

window.addEventListener('beforeinstallprompt', (e) => {
  // Prevent the mini-infobar from appearing on mobile
  e.preventDefault();
  // Stash the event so it can be triggered later.
  deferredPrompt = e;
  
  // Show the custom install UI
  showInstallPromotion();
});

function showInstallPromotion() {
  // Don't show if already created
  if (document.getElementById('pwa-install-banner')) return;

  const banner = document.createElement('div');
  banner.id = 'pwa-install-banner';
  banner.style.cssText = `
    position: fixed;
    bottom: 20px;
    left: 50%;
    transform: translateX(-50%);
    width: 90%;
    max-width: 400px;
    background: white;
    border-radius: 16px;
    box-shadow: 0 10px 40px rgba(0,0,0,0.2);
    padding: 1.5rem;
    z-index: 9999;
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    border: 2px solid #4f46e5;
    animation: slideUp 0.5s ease;
  `;

  banner.innerHTML = `
    <style>
      @keyframes slideUp { from { bottom: -100px; opacity: 0; } to { bottom: 20px; opacity: 1; } }
    </style>
    <div style="display: flex; align-items: center; justify-content: center; width: 60px; height: 60px; background: #e0e7ff; border-radius: 12px; margin-bottom: 1rem;">
        <img src="./image/mylogo.png" alt="Icon" style="max-width: 40px;">
    </div>
    <h5 style="font-family: 'Outfit', sans-serif; font-weight: 700; color: #1e293b; margin-bottom: 0.5rem;">Install QualiLearn</h5>
    <p style="font-family: 'Inter', sans-serif; color: #64748b; font-size: 0.9rem; margin-bottom: 1.25rem;">Get the mobile app experience on your home screen for faster access.</p>
    <div style="display: flex; gap: 10px; width: 100%;">
        <button id="pwa-dismiss-btn" style="flex: 1; padding: 10px; border: none; background: #f1f5f9; color: #64748b; border-radius: 8px; font-weight: 600; cursor: pointer;">Not Now</button>
        <button id="pwa-install-btn" style="flex: 1; padding: 10px; border: none; background: #4f46e5; color: white; border-radius: 8px; font-weight: 600; cursor: pointer; box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3);">Install App</button>
    </div>
  `;

  document.body.appendChild(banner);

  document.getElementById('pwa-dismiss-btn').addEventListener('click', () => {
    banner.style.display = 'none';
  });

  document.getElementById('pwa-install-btn').addEventListener('click', async () => {
    // Hide our user interface that shows our A2HS button
    banner.style.display = 'none';
    // Show the prompt
    if (deferredPrompt) {
        deferredPrompt.prompt();
        // Wait for the user to respond to the prompt
        const { outcome } = await deferredPrompt.userChoice;
        console.log(`[PWA] User response to the install prompt: ${outcome}`);
        // We've used the prompt, and can't use it again, throw it away
        deferredPrompt = null;
    }
  });
}

window.addEventListener('appinstalled', () => {
  // Hide the app-provided install promotion
  const banner = document.getElementById('pwa-install-banner');
  if (banner) banner.style.display = 'none';
  // Clear the deferredPrompt so it can be garbage collected
  deferredPrompt = null;
  console.log('[PWA] QualiLearn was installed successfully.');
});
