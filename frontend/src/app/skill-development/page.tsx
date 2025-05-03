import React from 'react';
import TechniqueAnalysisViewer from '@/components/skill-development/TechniqueAnalysisViewer';
import TrainingRecommendations from '@/components/skill-development/TrainingRecommendations';
import ProgressTracking from '@/components/skill-development/ProgressTracking';

export default function SkillDevelopmentPage() {
  // Mock user ID for demonstration
  const userId = 1;
  
  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 mb-8">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">
          Skill Development
        </h1>
        <p className="text-lg text-gray-600 dark:text-gray-300 mb-6">
          Personalized tennis skill development recommendations based on professional match analysis.
        </p>
      </div>

      {/* Skill Areas Section */}
      <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">Skill Areas</h2>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        {[
          { title: "Technical Skills", icon: "🎯", description: "Stroke techniques, footwork, and movement patterns" },
          { title: "Tactical Skills", icon: "🧠", description: "Game strategy, shot selection, and court positioning" },
          { title: "Mental Skills", icon: "🧘", description: "Focus, resilience, and pressure management" }
        ].map((skill, index) => (
          <div key={index} className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
            <div className="flex items-center mb-4">
              <span className="text-3xl mr-3">{skill.icon}</span>
              <h3 className="text-xl font-semibold text-gray-900 dark:text-white">{skill.title}</h3>
            </div>
            <p className="text-gray-600 dark:text-gray-300 mb-4">{skill.description}</p>
            <a 
              href={`/skill-development/${skill.title.toLowerCase().replace(' ', '-')}`}
              className="text-indigo-600 dark:text-indigo-400 hover:text-indigo-800 dark:hover:text-indigo-300 font-medium"
            >
              View recommendations →
            </a>
          </div>
        ))}
      </div>

      {/* Technique Analysis Viewer Component */}
      <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">Technique Analysis</h2>
      <TechniqueAnalysisViewer userId={userId} />

      {/* Training Recommendations Component */}
      <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">Training Recommendations</h2>
      <TrainingRecommendations userId={userId} />

      {/* Progress Tracking Component */}
      <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">Skill Progress</h2>
      <ProgressTracking userId={userId} />
    </div>
  );
}
