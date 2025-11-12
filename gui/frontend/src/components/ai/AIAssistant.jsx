import React, { useState, useRef, useEffect } from 'react';
import Card from '../common/Card';
import Button from '../common/Button';
import LoadingSpinner from '../common/LoadingSpinner';

const AIAssistant = ({ customerId = null }) => {
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content: 'Hej! Jag är din AI SEO-assistent. Fråga mig om din länkprofil, SEO-strategi eller få smarta rekommendationer!',
    },
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(scrollToBottom, [messages]);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = { role: 'user', content: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const response = await fetch('http://localhost:8000/api/ai/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          messages: [...messages, userMessage].map(m => ({
            role: m.role,
            content: m.content
          })),
          customer_id: customerId,
        }),
      });

      const data = await response.json();
      const aiMessage = { role: 'assistant', content: data.data.response };
      setMessages(prev => [...prev, aiMessage]);
    } catch (error) {
      console.error('AI chat error:', error);
      setMessages(prev => [
        ...prev,
        { role: 'assistant', content: 'Ursäkta, något gick fel. Försök igen!' },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const quickQuestions = [
    'Hur ser min länkprofil ut?',
    'Vilka risker har jag?',
    'Vad ska jag göra härnäst?',
    'Analysera min ankartextstrategi'
  ];

  return (
    <Card className="flex flex-col h-[500px]">
      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto mb-4 space-y-4 pr-2">
        {messages.map((message, index) => (
          <div
            key={index}
            className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-[85%] rounded-lg px-4 py-3 ${
                message.role === 'user'
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-100 text-gray-900 border border-gray-200'
              }`}
            >
              <p className="text-sm whitespace-pre-wrap">{message.content}</p>
            </div>
          </div>
        ))}
        {loading && (
          <div className="flex justify-start">
            <div className="bg-gray-100 rounded-lg px-4 py-3 border border-gray-200">
              <LoadingSpinner size="sm" />
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="flex space-x-2 mb-3">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Fråga mig vad som helst om SEO..."
          className="flex-1 px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          disabled={loading}
        />
        <Button onClick={sendMessage} disabled={loading || !input.trim()}>
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
          </svg>
        </Button>
      </div>

      {/* Quick Questions */}
      <div className="flex flex-wrap gap-2">
        {quickQuestions.map((question, index) => (
          <button
            key={index}
            onClick={() => setInput(question)}
            className="text-xs px-3 py-1.5 bg-gray-100 rounded-full hover:bg-gray-200 transition-colors"
            disabled={loading}
          >
            {question}
          </button>
        ))}
      </div>
    </Card>
  );
};

export default AIAssistant;
