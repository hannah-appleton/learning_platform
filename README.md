# Adaptive Learning Platform

An AI-powered adaptive learning platform that generates personalized lessons and quizzes using the Anthropic Messages API. The project is built with [Vite](https://vitejs.dev/), [React](https://react.dev/), and [Tailwind CSS](https://tailwindcss.com/).

## Features

- Guided onboarding flow that captures subject, skill level, and learning style preferences
- Dynamic lesson generation tailored to the learner's profile
- Rich markdown rendering with syntax highlighting for code blocks
- Quiz generation with real-time progress tracking
- Tailwind CSS styling with typography enhancements

## Getting Started

### Prerequisites

- [Node.js](https://nodejs.org/) 18 or later
- An Anthropic API key with access to the Messages API

### Installation

```bash
npm install
```

### Environment Variables

Copy `.env.example` to `.env` and fill in your Anthropic credentials.

```bash
cp .env.example .env
```

Required variables:

- `VITE_ANTHROPIC_API_KEY`: Your Anthropic API key
- `VITE_ANTHROPIC_MODEL`: The Claude model to use (defaults to `claude-3-5-sonnet-20240620`)
- `VITE_ANTHROPIC_API_VERSION`: API version header (defaults to `2023-06-01`)

### Development Server

```bash
npm run dev
```

Visit [http://localhost:5173](http://localhost:5173) to access the app.

### Build for Production

```bash
npm run build
```

### Preview Production Build

```bash
npm run preview
```

## Project Structure

```
.
├── .env.example
├── index.html
├── package.json
├── postcss.config.js
├── tailwind.config.js
├── vite.config.js
└── src
    ├── App.jsx
    ├── index.css
    ├── main.jsx
    └── components
        └── AdaptiveLearningPlatform.jsx
```

## License

This project is licensed under the MIT License.
