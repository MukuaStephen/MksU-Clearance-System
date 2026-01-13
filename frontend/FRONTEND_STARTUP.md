# 🚀 Frontend Startup Guide

## Quick Start (3 Steps)

### Step 1: Navigate to Frontend Directory
```powershell
cd FRONTEND
```

### Step 2: Install Dependencies (First Time Only)
```powershell
npm install
```

### Step 3: Start the Development Server
```powershell
npm start
```

That's it! The frontend will automatically open at **http://localhost:4200/**

---

## 📍 Access Points

Once running, you can access:

| What | URL |
|------|-----|
| **Frontend App** | http://localhost:4200/ |
| **Backend API** | http://localhost:8000/ |
| **API Docs** | http://localhost:8000/api/docs/ |

---

## 🔧 Alternative: Using Angular CLI Directly

If you want more control over the port or settings:

```powershell
cd FRONTEND
npx ng serve --port 4200 --open
```

Options:
- `--port 4200` - Run on specific port (default is 4200)
- `--open` - Auto-open in browser
- `--host 0.0.0.0` - Allow external access
- `--ssl` - Run with HTTPS

---

## ⚡ Command Reference

| Command | Purpose |
|---------|---------|
| `npm start` | Start dev server (port 4200) |
| `npm run build` | Build for production |
| `npm test` | Run unit tests |
| `npm run watch` | Watch mode for development |
| `npx ng serve` | Start server (with options) |
| `npx ng generate component name` | Create new component |
| `npx ng generate service name` | Create new service |

---

## ✅ Verification

Once running, verify with these checks:

### 1. Frontend is Loading
```powershell
curl http://localhost:4200/
```

### 2. Backend is Running (In Another Terminal)
```powershell
curl http://localhost:8000/api/health/
```

### 3. Check Browser Console
1. Open http://localhost:4200/
2. Press **F12** to open DevTools
3. Go to **Console** tab
4. Check for any errors (red text)

---

## 🛑 Troubleshooting

### "npm: command not found"
**Solution:** Node.js not installed. Download from https://nodejs.org/

### "Port 4200 already in use"
**Solution:** Use a different port:
```powershell
npx ng serve --port 4300
```

### "Angular CLI not found"
**Solution:** Run npm install first:
```powershell
npm install
```

### "Cannot find module"
**Solution:** Dependencies not installed:
```powershell
npm install
```

### Frontend won't connect to backend
**Solution:** Check CORS in `BACKEND/config/settings.py`:
```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:4200",  # Make sure this is here
    "http://localhost:3000",
]
```

---

## 🎯 What to Expect

When you run `npm start`:

1. Angular CLI builds the project
2. Dev server starts on port 4200
3. Browser opens to http://localhost:4200/
4. You should see the **Login Page**

### First Load Takes ~5-10 seconds

The terminal will show:
```
✔ Compiled successfully.
NOTE: Raw file sizes do not reflect development server per-request transformations.

                    | Initial total |  17.16 kB

Watch mode enabled. Watching for file changes...
NOTE: Raw file sizes do not reflect development server per-request transformations.
➜  Local:   http://localhost:4200/
```

This means it's ready! ✅

---

## 📝 Keep Terminal Open

**Important:** Keep the terminal running while developing!
- If you close it, the dev server stops
- Changes to code auto-reload in browser

To stop the server, press **Ctrl+C** in the terminal.

---

## 🔄 Hot Reload

Angular's dev server has hot reload built-in:
1. Edit any `.ts`, `.html`, or `.css` file
2. Save the file (Ctrl+S)
3. Browser auto-refreshes with your changes
4. **No need to restart the server!**

---

## 📂 Project Structure

```
FRONTEND/
├── src/
│   ├── main.ts              # App entry point
│   ├── app/
│   │   ├── app.routes.ts    # Route configuration
│   │   ├── app.config.ts    # App configuration
│   │   ├── student-login/   # Login component
│   │   └── student-dashboard/  # Dashboard component
│   ├── index.html           # HTML template
│   └── styles.css           # Global styles
│
├── angular.json             # Angular CLI config
├── package.json             # Dependencies
├── tsconfig.json            # TypeScript config
└── node_modules/            # Installed packages
```

---

## 🎨 Development Workflow

1. **Start server**
   ```powershell
   npm start
   ```

2. **Open browser**
   ```
   http://localhost:4200/
   ```

3. **Edit code** in your editor

4. **Watch for auto-refresh** in browser

5. **Check Console** (F12) for errors

6. **Test API** using http://localhost:8000/api/docs/

---

## 💡 Pro Tips

### View Network Requests
1. Open DevTools (F12)
2. Go to **Network** tab
3. Perform actions in the app
4. See API calls to `http://localhost:8000/api/...`

### Debug Variables
1. Open DevTools (F12)
2. Go to **Console** tab
3. Type variable names to inspect

### Check Stored Data
1. Open DevTools (F12)
2. Go to **Application** tab
3. Expand **Local Storage**
4. See stored tokens and data

### Device View
1. Press **F12**
2. Click the device icon (top-left)
3. See mobile/tablet view

---

## 🚀 Next Steps After Starting Frontend

1. **Test the Login**
   - See if the login form appears
   - Check browser console (F12) for errors

2. **Connect to Backend**
   - Create HTTP service to call backend
   - Add JWT token management
   - Integrate API calls in components

3. **Build Features**
   - Clearance request form
   - Status tracking
   - Department dashboard

4. **Style the UI**
   - Add CSS/Bootstrap
   - Improve layout
   - Make it responsive

---

**Ready to go!** 🎉

Run `npm start` and your frontend will be live at http://localhost:4200/
