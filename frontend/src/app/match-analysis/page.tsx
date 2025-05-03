import React from 'react';

export default function MatchAnalysisPage() {
  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 mb-8">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">
          Match Analysis
        </h1>
        <p className="text-lg text-gray-600 dark:text-gray-300 mb-6">
          Analyze professional tennis matches to extract key patterns, techniques, and strategies.
        </p>
      </div>

      {/* Search and Filter Section */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 mb-8">
        <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">
          Find Matches
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label htmlFor="tournament" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              Tournament
            </label>
            <select
              id="tournament"
              className="w-full rounded-md border-gray-300 dark:border-gray-600 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 dark:bg-gray-700 dark:text-white"
            >
              <option value="">All Tournaments</option>
              <option value="french-open-2024">French Open 2024</option>
              <option value="wimbledon-2024">Wimbledon 2024</option>
              <option value="us-open-2024">US Open 2024</option>
            </select>
          </div>
          <div>
            <label htmlFor="player" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              Player
            </label>
            <select
              id="player"
              className="w-full rounded-md border-gray-300 dark:border-gray-600 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 dark:bg-gray-700 dark:text-white"
            >
              <option value="">All Players</option>
              <option value="djokovic">Novak Djokovic</option>
              <option value="nadal">Rafael Nadal</option>
              <option value="alcaraz">Carlos Alcaraz</option>
            </select>
          </div>
          <div>
            <label htmlFor="round" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              Round
            </label>
            <select
              id="round"
              className="w-full rounded-md border-gray-300 dark:border-gray-600 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 dark:bg-gray-700 dark:text-white"
            >
              <option value="">All Rounds</option>
              <option value="final">Final</option>
              <option value="semi">Semi-Final</option>
              <option value="quarter">Quarter-Final</option>
            </select>
          </div>
        </div>
        <div className="mt-4">
          <button
            type="button"
            className="bg-indigo-600 hover:bg-indigo-700 text-white font-medium py-2 px-4 rounded-md transition-colors"
          >
            Search Matches
          </button>
        </div>
      </div>

      {/* Recent Matches Section */}
      <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">Recent Matches</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
        {[1, 2, 3, 4, 5, 6].map((item) => (
          <div key={item} className="bg-white dark:bg-gray-800 rounded-lg shadow-md overflow-hidden">
            <div className="p-4">
              <div className="flex justify-between items-center mb-3">
                <span className="text-xs text-indigo-600 dark:text-indigo-400 font-semibold">
                  {['French Open', 'Wimbledon', 'US Open'][item % 3]} • {['Final', 'Semi-Final', 'Quarter-Final'][item % 3]}
                </span>
                <span className="text-xs text-gray-500 dark:text-gray-400">May {item + 1}, 2025</span>
              </div>
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                {['Djokovic', 'Nadal', 'Alcaraz', 'Medvedev', 'Zverev', 'Sinner'][item % 6]} vs. {['Nadal', 'Alcaraz', 'Medvedev', 'Zverev', 'Sinner', 'Djokovic'][item % 6]}
              </h3>
              <div className="flex justify-between items-center text-sm mb-4">
                <div className="flex items-center">
                  <span className="font-semibold mr-1">Score:</span>
                  <span className="text-gray-600 dark:text-gray-300">
                    {['6-4, 6-3, 7-6', '3-6, 6-4, 6-2, 6-4', '6-7, 7-5, 6-2, 6-3'][item % 3]}
                  </span>
                </div>
                <div className="flex items-center">
                  <span className="font-semibold mr-1">Duration:</span>
                  <span className="text-gray-600 dark:text-gray-300">{['2h 45m', '3h 12m', '3h 30m'][item % 3]}</span>
                </div>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-xs text-gray-500 dark:text-gray-400">
                  {['Clay', 'Grass', 'Hard'][item % 3]} Court
                </span>
                <a 
                  href={`/match-analysis/${item}`}
                  className="text-sm text-indigo-600 dark:text-indigo-400 hover:text-indigo-800 dark:hover:text-indigo-300"
                >
                  View Match →
                </a>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* New Analysis Button */}
      <div className="flex justify-center mt-6">
        <a 
          href="/match-analysis/new"
          className="bg-indigo-600 hover:bg-indigo-700 text-white font-medium py-3 px-6 rounded-md transition-colors flex items-center"
        >
          <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
            <path fillRule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clipRule="evenodd" />
          </svg>
          Analyze New Match
        </a>
      </div>
    </div>
  );
}
