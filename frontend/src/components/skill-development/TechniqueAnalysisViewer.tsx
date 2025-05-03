"use client";

import React, { useState } from 'react';

interface TechniqueAnalysisViewerProps {
  userId: number;
}

interface TechniqueData {
  title: string;
  description: string;
  keyPoints: string[];
  strengths: string[];
  imageUrl: string;
}

interface PlayerTechniqueData {
  [key: string]: TechniqueData;
}

interface TechniqueDataMap {
  [key: string]: PlayerTechniqueData;
}

const TechniqueAnalysisViewer: React.FC<TechniqueAnalysisViewerProps> = ({ userId }) => {
  const [selectedTechnique, setSelectedTechnique] = useState('forehand');
  const [selectedPlayer, setSelectedPlayer] = useState('federer');
  
  // Mock data for demonstration
  const techniques = [
    { id: 'forehand', name: 'Forehand' },
    { id: 'backhand', name: 'Backhand' },
    { id: 'serve', name: 'Serve' },
    { id: 'volley', name: 'Volley' },
    { id: 'footwork', name: 'Footwork' }
  ];
  
  const players = [
    { id: 'federer', name: 'Roger Federer' },
    { id: 'nadal', name: 'Rafael Nadal' },
    { id: 'djokovic', name: 'Novak Djokovic' },
    { id: 'alcaraz', name: 'Carlos Alcaraz' }
  ];
  
  const techniqueData: TechniqueDataMap = {
    forehand: {
      federer: {
        title: 'Roger Federer\'s Forehand',
        description: 'Federer\'s forehand is known for its fluidity and versatility. He uses an Eastern grip which allows for both topspin and flat shots.',
        keyPoints: [
          'Eastern grip for versatility',
          'Full shoulder turn for power generation',
          'Relaxed wrist for control and feel',
          'Complete follow-through across the body',
          'Early preparation and racket take-back'
        ],
        strengths: [
          'Exceptional disguise and deception',
          'Ability to hit winners from any position',
          'Versatility in spin and pace',
          'Efficient energy transfer'
        ],
        imageUrl: 'https://example.com/federer-forehand.jpg'
      },
      nadal: {
        title: 'Rafael Nadal\'s Forehand',
        description: 'Nadal\'s forehand is characterized by extreme topspin and a unique "lasso" technique. He uses a semi-Western grip for maximum rotation.',
        keyPoints: [
          'Semi-Western to Western grip',
          'Extreme wrist rotation for topspin',
          'High-to-low swing path',
          'Lasso finish above the shoulder',
          'Open stance for stability'
        ],
        strengths: [
          'Incredible topspin generation',
          'Exceptional consistency',
          'Great defensive capabilities',
          'Effective on all surfaces, especially clay'
        ],
        imageUrl: 'https://example.com/nadal-forehand.jpg'
      },
      // Other players' data would be here
    },
    backhand: {
      // Backhand data for different players
    },
    serve: {
      // Serve data for different players
    },
    // Other techniques
  };
  
  const selectedTechniqueData = techniqueData[selectedTechnique]?.[selectedPlayer];
  
  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 mb-8">
      <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">Technique Analysis</h2>
      
      {/* Selection Controls */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
        <div>
          <label htmlFor="technique-selector" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
            Technique
          </label>
          <select
            id="technique-selector"
            value={selectedTechnique}
            onChange={(e) => setSelectedTechnique(e.target.value)}
            className="w-full rounded-md border-gray-300 dark:border-gray-600 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 dark:bg-gray-700 dark:text-white"
          >
            {techniques.map((technique) => (
              <option key={technique.id} value={technique.id}>{technique.name}</option>
            ))}
          </select>
        </div>
        
        <div>
          <label htmlFor="player-selector" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
            Reference Player
          </label>
          <select
            id="player-selector"
            value={selectedPlayer}
            onChange={(e) => setSelectedPlayer(e.target.value)}
            className="w-full rounded-md border-gray-300 dark:border-gray-600 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 dark:bg-gray-700 dark:text-white"
          >
            {players.map((player) => (
              <option key={player.id} value={player.id}>{player.name}</option>
            ))}
          </select>
        </div>
      </div>
      
      {selectedTechniqueData && (
        <div>
          {/* Technique Visualization */}
          <div className="bg-gray-100 dark:bg-gray-700 rounded-lg p-4 mb-6">
            <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">
              {selectedTechniqueData.title}
            </h3>
            
            {/* This would be an actual video or animation in a real implementation */}
            <div className="relative w-full h-64 bg-gray-200 dark:bg-gray-600 rounded-lg mb-4 flex items-center justify-center">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-16 w-16 text-gray-400 dark:text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" />
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <div className="absolute inset-0 flex items-center justify-center">
                <span className="text-sm text-gray-500 dark:text-gray-400">
                  Technique visualization would appear here
                </span>
              </div>
            </div>
            
            <p className="text-gray-600 dark:text-gray-300 mb-4">
              {selectedTechniqueData.description}
            </p>
          </div>
          
          {/* Key Technical Points */}
          <div className="mb-6">
            <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-3">
              Key Technical Points
            </h3>
            <ul className="space-y-2">
              {selectedTechniqueData.keyPoints.map((point: string, index: number) => (
                <li key={index} className="flex items-start">
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-green-500 dark:text-green-400 mr-2 mt-0.5" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                  </svg>
                  <span className="text-gray-700 dark:text-gray-300">{point}</span>
                </li>
              ))}
            </ul>
          </div>
          
          {/* Strengths */}
          <div>
            <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-3">
              Strengths
            </h3>
            <ul className="space-y-2">
              {selectedTechniqueData.strengths.map((strength: string, index: number) => (
                <li key={index} className="flex items-start">
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-indigo-500 dark:text-indigo-400 mr-2 mt-0.5" viewBox="0 0 20 20" fill="currentColor">
                    <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                  </svg>
                  <span className="text-gray-700 dark:text-gray-300">{strength}</span>
                </li>
              ))}
            </ul>
          </div>
          
          {/* Compare with Your Technique Button */}
          <div className="mt-6">
            <button
              type="button"
              className="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-medium py-2 px-4 rounded-md transition-colors"
            >
              Compare with Your Technique
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default TechniqueAnalysisViewer;
