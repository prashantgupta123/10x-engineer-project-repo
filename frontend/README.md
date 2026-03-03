# PromptLab Frontend

React + Vite frontend for the PromptLab AI Prompt Engineering Platform.

## Setup

```bash
# Install dependencies
npm install

# Start development server
npm run dev
```

The app runs on `http://localhost:3000` and proxies API requests to `http://localhost:8000`.

**Important:** Make sure the backend is running before starting the frontend.

## Project Structure

```
src/
├── api/
│   └── client.js          # API client for backend communication
├── components/
│   ├── Button.jsx         # Reusable button component
│   ├── Modal.jsx          # Modal dialog component
│   ├── PromptCard.jsx     # Individual prompt display
│   ├── PromptForm.jsx     # Create/edit prompt form
│   ├── PromptList.jsx     # Prompts list with filters
│   └── CollectionList.jsx # Collections management
├── hooks/
│   └── useData.js         # Custom hooks for data fetching
├── App.jsx                # Main application component
├── App.css                # Application styles
└── main.jsx               # Entry point
```

## Features

- ✅ Create, edit, and delete prompts
- ✅ Organize prompts into collections
- ✅ Search and filter prompts
- ✅ Responsive grid layout
- ✅ Modal-based forms
- ✅ Real-time updates

## API Integration

All API calls are proxied through Vite's dev server:
- Frontend: `http://localhost:3000`
- Backend API: `http://localhost:8000`
- Proxy: `/api/*` → `http://localhost:8000/*`

## Development

```bash
# Run dev server with hot reload
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Lint code
npm run lint
```
