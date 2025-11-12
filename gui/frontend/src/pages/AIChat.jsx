import React from 'react';
import AIAssistant from '../components/ai/AIAssistant';

const AIChat = () => {
  return (
    <div className="max-w-4xl mx-auto">
      <div className="mb-6">
        <h1 className="text-4xl font-bold mb-2">
          <span className="bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
            🤖 AI SEO Assistant
          </span>
        </h1>
        <p className="text-gray-600 text-lg">
          Fråga mig vad som helst om din länkprofil, SEO-strategi eller få AI-drivna rekommendationer.
        </p>
      </div>

      <AIAssistant />

      <div className="mt-8 grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-gradient-to-br from-blue-50 to-blue-100 p-5 rounded-lg border border-blue-200">
          <div className="text-3xl mb-2">📊</div>
          <h3 className="font-semibold text-blue-900 mb-2">Dataanalys</h3>
          <p className="text-sm text-blue-800">
            Jag kan analysera din kompletta länkprofil och identifiera mönster och trender.
          </p>
        </div>

        <div className="bg-gradient-to-br from-purple-50 to-purple-100 p-5 rounded-lg border border-purple-200">
          <div className="text-3xl mb-2">🎯</div>
          <h3 className="font-semibold text-purple-900 mb-2">Strategiråd</h3>
          <p className="text-sm text-purple-800">
            Få personliga rekommendationer för din nästa länkbyggnadskampanj.
          </p>
        </div>

        <div className="bg-gradient-to-br from-green-50 to-green-100 p-5 rounded-lg border border-green-200">
          <div className="text-3xl mb-2">⚠️</div>
          <h3 className="font-semibold text-green-900 mb-2">Riskdetektering</h3>
          <p className="text-sm text-green-800">
            Jag varnar dig för potentiella påföljder och över-optimering.
          </p>
        </div>
      </div>

      <div className="mt-6 p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
        <p className="text-sm text-yellow-800">
          <strong>💡 Tips:</strong> Ju mer specifik du är i dina frågor, desto bättre svar får du!
          Prova att fråga om specifika områden som "ankartextfördelning" eller "temporal strategi".
        </p>
      </div>
    </div>
  );
};

export default AIChat;
