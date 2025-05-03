"use client";

import React, { useState } from 'react';

interface SkillProgress {
  id: string;
  name: string;
  category: string;
  currentLevel: number;
  targetLevel: number;
  progress: number[];
  lastUpdated: string;
}

interface ProgressTrackingProps {
  userId: number;
}

const ProgressTracking: React.FC<ProgressTrackingProps> = ({ userId }) => {
  const [timeframe, setTimeframe] = useState('3m');
  const [selectedCategory, setSelectedCategory] = useState('all');
  
  // Mock data for demonstration
  const skillCategories = [
    { id: 'all', name: 'All Skills' },
    { id: 'technical', name: 'Technical' },
    { id: 'tactical', name: 'Tactical' },
    { id: 'physical', name: 'Physical' },
    { id: 'mental', name: 'Mental' }
  ];
  
  const skillProgressData: SkillProgress[] = [
    {
      id: 'forehand',
      name: 'Forehand',
      category: 'technical',
      currentLevel: 7,
      targetLevel: 9,
      progress: [5, 5, 6, 6, 6, 7, 7],
      lastUpdated: '2025-05-01'
    },
    {
      id: 'backhand',
      name: 'Backhand',
      category: 'technical',
      currentLevel: 6,
      targetLevel: 8,
      progress: [4, 4, 5, 5, 6, 6, 6],
      lastUpdated: '2025-05-01'
    },
    {
      id: 'serve',
      name: 'Serve',
      category: 'technical',
      currentLevel: 8,
      targetLevel: 9,
      progress: [6, 7, 7, 7, 8, 8, 8],
      lastUpdated: '2025-04-28'
    },
    {
      id: 'volley',
      name: 'Volley',
      category: 'technical',
      currentLevel: 5,
      targetLevel: 7,
      progress: [3, 3, 4, 4, 5, 5, 5],
      lastUpdated: '2025-04-25'
    },
    {
      id: 'court-positioning',
      name: 'Court Positioning',
      category: 'tactical',
      currentLevel: 6,
      targetLevel: 8,
      progress: [4, 5, 5, 5, 6, 6, 6],
      lastUpdated: '2025-04-22'
    },
    {
      id: 'shot-selection',
      name: 'Shot Selection',
      category: 'tactical',
      currentLevel: 7,
      targetLevel: 9,
      progress: [5, 5, 6, 6, 7, 7, 7],
      lastUpdated: '2025-04-20'
    },
    {
      id: 'endurance',
      name: 'Endurance',
      category: 'physical',
      currentLevel: 8,
      targetLevel: 9,
      progress: [6, 7, 7, 8, 8, 8, 8],
      lastUpdated: '2025-04-18'
    },
    {
      id: 'mental-toughness',
      name: 'Mental Toughness',
      category: 'mental',
      currentLevel: 6,
      targetLevel: 8,
      progress: [4, 4, 5, 5, 5, 6, 6],
      lastUpdated: '2025-04-15'
    }
  ];
  
  // Filter skills based on selected category
  const filteredSkills = skillProgressData.filter(skill => {
    if (selectedCategory === 'all') return true;
    return skill.category === selectedCategory;
  });
  
  // Function to get the appropriate number of data points based on timeframe
  const getTimeframeData = (progress: number[]) => {
    switch (timeframe) {
      case '1m':
        return progress.slice(-4); // Last 4 weeks (1 month)
      case '3m':
        return progress; // All data (assuming 3 months)
      case '6m':
        return progress; // In a real app, this would have more data points
      default:
        return progress;
    }
  };
  
  // Calculate overall progress percentage
  const calculateOverallProgress = () => {
    if (filteredSkills.length === 0) return 0;
    
    const totalCurrentLevels = filteredSkills.reduce((sum, skill) => sum + skill.currentLevel, 0);
    const totalTargetLevels = filteredSkills.reduce((sum, skill) => sum + skill.targetLevel, 0);
    
    return Math.round((totalCurrentLevels / totalTargetLevels) * 100);
  };
  
  const overallProgress = calculateOverallProgress();
  
  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
      <div className="flex flex-wrap items-center justify-between mb-6">
        <h2 className="text-xl font-semibold text-gray-900 dark:text-white">Progress Tracking</h2>
        
        <div className="flex space-x-4 mt-2 sm:mt-0">
          <div>
            <select
              value={selectedCategory}
              onChange={(e) => setSelectedCategory(e.target.value)}
              className="rounded-md border-gray-300 dark:border-gray-600 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 dark:bg-gray-700 dark:text-white text-sm"
            >
              {skillCategories.map((category) => (
                <option key={category.id} value={category.id}>{category.name}</option>
              ))}
            </select>
          </div>
          
          <div>
            <select
              value={timeframe}
              onChange={(e) => setTimeframe(e.target.value)}
              className="rounded-md border-gray-300 dark:border-gray-600 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 dark:bg-gray-700 dark:text-white text-sm"
            >
              <option value="1m">Last Month</option>
              <option value="3m">Last 3 Months</option>
              <option value="6m">Last 6 Months</option>
            </select>
          </div>
        </div>
      </div>
      
      {/* Overall Progress */}
      <div className="mb-8">
        <div className="flex items-center justify-between mb-2">
          <h3 className="text-lg font-medium text-gray-900 dark:text-white">Overall Progress</h3>
          <span className="text-lg font-semibold text-indigo-600 dark:text-indigo-400">{overallProgress}%</span>
        </div>
        <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-4">
          <div 
            className="bg-indigo-600 h-4 rounded-full" 
            style={{ width: `${overallProgress}%` }}
          ></div>
        </div>
      </div>
      
      {/* Individual Skills Progress */}
      <div className="space-y-6">
        {filteredSkills.map((skill) => {
          const progressPercentage = Math.round((skill.currentLevel / skill.targetLevel) * 100);
          const timeframeData = getTimeframeData(skill.progress);
          
          return (
            <div key={skill.id} className="border-b border-gray-200 dark:border-gray-700 pb-6 last:border-b-0 last:pb-0">
              <div className="flex items-center justify-between mb-2">
                <div>
                  <h4 className="text-base font-medium text-gray-900 dark:text-white">{skill.name}</h4>
                  <p className="text-sm text-gray-500 dark:text-gray-400 capitalize">{skill.category}</p>
                </div>
                <div className="text-right">
                  <div className="text-sm font-medium text-gray-900 dark:text-white">
                    Level {skill.currentLevel}/{skill.targetLevel}
                  </div>
                  <p className="text-xs text-gray-500 dark:text-gray-400">
                    Last updated: {skill.lastUpdated}
                  </p>
                </div>
              </div>
              
              {/* Progress Bar */}
              <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2.5 mb-4">
                <div 
                  className="bg-indigo-600 h-2.5 rounded-full" 
                  style={{ width: `${progressPercentage}%` }}
                ></div>
              </div>
              
              {/* Progress Chart (simplified representation) */}
              <div className="h-16 flex items-end space-x-1">
                {timeframeData.map((value, index) => {
                  const height = (value / 10) * 100; // Scale to percentage (assuming max level is 10)
                  return (
                    <div key={index} className="flex-1 flex flex-col items-center">
                      <div 
                        className="w-full bg-indigo-200 dark:bg-indigo-900 rounded-t"
                        style={{ height: `${height}%` }}
                      ></div>
                      <span className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                        {index + 1}
                      </span>
                    </div>
                  );
                })}
              </div>
              
              {/* Update Button */}
              <div className="mt-4 flex justify-end">
                <button
                  type="button"
                  className="text-indigo-600 dark:text-indigo-400 hover:text-indigo-800 dark:hover:text-indigo-300 text-sm font-medium"
                  onClick={() => console.log(`Update progress for ${skill.name}`)}
                >
                  Update Progress
                </button>
              </div>
            </div>
          );
        })}
        
        {filteredSkills.length === 0 && (
          <div className="text-center py-8 text-gray-500 dark:text-gray-400">
            No skills found in this category.
          </div>
        )}
      </div>
      
      {/* Add New Skill Button */}
      <div className="mt-8">
        <button
          type="button"
          className="flex items-center justify-center w-full bg-indigo-600 hover:bg-indigo-700 text-white font-medium py-2 px-4 rounded-md transition-colors"
        >
          <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
            <path fillRule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clipRule="evenodd" />
          </svg>
          Add New Skill
        </button>
      </div>
    </div>
  );
};

export default ProgressTracking;
