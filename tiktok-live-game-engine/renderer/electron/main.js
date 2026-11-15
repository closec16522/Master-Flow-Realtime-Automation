/**
 * Module 6: Graphic & Scene Rendering Engine (Electron Transparent Window)
 * รองรับ Windows / Mac สำหรับใช้ Window Capture หรือ Game Capture เข้า OBS และ TikTok LIVE Studio
 */

const { app, BrowserWindow, ipcMain } = require('electron');

let mainWindow = null;

function createTransparentOverlay() {
  mainWindow = new BrowserWindow({
    width: 540,
    height: 960, // อัตราส่วน 9:16 สำหรับ TikTok Live
    transparent: true,
    frame: false,
    alwaysOnTop: true,
    hasShadow: false,
    resizable: true,
    backgroundColor: '#00000000',
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true
    }
  });

  // โหลดหน้า WebGL Renderer (รองรับทั้งโหมด Dev และ Production build)
  const targetUrl = process.env.RENDERER_URL || 'http://127.0.0.1:3333/live-scene?transparent=1';
  mainWindow.loadURL(targetUrl);

  // เปิดใช้งาน Click-Through (ไม่บังเมาส์ขณะเล่นเกมหรือกดปุ่มบนหน้าจอ)
  ipcMain.on('toggle-click-through', (_event, ignore) => {
    mainWindow?.setIgnoreMouseEvents(Boolean(ignore), { forward: true });
  });
}

app.whenReady().then(createTransparentOverlay);
app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit();
});
