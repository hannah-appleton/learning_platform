# Adaptive Learning Platform

A browser-based adaptive learning experience that generates personalised lessons and quizzes with the Anthropic Messages API. The entire interface runs directly in the browser using React, Tailwind via the CDN build and Babel Standalone—no build tooling or package installation required.

## Features

- Guided onboarding flow to capture the learner's subject, skill level, and preferred learning style
- AI-generated lessons with rich markdown rendering, inline code blocks and styled takeaways
- Automatically generated practice questions with instant feedback and progress tracking
- Local persistence of your Anthropic API key and preferred model in the browser's storage
- Responsive Tailwind UI that works on desktops and tablets without additional setup

## Getting Started

1. Clone or download this repository.
2. Open `index.html` in a modern browser **or** serve the project folder with any static file server (for example: `python -m http.server 8000`).
3. Enter your Anthropic API key and preferred model in the onboarding form. The key is stored locally in your browser so you only need to enter it once per device.

That’s it—no `npm install`, build steps, or environment files are required.

## Development Tips

- The UI relies on the Tailwind Play CDN. If you customize class names heavily, ensure they are present in the rendered markup so Tailwind can detect them at runtime.
- The code lives entirely inside `index.html` under a `<script type="text/babel">` block. Babel Standalone transpiles the JSX in the browser, which keeps the repository lightweight while preserving a familiar React authoring experience.
- To clear stored Anthropic credentials, remove them from the onboarding form or clear localStorage for the site.

## Project Structure

```
.
├── .gitignore
├── LICENSE
├── README.md
├── index.html
└── package.json
```

## License

This project is licensed under the MIT License. See [`LICENSE`](LICENSE) for details.
