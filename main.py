import React, { useState } from 'react';
import { BookOpen, Brain, CheckCircle, ArrowRight, Sparkles, Target, Zap } from 'lucide-react';

export default function AdaptiveLearningPlatform() {
  const [screen, setScreen] = useState('setup'); // setup, learning, quiz, complete
  const [subject, setSubject] = useState('');
  const [skillLevel, setSkillLevel] = useState('beginner');
  const [learningStyle, setLearningStyle] = useState('balanced');
  const [currentLesson, setCurrentLesson] = useState(null);
  const [lessonHistory, setLessonHistory] = useState([]);
  const [quizData, setQuizData] = useState(null);
  const [userAnswer, setUserAnswer] = useState('');
  const [loading, setLoading] = useState(false);
  const [progress, setProgress] = useState(0);

  // Simple markdown renderer
  const renderMarkdown = (text) => {
    if (!text) return null;
   
    const elements = [];
    let i = 0;
    const lines = text.split('\n');
   
    const processInlineMarkdown = (text) => {
      const parts = [];
      let currentText = text;
      let key = 0;
     
      // Process inline code first: `code`
      const inlineCodeRegex = /`([^`]+)`/g;
      let lastIndex = 0;
      let match;
     
      while ((match = inlineCodeRegex.exec(currentText)) !== null) {
        // Add text before code
        if (match.index > lastIndex) {
          const beforeText = currentText.substring(lastIndex, match.index);
          // Process bold in the text before
          parts.push(...processBold(beforeText, key++));
        }
        // Add inline code
        parts.push(
          <code key={`code-${key++}`} className="bg-gray-100 px-2 py-0.5 rounded text-sm font-mono text-purple-700">
            {match[1]}
          </code>
        );
        lastIndex = match.index + match[0].length;
      }
     
      // Add remaining text
      if (lastIndex < currentText.length) {
        const remainingText = currentText.substring(lastIndex);
        parts.push(...processBold(remainingText, key++));
      }
     
      return parts.length > 0 ? parts : text;
    };
   
    const processBold = (text, startKey = 0) => {
      const parts = [];
      const boldRegex = /(\*\*|__)(.*?)\1/g;
      let lastIndex = 0;
      let match;
      let key = startKey;
     
      while ((match = boldRegex.exec(text)) !== null) {
        if (match.index > lastIndex) {
          parts.push(text.substring(lastIndex, match.index));
        }
        parts.push(<strong key={`bold-${key++}`} className="font-semibold">{match[2]}</strong>);
        lastIndex = match.index + match[0].length;
      }
     
      if (lastIndex < text.length) {
        parts.push(text.substring(lastIndex));
      }
     
      return parts.length > 0 ? parts : [text];
    };
   
    while (i < lines.length) {
      const line = lines[i];
      const trimmedLine = line.trim();
     
      // Code blocks: ```language
      if (trimmedLine.startsWith('```')) {
        const language = trimmedLine.substring(3).trim();
        const codeLines = [];
        i++;
       
        while (i < lines.length && !lines[i].trim().startsWith('```')) {
          codeLines.push(lines[i]);
          i++;
        }
       
        elements.push(
          <div key={`code-block-${elements.length}`} className="mb-4">
            {language && (
              <div className="bg-gray-700 text-gray-300 text-xs px-4 py-2 rounded-t-lg font-mono">
                {language}
              </div>
            )}
            <pre className={`bg-gray-800 text-gray-100 p-4 ${language ? 'rounded-b-lg' : 'rounded-lg'} overflow-x-auto`}>
              <code className="text-sm font-mono">{codeLines.join('\n')}</code>
            </pre>
          </div>
        );
        i++; // Skip closing ```
        continue;
      }
     
      // Headers
      if (trimmedLine.startsWith('###')) {
        elements.push(
          <h3 key={`h3-${elements.length}`} className="text-lg font-semibold text-gray-800 mt-6 mb-3">
            {processInlineMarkdown(trimmedLine.replace(/^###\s*/, ''))}
          </h3>
        );
      } else if (trimmedLine.startsWith('##')) {
        elements.push(
          <h2 key={`h2-${elements.length}`} className="text-xl font-semibold text-gray-800 mt-6 mb-3">
            {processInlineMarkdown(trimmedLine.replace(/^##\s*/, ''))}
          </h2>
        );
      } else if (trimmedLine.startsWith('#')) {
        elements.push(
          <h1 key={`h1-${elements.length}`} className="text-2xl font-semibold text-gray-800 mt-6 mb-4">
            {processInlineMarkdown(trimmedLine.replace(/^#\s*/, ''))}
          </h1>
        );
      }
      // List items
      else if (trimmedLine.match(/^[-*•]\s/)) {
        const listItems = [];
        while (i < lines.length && lines[i].trim().match(/^[-*•]\s/)) {
          listItems.push(lines[i].trim().replace(/^[-*•]\s/, ''));
          i++;
        }
        elements.push(
          <ul key={`list-${elements.length}`} className="list-disc pl-6 mb-4 space-y-2">
            {listItems.map((item, idx) => (
              <li key={idx} className="text-gray-700">{processInlineMarkdown(item)}</li>
            ))}
          </ul>
        );
        continue;
      }
      // Numbered lists
      else if (trimmedLine.match(/^\d+\.\s/)) {
        const listItems = [];
        while (i < lines.length && lines[i].trim().match(/^\d+\.\s/)) {
          listItems.push(lines[i].trim().replace(/^\d+\.\s/, ''));
          i++;
        }
        elements.push(
          <ol key={`olist-${elements.length}`} className="list-decimal pl-6 mb-4 space-y-2">
            {listItems.map((item, idx) => (
              <li key={idx} className="text-gray-700">{processInlineMarkdown(item)}</li>
            ))}
          </ol>
        );
        continue;
      }
      // Empty line
      else if (trimmedLine === '') {
        elements.push(<div key={`space-${elements.length}`} className="h-4"></div>);
      }
      // Regular paragraph
      else if (trimmedLine.length > 0) {
        elements.push(
          <p key={`p-${elements.length}`} className="text-gray-700 mb-4 leading-relaxed">
            {processInlineMarkdown(trimmedLine)}
          </p>
        );
      }
     
      i++;
    }
   
    return <div>{elements}</div>;
  };

  const learningStyles = [
    { id: 'visual', name: 'Visual', icon: '👁️', description: 'Diagrams, examples, and visual explanations' },
    { id: 'practical', name: 'Practical', icon: '🛠️', description: 'Hands-on exercises and real-world applications' },
    { id: 'theoretical', name: 'Theoretical', icon: '📚', description: 'Deep concepts and theoretical foundations' },
    { id: 'balanced', name: 'Balanced', icon: '⚖️', description: 'Mix of theory, examples, and practice' }
  ];

  const skillLevels = [
    { id: 'beginner', name: 'Beginner', description: 'New to this topic' },
    { id: 'intermediate', name: 'Intermediate', description: 'Some familiarity' },
    { id: 'advanced', name: 'Advanced', description: 'Strong foundation' }
  ];

  const generateLesson = async () => {
    setLoading(true);
    try {
      const lessonNumber = lessonHistory.length + 1;
      const previousContext = lessonHistory.length > 0
        ? `\n\nPrevious lessons covered: ${lessonHistory.map((l, i) => `Lesson ${i + 1}: ${l.title}`).join(', ')}`
        : '';

      const prompt = `You are an expert educational AI creating lesson ${lessonNumber} about "${subject}".

Student Profile:
- Skill Level: ${skillLevel}
- Learning Style: ${learningStyle}
- Progress: ${lessonHistory.length} lessons completed${previousContext}

Create an engaging, ${skillLevel}-appropriate lesson. Structure your response EXACTLY as follows:

LESSON_TITLE: [A clear, engaging title]

INTRODUCTION:
[2-3 sentences introducing the topic in an engaging way]

MAIN_CONTENT:
[The core lesson content. For ${learningStyle} learners, ${
  learningStyle === 'visual' ? 'use concrete examples and analogies' :
  learningStyle === 'practical' ? 'focus on real-world applications and how to use this knowledge' :
  learningStyle === 'theoretical' ? 'explain underlying principles and concepts deeply' :
  'balance theory with practical examples'
}. Use clear sections and formatting. Make it substantive but digestible.]

KEY_TAKEAWAYS:
[3-5 bullet points of the most important concepts]

PRACTICE_HINT:
[A brief hint about what kind of practice question will follow]

Keep the tone encouraging and enthusiastic. Adjust complexity for ${skillLevel} level.`;

      const response = await fetch("https://api.anthropic.com/v1/messages", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          model: "claude-sonnet-4-20250514",
          max_tokens: 2000,
          messages: [{ role: "user", content: prompt }]
        })
      });

      const data = await response.json();
      const lessonText = data.content[0].text;

      // Parse the lesson
      const titleMatch = lessonText.match(/LESSON_TITLE:\s*(.+)/);
      const introMatch = lessonText.match(/INTRODUCTION:\s*([\s\S]+?)(?=MAIN_CONTENT:)/);
      const contentMatch = lessonText.match(/MAIN_CONTENT:\s*([\s\S]+?)(?=KEY_TAKEAWAYS:)/);
      const takeawaysMatch = lessonText.match(/KEY_TAKEAWAYS:\s*([\s\S]+?)(?=PRACTICE_HINT:|$)/);

      const lesson = {
        title: titleMatch ? titleMatch[1].trim() : `Lesson ${lessonNumber}: ${subject}`,
        introduction: introMatch ? introMatch[1].trim() : '',
        content: contentMatch ? contentMatch[1].trim() : lessonText,
        takeaways: takeawaysMatch ? takeawaysMatch[1].trim() : '',
        timestamp: new Date().toISOString()
      };

      setCurrentLesson(lesson);
      setScreen('learning');
    } catch (error) {
      console.error('Error generating lesson:', error);
      alert('Failed to generate lesson. Please try again.');
    }
    setLoading(false);
  };

  const generateQuiz = async () => {
    setLoading(true);
    try {
      const prompt = `Based on the lesson titled "${currentLesson.title}" about ${subject}, create ONE ${skillLevel}-level quiz question.

Respond ONLY with valid JSON in this exact format (no other text, no backticks):
{
  "question": "The quiz question text",
  "type": "multiple-choice",
  "options": ["Option A", "Option B", "Option C", "Option D"],
  "correctAnswer": "The exact text of the correct option",
  "explanation": "Why this answer is correct and what it demonstrates"
}

Make the question test understanding, not just memorization. Keep it relevant to ${skillLevel} level.`;

      const response = await fetch("https://api.anthropic.com/v1/messages", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          model: "claude-sonnet-4-20250514",
          max_tokens: 800,
          messages: [{ role: "user", content: prompt }]
        })
      });

      const data = await response.json();
      let responseText = data.content[0].text;
     
      // Clean up response
      responseText = responseText.replace(/```json\n?/g, "").replace(/```\n?/g, "").trim();
     
      const quiz = JSON.parse(responseText);
      setQuizData(quiz);
      setScreen('quiz');
    } catch (error) {
      console.error('Error generating quiz:', error);
      alert('Failed to generate quiz. Please try again.');
    }
    setLoading(false);
  };

  const submitQuiz = async () => {
    if (!userAnswer) {
      alert('Please select an answer');
      return;
    }

    const isCorrect = userAnswer === quizData.correctAnswer;
   
    // Update progress
    const newProgress = Math.min(100, progress + (isCorrect ? 15 : 5));
    setProgress(newProgress);

    // Save lesson to history
    setLessonHistory([...lessonHistory, {
      ...currentLesson,
      quizResult: isCorrect ? 'correct' : 'incorrect'
    }]);

    // Show result and move to complete screen
    setScreen('complete');
  };

  const startNewLesson = () => {
    setCurrentLesson(null);
    setQuizData(null);
    setUserAnswer('');
    setScreen('learning');
    generateLesson();
  };

  const restartPlatform = () => {
    setScreen('setup');
    setSubject('');
    setCurrentLesson(null);
    setLessonHistory([]);
    setQuizData(null);
    setUserAnswer('');
    setProgress(0);
  };

  // Setup Screen
  if (screen === 'setup') {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50 p-6">
        <div className="max-w-3xl mx-auto">
          <div className="text-center mb-8 mt-8">
            <div className="flex items-center justify-center mb-4">
              <Brain className="w-16 h-16 text-purple-600" />
            </div>
            <h1 className="text-4xl font-bold text-gray-800 mb-2">Adaptive Learning AI</h1>
            <p className="text-gray-600">Personalized lessons that adapt to your style and pace</p>
          </div>

          <div className="bg-white rounded-2xl shadow-xl p-8 space-y-6">
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                What do you want to learn?
              </label>
              <input
                type="text"
                value={subject}
                onChange={(e) => setSubject(e.target.value)}
                placeholder="e.g., Quantum Physics, French Cooking, Machine Learning..."
                className="w-full px-4 py-3 border-2 border-gray-200 rounded-lg focus:border-purple-500 focus:outline-none"
              />
            </div>

            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-3">
                Your skill level
              </label>
              <div className="grid grid-cols-3 gap-3">
                {skillLevels.map((level) => (
                  <button
                    key={level.id}
                    onClick={() => setSkillLevel(level.id)}
                    className={`p-4 rounded-lg border-2 transition-all ${
                      skillLevel === level.id
                        ? 'border-purple-500 bg-purple-50'
                        : 'border-gray-200 hover:border-gray-300'
                    }`}
                  >
                    <div className="font-semibold text-gray-800">{level.name}</div>
                    <div className="text-xs text-gray-600 mt-1">{level.description}</div>
                  </button>
                ))}
              </div>
            </div>

            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-3">
                Learning style
              </label>
              <div className="grid grid-cols-2 gap-3">
                {learningStyles.map((style) => (
                  <button
                    key={style.id}
                    onClick={() => setLearningStyle(style.id)}
                    className={`p-4 rounded-lg border-2 transition-all text-left ${
                      learningStyle === style.id
                        ? 'border-purple-500 bg-purple-50'
                        : 'border-gray-200 hover:border-gray-300'
                    }`}
                  >
                    <div className="flex items-center mb-1">
                      <span className="text-2xl mr-2">{style.icon}</span>
                      <span className="font-semibold text-gray-800">{style.name}</span>
                    </div>
                    <div className="text-xs text-gray-600">{style.description}</div>
                  </button>
                ))}
              </div>
            </div>

            <button
              onClick={generateLesson}
              disabled={!subject || loading}
              className="w-full bg-gradient-to-r from-purple-600 to-pink-600 text-white py-4 rounded-lg font-semibold hover:from-purple-700 hover:to-pink-700 transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
            >
              {loading ? (
                <>
                  <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                  Crafting your first lesson...
                </>
              ) : (
                <>
                  <Sparkles className="w-5 h-5 mr-2" />
                  Start Learning
                </>
              )}
            </button>
          </div>
        </div>
      </div>
    );
  }

  // Learning Screen
  if (screen === 'learning' && currentLesson) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50 p-6">
        <div className="max-w-4xl mx-auto">
          <div className="mb-6 flex items-center justify-between">
            <div>
              <div className="text-sm text-gray-600 mb-1">Lesson {lessonHistory.length + 1}</div>
              <h2 className="text-3xl font-bold text-gray-800">{currentLesson.title}</h2>
            </div>
            <div className="text-right">
              <div className="text-sm text-gray-600 mb-1">Progress</div>
              <div className="text-2xl font-bold text-purple-600">{progress}%</div>
            </div>
          </div>

          <div className="bg-white rounded-2xl shadow-xl p-8 mb-6">
            {currentLesson.introduction && (
              <div className="mb-6 p-4 bg-purple-50 rounded-lg border-l-4 border-purple-500">
                <p className="text-gray-700 leading-relaxed">{currentLesson.introduction}</p>
              </div>
            )}

            <div className="prose max-w-none mb-6">
              {renderMarkdown(currentLesson.content)}
            </div>

            {currentLesson.takeaways && (
              <div className="mt-6 p-6 bg-gradient-to-r from-purple-50 to-pink-50 rounded-lg">
                <div className="flex items-center mb-3">
                  <Target className="w-5 h-5 text-purple-600 mr-2" />
                  <h3 className="font-semibold text-gray-800">Key Takeaways</h3>
                </div>
                {renderMarkdown(currentLesson.takeaways)}
              </div>
            )}
          </div>

          <div className="flex gap-4">
            <button
              onClick={restartPlatform}
              className="px-6 py-3 border-2 border-gray-300 text-gray-700 rounded-lg font-semibold hover:border-gray-400 transition-all"
            >
              Choose Different Topic
            </button>
            <button
              onClick={generateQuiz}
              disabled={loading}
              className="flex-1 bg-gradient-to-r from-purple-600 to-pink-600 text-white py-3 rounded-lg font-semibold hover:from-purple-700 hover:to-pink-700 transition-all disabled:opacity-50 flex items-center justify-center"
            >
              {loading ? (
                <>
                  <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                  Preparing practice...
                </>
              ) : (
                <>
                  Continue to Practice
                  <ArrowRight className="w-5 h-5 ml-2" />
                </>
              )}
            </button>
          </div>
        </div>
      </div>
    );
  }

  // Quiz Screen
  if (screen === 'quiz' && quizData) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50 p-6">
        <div className="max-w-3xl mx-auto">
          <div className="mb-6">
            <div className="text-sm text-gray-600 mb-1">Practice Question</div>
            <h2 className="text-3xl font-bold text-gray-800">Test Your Understanding</h2>
          </div>

          <div className="bg-white rounded-2xl shadow-xl p-8">
            <div className="mb-6">
              <div className="flex items-start mb-4">
                <Zap className="w-6 h-6 text-purple-600 mr-3 mt-1 flex-shrink-0" />
                <p className="text-lg text-gray-800 font-medium">{quizData.question}</p>
              </div>
            </div>

            <div className="space-y-3 mb-6">
              {quizData.options.map((option, index) => (
                <button
                  key={index}
                  onClick={() => setUserAnswer(option)}
                  className={`w-full p-4 rounded-lg border-2 text-left transition-all ${
                    userAnswer === option
                      ? 'border-purple-500 bg-purple-50'
                      : 'border-gray-200 hover:border-gray-300'
                  }`}
                >
                  <div className="flex items-center">
                    <div className={`w-6 h-6 rounded-full border-2 mr-3 flex items-center justify-center ${
                      userAnswer === option
                        ? 'border-purple-500 bg-purple-500'
                        : 'border-gray-300'
                    }`}>
                      {userAnswer === option && (
                        <CheckCircle className="w-4 h-4 text-white" />
                      )}
                    </div>
                    <span className="text-gray-800">{option}</span>
                  </div>
                </button>
              ))}
            </div>

            <button
              onClick={submitQuiz}
              disabled={!userAnswer}
              className="w-full bg-gradient-to-r from-purple-600 to-pink-600 text-white py-4 rounded-lg font-semibold hover:from-purple-700 hover:to-pink-700 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Submit Answer
            </button>
          </div>
        </div>
      </div>
    );
  }

  // Complete Screen
  if (screen === 'complete' && quizData) {
    const isCorrect = userAnswer === quizData.correctAnswer;
   
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50 p-6">
        <div className="max-w-3xl mx-auto">
          <div className={`mb-6 p-6 rounded-2xl ${
            isCorrect ? 'bg-green-100 border-2 border-green-300' : 'bg-yellow-100 border-2 border-yellow-300'
          }`}>
            <div className="text-center">
              <div className="text-4xl mb-2">{isCorrect ? '🎉' : '💡'}</div>
              <h2 className="text-2xl font-bold text-gray-800 mb-2">
                {isCorrect ? 'Excellent!' : 'Good Try!'}
              </h2>
              <p className="text-gray-700">
                {isCorrect
                  ? 'You nailed it! Your understanding is growing.'
                  : 'Learning is a journey. Let\'s review what we learned.'}
              </p>
            </div>
          </div>

          <div className="bg-white rounded-2xl shadow-xl p-8 mb-6">
            <h3 className="font-semibold text-gray-800 mb-3">The Question</h3>
            <p className="text-gray-700 mb-4">{quizData.question}</p>

            <div className="mb-4">
              <div className="text-sm font-semibold text-gray-600 mb-2">Your Answer:</div>
              <div className={`p-3 rounded-lg ${
                isCorrect ? 'bg-green-50 border border-green-200' : 'bg-red-50 border border-red-200'
              }`}>
                {userAnswer}
              </div>
            </div>

            {!isCorrect && (
              <div className="mb-4">
                <div className="text-sm font-semibold text-gray-600 mb-2">Correct Answer:</div>
                <div className="p-3 rounded-lg bg-green-50 border border-green-200">
                  {quizData.correctAnswer}
                </div>
              </div>
            )}

            <div className="mt-6 p-4 bg-blue-50 rounded-lg">
              <div className="text-sm font-semibold text-gray-800 mb-2">💡 Explanation</div>
              <p className="text-gray-700">{quizData.explanation}</p>
            </div>
          </div>

          <div className="bg-white rounded-2xl shadow-xl p-6 mb-6">
            <div className="flex items-center justify-between">
              <div>
                <div className="text-sm text-gray-600">Lessons Completed</div>
                <div className="text-2xl font-bold text-gray-800">{lessonHistory.length}</div>
              </div>
              <div>
                <div className="text-sm text-gray-600">Overall Progress</div>
                <div className="text-2xl font-bold text-purple-600">{progress}%</div>
              </div>
              <div>
                <div className="text-sm text-gray-600">Current Level</div>
                <div className="text-2xl font-bold text-gray-800 capitalize">{skillLevel}</div>
              </div>
            </div>
          </div>

          <div className="flex gap-4">
            <button
              onClick={restartPlatform}
              className="px-6 py-3 border-2 border-gray-300 text-gray-700 rounded-lg font-semibold hover:border-gray-400 transition-all"
            >
              Choose New Topic
            </button>
            <button
              onClick={startNewLesson}
              disabled={loading}
              className="flex-1 bg-gradient-to-r from-purple-600 to-pink-600 text-white py-3 rounded-lg font-semibold hover:from-purple-700 hover:to-pink-700 transition-all disabled:opacity-50 flex items-center justify-center"
            >
              {loading ? (
                <>
                  <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                  Creating next lesson...
                </>
              ) : (
                <>
                  <BookOpen className="w-5 h-5 mr-2" />
                  Continue Learning
                </>
              )}
            </button>
          </div>
        </div>
      </div>
    );
  }

  return null;
}
