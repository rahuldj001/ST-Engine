# AI Startup Feasibility Engine - Frontend

A modern, futuristic landing page with glassmorphism design for the AI Startup Feasibility Engine.

## 🎨 Design Features

### Visual Design
- **Glassmorphism UI**: Frosted glass effects with backdrop blur
- **Gradient Orbs**: Animated floating gradient backgrounds
- **Modern Typography**: Inter font family for clean, professional look
- **Responsive Design**: Mobile-first approach, works on all devices
- **Smooth Animations**: CSS animations and transitions throughout

### Key Sections
1. **Hero Section**: Eye-catching introduction with CTA and stats
2. **Features Grid**: 6 key features with gradient icons
3. **How It Works**: 3-step process visualization
4. **Analysis Form**: Interactive form to submit startup ideas
5. **Results Modal**: Beautiful display of feasibility reports

## 🚀 Quick Start

### Option 1: Direct File Opening
Simply open `index.html` in your browser:
```bash
# Windows
start index.html

# Mac
open index.html

# Linux
xdg-open index.html
```

### Option 2: Local Server (Recommended)
Using Python's built-in server:
```bash
# Python 3
python -m http.server 8080

# Then open: http://localhost:8080
```

Using Node.js:
```bash
# Install http-server globally
npm install -g http-server

# Run server
http-server -p 8080

# Then open: http://localhost:8080
```

## 🔌 Backend Integration

The frontend connects to the FastAPI backend at `http://localhost:8000` by default.

### Update API URL
Edit `script.js` line 2:
```javascript
const API_BASE_URL = 'http://localhost:8000';  // Change this to your backend URL
```

### Required Backend Endpoints
- `POST /api/analyze` - Submit startup idea for analysis
- `GET /health` - Check API status

## 📁 File Structure

```
frontend/
├── index.html       # Main HTML file
├── styles.css       # Core styles with glassmorphism
├── results.css      # Results modal and notification styles
├── script.js        # JavaScript for interactivity
└── README.md        # This file
```

## 🎯 Features

### Interactive Elements
- ✅ Smooth scroll navigation
- ✅ Mobile responsive menu
- ✅ Form validation
- ✅ Loading states with progress indicators
- ✅ Results modal with tabbed interface
- ✅ Download report functionality
- ✅ Toast notifications
- ✅ Scroll animations

### Glassmorphism Effects
- Frosted glass cards
- Backdrop blur filters
- Semi-transparent backgrounds
- Subtle borders and shadows
- Gradient overlays

### Color Palette
- **Primary**: Purple gradient (#667eea → #764ba2)
- **Secondary**: Pink gradient (#f093fb → #f5576c)
- **Accent**: Cyan gradient (#4facfe → #00f2fe)
- **Success**: Green gradient (#43e97b → #38f9d7)
- **Background**: Dark navy (#0a0e27)

## 🎨 Customization

### Change Colors
Edit CSS variables in `styles.css`:
```css
:root {
    --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    --secondary-gradient: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    /* ... more variables */
}
```

### Modify Content
All content is in `index.html`. Key sections:
- Hero title and description
- Feature cards
- How it works steps
- Footer information

### Adjust Animations
Animation timings in `styles.css`:
```css
@keyframes float {
    /* Modify animation behavior */
}
```

## 📱 Responsive Breakpoints

- **Desktop**: > 1024px
- **Tablet**: 768px - 1024px
- **Mobile**: < 768px

## 🌐 Browser Support

- ✅ Chrome (latest)
- ✅ Firefox (latest)
- ✅ Safari (latest)
- ✅ Edge (latest)
- ⚠️ IE11 (limited support, no backdrop-filter)

## 🔧 Development

### Testing Locally
1. Start the backend server:
   ```bash
   cd ..
   uvicorn main:app --reload
   ```

2. Start the frontend server:
   ```bash
   python -m http.server 8080
   ```

3. Open http://localhost:8080

### Debugging
- Open browser DevTools (F12)
- Check Console for API status
- Network tab shows API requests
- Easter egg in console! 🥚

## 📊 Performance

- Optimized CSS with minimal reflows
- Lazy loading for images (if added)
- Efficient animations using transform/opacity
- Minimal JavaScript bundle size

## 🎭 Animations

### On Load
- Hero content slides up
- Stats fade in
- Dashboard preview slides from right

### On Scroll
- Feature cards fade in
- Step cards animate
- Intersection Observer for performance

### On Interaction
- Button hover effects
- Card hover lift
- Form focus states
- Modal transitions

## 🚀 Deployment

### Static Hosting
Deploy to any static hosting service:

**Netlify**:
```bash
# Drag and drop the frontend folder
# Or use Netlify CLI
netlify deploy --dir=frontend
```

**Vercel**:
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
cd frontend
vercel
```

**GitHub Pages**:
```bash
# Push to GitHub
git add frontend/
git commit -m "Add frontend"
git push

# Enable GitHub Pages in repo settings
```

### Update API URL for Production
```javascript
const API_BASE_URL = 'https://your-api-domain.com';
```

## 🎨 Design Credits

- **Font**: Inter by Rasmus Andersson
- **Icons**: Custom SVG icons
- **Color Inspiration**: Modern gradient palettes
- **Design Style**: Glassmorphism + Futuristic minimal

## 📝 License

Part of the AI Startup Feasibility Engine project.

## 🤝 Contributing

Suggestions for UI improvements are welcome!

---

**Built with ❤️ using modern web technologies**
