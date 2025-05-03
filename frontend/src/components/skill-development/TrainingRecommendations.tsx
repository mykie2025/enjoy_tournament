"use client";

import React, { useState } from 'react';

interface Recommendation {
  id: number;
  title: string;
  description: string;
  category: string;
  priority: 'High' | 'Medium' | 'Low';
  status: 'Not Started' | 'In Progress' | 'Completed';
  dateCreated: string;
  source: string;
}

interface TrainingRecommendationsProps {
  userId: number;
}

const TrainingRecommendations: React.FC<TrainingRecommendationsProps> = ({ userId }) => {
  const [filter, setFilter] = useState('all');
  const [sortBy, setSortBy] = useState('priority');
  
  // Mock data for demonstration
  const recommendations: Recommendation[] = [
    {
      id: 1,
      title: 'Improve second serve consistency',
      description: 'Focus on increasing second serve percentage and pace, particularly under pressure. Practice kick serves with controlled power.',
      category: 'Technical',
      priority: 'High',
      status: 'In Progress',
      dateCreated: '2025-05-01',
      source: 'Federer vs Djokovic Analysis'
    },
    {
      id: 2,
      title: 'Increase net approach frequency',
      description: 'Approach the net more frequently, especially after wide serves. Practice transition game and volley positioning.',
      category: 'Tactical',
      priority: 'Medium',
      status: 'Not Started',
      dateCreated: '2025-05-01',
      source: 'Federer vs Djokovic Analysis'
    },
    {
      id: 3,
      title: 'Improve backhand return positioning',
      description: 'Stand closer to the baseline when returning second serves to take time away from opponent. Focus on aggressive positioning and early preparation.',
      category: 'Tactical',
      priority: 'Medium',
      status: 'Completed',
      dateCreated: '2025-04-28',
      source: 'Federer vs Nadal Analysis'
    },
    {
      id: 4,
      title: 'Develop forehand down-the-line',
      description: 'Practice hitting forehand down-the-line from defensive positions. Focus on hip rotation and follow-through direction.',
      category: 'Technical',
      priority: 'High',
      status: 'In Progress',
      dateCreated: '2025-04-25',
      source: 'Alcaraz vs Sinner Analysis'
    },
    {
      id: 5,
      title: 'Improve focus during break points',
      description: 'Develop a consistent routine for high-pressure points. Practice visualization and breathing techniques.',
      category: 'Mental',
      priority: 'High',
      status: 'Not Started',
      dateCreated: '2025-04-22',
      source: 'Djokovic vs Medvedev Analysis'
    },
    {
      id: 6,
      title: 'Enhance slice backhand variety',
      description: 'Practice different depths and spins with slice backhand. Focus on changing pace to disrupt opponent rhythm.',
      category: 'Technical',
      priority: 'Low',
      status: 'Not Started',
      dateCreated: '2025-04-20',
      source: 'Federer vs Zverev Analysis'
    }
  ];
  
  // Filter recommendations
  const filteredRecommendations = recommendations.filter(rec => {
    if (filter === 'all') return true;
    if (filter === 'technical') return rec.category === 'Technical';
    if (filter === 'tactical') return rec.category === 'Tactical';
    if (filter === 'mental') return rec.category === 'Mental';
    if (filter === 'completed') return rec.status === 'Completed';
    if (filter === 'in-progress') return rec.status === 'In Progress';
    if (filter === 'not-started') return rec.status === 'Not Started';
    if (filter === 'high-priority') return rec.priority === 'High';
    return true;
  });
  
  // Sort recommendations
  const sortedRecommendations = [...filteredRecommendations].sort((a, b) => {
    if (sortBy === 'priority') {
      const priorityOrder = { 'High': 0, 'Medium': 1, 'Low': 2 };
      return priorityOrder[a.priority] - priorityOrder[b.priority];
    }
    if (sortBy === 'date') {
      return new Date(b.dateCreated).getTime() - new Date(a.dateCreated).getTime();
    }
    if (sortBy === 'status') {
      const statusOrder = { 'Not Started': 0, 'In Progress': 1, 'Completed': 2 };
      return statusOrder[a.status] - statusOrder[b.status];
    }
    return 0;
  });
  
  // Toggle recommendation status
  const toggleStatus = (id: number) => {
    // In a real app, this would update the status in the database
    console.log(`Toggling status for recommendation ${id}`);
  };
  
  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 mb-8">
      <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">Training Recommendations</h2>
      
      {/* Filters and Sorting */}
      <div className="flex flex-wrap gap-4 mb-6">
        <div>
          <label htmlFor="filter-selector" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
            Filter By
          </label>
          <select
            id="filter-selector"
            value={filter}
            onChange={(e) => setFilter(e.target.value)}
            className="rounded-md border-gray-300 dark:border-gray-600 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 dark:bg-gray-700 dark:text-white"
          >
            <option value="all">All Recommendations</option>
            <option value="technical">Technical Skills</option>
            <option value="tactical">Tactical Skills</option>
            <option value="mental">Mental Skills</option>
            <option value="high-priority">High Priority</option>
            <option value="completed">Completed</option>
            <option value="in-progress">In Progress</option>
            <option value="not-started">Not Started</option>
          </select>
        </div>
        
        <div>
          <label htmlFor="sort-selector" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
            Sort By
          </label>
          <select
            id="sort-selector"
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value)}
            className="rounded-md border-gray-300 dark:border-gray-600 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 dark:bg-gray-700 dark:text-white"
          >
            <option value="priority">Priority</option>
            <option value="date">Date (Newest First)</option>
            <option value="status">Status</option>
          </select>
        </div>
      </div>
      
      {/* Recommendations List */}
      <div className="space-y-4">
        {sortedRecommendations.length > 0 ? (
          sortedRecommendations.map((rec) => (
            <div 
              key={rec.id}
              className="border border-gray-200 dark:border-gray-700 rounded-lg overflow-hidden"
            >
              <div className="flex items-center justify-between px-4 py-3 bg-gray-50 dark:bg-gray-700">
                <div className="flex items-center">
                  <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                    rec.category === 'Technical' 
                      ? 'bg-blue-100 text-blue-800 dark:bg-blue-800 dark:text-blue-100'
                      : rec.category === 'Tactical'
                      ? 'bg-purple-100 text-purple-800 dark:bg-purple-800 dark:text-purple-100'
                      : 'bg-green-100 text-green-800 dark:bg-green-800 dark:text-green-100'
                  }`}>
                    {rec.category}
                  </span>
                  <span className={`ml-2 inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                    rec.priority === 'High' 
                      ? 'bg-red-100 text-red-800 dark:bg-red-800 dark:text-red-100'
                      : rec.priority === 'Medium'
                      ? 'bg-yellow-100 text-yellow-800 dark:bg-yellow-800 dark:text-yellow-100'
                      : 'bg-green-100 text-green-800 dark:bg-green-800 dark:text-green-100'
                  }`}>
                    {rec.priority} Priority
                  </span>
                </div>
                <div className="flex items-center">
                  <span className="text-xs text-gray-500 dark:text-gray-400 mr-2">
                    {rec.dateCreated}
                  </span>
                  <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                    rec.status === 'Completed' 
                      ? 'bg-green-100 text-green-800 dark:bg-green-800 dark:text-green-100'
                      : rec.status === 'In Progress'
                      ? 'bg-blue-100 text-blue-800 dark:bg-blue-800 dark:text-blue-100'
                      : 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300'
                  }`}>
                    {rec.status}
                  </span>
                </div>
              </div>
              <div className="px-4 py-3">
                <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-1">
                  {rec.title}
                </h3>
                <p className="text-sm text-gray-600 dark:text-gray-300 mb-2">
                  {rec.description}
                </p>
                <div className="flex items-center text-xs text-gray-500 dark:text-gray-400">
                  <span>Source: {rec.source}</span>
                </div>
              </div>
              <div className="px-4 py-3 bg-gray-50 dark:bg-gray-700 flex justify-between">
                <button
                  type="button"
                  className="text-indigo-600 dark:text-indigo-400 hover:text-indigo-800 dark:hover:text-indigo-300 text-sm font-medium"
                  onClick={() => console.log(`View details for recommendation ${rec.id}`)}
                >
                  View Details
                </button>
                <button
                  type="button"
                  className={`text-sm font-medium ${
                    rec.status === 'Completed'
                      ? 'text-gray-600 dark:text-gray-400'
                      : 'text-green-600 dark:text-green-400 hover:text-green-800 dark:hover:text-green-300'
                  }`}
                  onClick={() => toggleStatus(rec.id)}
                  disabled={rec.status === 'Completed'}
                >
                  {rec.status === 'Completed' ? 'Completed' : 'Mark as Complete'}
                </button>
              </div>
            </div>
          ))
        ) : (
          <div className="text-center py-8 text-gray-500 dark:text-gray-400">
            No recommendations match the selected filter.
          </div>
        )}
      </div>
      
      {/* Add Custom Recommendation Button */}
      <div className="mt-6">
        <button
          type="button"
          className="flex items-center justify-center w-full bg-indigo-600 hover:bg-indigo-700 text-white font-medium py-2 px-4 rounded-md transition-colors"
        >
          <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
            <path fillRule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clipRule="evenodd" />
          </svg>
          Add Custom Recommendation
        </button>
      </div>
    </div>
  );
};

export default TrainingRecommendations;
