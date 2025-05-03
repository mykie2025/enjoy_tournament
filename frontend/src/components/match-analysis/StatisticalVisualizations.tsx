"use client";

import React, { useState } from 'react';

interface StatisticalVisualizationsProps {
  matchId: number;
  player1: string;
  player2: string;
}

interface RallyLengthValues {
  [key: string]: number;
}

interface RallyLengthData {
  [key: string]: { [player: string]: number };
}

interface PlayerRallyStats {
  forehandWinners: number;
  backhandWinners: number;
  forehandErrors: number;
  backhandErrors: number;
  netPoints: number;
  netPointsWon: number;
}

interface PlayerServeStats {
  aces: number;
  doubleFaults: number;
  firstServePercentage: number;
  secondServePercentage: number;
  firstServePointsWon: number;
  secondServePointsWon: number;
  wideServes: number;
  bodyServes: number;
  tServes: number;
}

interface PlayerOverviewStats {
  aces: number;
  doubleFaults: number;
  firstServePercentage: number;
  firstServePointsWon: number;
  secondServePointsWon: number;
  breakPointsConverted: number;
  breakPointOpportunities: number;
  totalPoints: number;
}

const StatisticalVisualizations: React.FC<StatisticalVisualizationsProps> = ({ 
  matchId, 
  player1, 
  player2 
}) => {
  const [activeTab, setActiveTab] = useState('overview');
  
  // Mock data for demonstration
  const stats = {
    overview: {
      [player1]: { 
        aces: 12, 
        doubleFaults: 2, 
        firstServePercentage: 68, 
        firstServePointsWon: 78, 
        secondServePointsWon: 52,
        breakPointsConverted: 3,
        breakPointOpportunities: 5,
        totalPoints: 98
      } as PlayerOverviewStats,
      [player2]: { 
        aces: 8, 
        doubleFaults: 1, 
        firstServePercentage: 72, 
        firstServePointsWon: 75, 
        secondServePointsWon: 48,
        breakPointsConverted: 0,
        breakPointOpportunities: 3,
        totalPoints: 87
      } as PlayerOverviewStats
    },
    serve: {
      [player1]: {
        aces: 12,
        doubleFaults: 2,
        firstServePercentage: 68,
        secondServePercentage: 92,
        firstServePointsWon: 78,
        secondServePointsWon: 52,
        wideServes: 35,
        bodyServes: 25,
        tServes: 40
      } as PlayerServeStats,
      [player2]: {
        aces: 8,
        doubleFaults: 1,
        firstServePercentage: 72,
        secondServePercentage: 94,
        firstServePointsWon: 75,
        secondServePointsWon: 48,
        wideServes: 30,
        bodyServes: 30,
        tServes: 40
      } as PlayerServeStats
    },
    rally: {
      [player1]: {
        forehandWinners: 18,
        backhandWinners: 12,
        forehandErrors: 15,
        backhandErrors: 10,
        netPoints: 12,
        netPointsWon: 9
      } as PlayerRallyStats,
      [player2]: {
        forehandWinners: 14,
        backhandWinners: 15,
        forehandErrors: 18,
        backhandErrors: 12,
        netPoints: 8,
        netPointsWon: 5
      } as PlayerRallyStats,
      rallyLengths: {
        '1-3': { [player1]: 25, [player2]: 20 },
        '4-6': { [player1]: 18, [player2]: 15 },
        '7-9': { [player1]: 12, [player2]: 14 },
        '10+': { [player1]: 5, [player2]: 8 }
      } as RallyLengthData
    }
  };
  
  // Helper function to render stat comparison
  const renderStatComparison = (
    label: string, 
    player1Value: number | string, 
    player2Value: number | string,
    isPercentage = false
  ) => {
    const p1Value = typeof player1Value === 'number' ? player1Value : parseInt(player1Value);
    const p2Value = typeof player2Value === 'number' ? player2Value : parseInt(player2Value);
    const total = p1Value + p2Value;
    const p1Percentage = total > 0 ? (p1Value / total) * 100 : 50;
    
    return (
      <div className="mb-4">
        <div className="flex justify-between mb-1">
          <span className="text-sm font-medium text-gray-700 dark:text-gray-300">{label}</span>
          <div className="flex space-x-4">
            <span className="text-sm font-medium text-blue-600 dark:text-blue-400">
              {player1Value}{isPercentage ? '%' : ''}
            </span>
            <span className="text-sm font-medium text-purple-600 dark:text-purple-400">
              {player2Value}{isPercentage ? '%' : ''}
            </span>
          </div>
        </div>
        <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2.5 overflow-hidden">
          <div 
            className="bg-blue-600 h-2.5" 
            style={{ width: `${p1Percentage}%` }}
          ></div>
        </div>
      </div>
    );
  };
  
  // Calculate percentages for overview tab
  const p1TotalPoints = stats.overview[player1].totalPoints;
  const p2TotalPoints = stats.overview[player2].totalPoints;
  const totalPoints = p1TotalPoints + p2TotalPoints;
  const p1PointsPercentage = Math.round((p1TotalPoints / totalPoints) * 100);
  const p2PointsPercentage = Math.round((p2TotalPoints / totalPoints) * 100);
  
  // Get player rally stats
  const p1RallyStats = stats.rally[player1];
  const p2RallyStats = stats.rally[player2];
  
  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 mb-8">
      <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">Match Statistics</h2>
      
      {/* Player Legend */}
      <div className="flex justify-center space-x-8 mb-6">
        <div className="flex items-center">
          <div className="w-4 h-4 bg-blue-600 rounded-full mr-2"></div>
          <span className="text-sm font-medium text-gray-700 dark:text-gray-300">{player1}</span>
        </div>
        <div className="flex items-center">
          <div className="w-4 h-4 bg-purple-600 rounded-full mr-2"></div>
          <span className="text-sm font-medium text-gray-700 dark:text-gray-300">{player2}</span>
        </div>
      </div>
      
      {/* Tabs */}
      <div className="border-b border-gray-200 dark:border-gray-700 mb-6">
        <nav className="-mb-px flex space-x-4" aria-label="Tabs">
          {['overview', 'serve', 'rally'].map((tab) => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              className={`py-2 px-1 border-b-2 font-medium text-sm ${
                activeTab === tab
                  ? 'border-indigo-500 text-indigo-600 dark:text-indigo-400'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300 dark:text-gray-400 dark:hover:text-gray-300'
              }`}
            >
              {tab.charAt(0).toUpperCase() + tab.slice(1)}
            </button>
          ))}
        </nav>
      </div>
      
      {/* Overview Tab */}
      {activeTab === 'overview' && (
        <div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-4">Service</h3>
              {renderStatComparison('Aces', stats.overview[player1].aces, stats.overview[player2].aces)}
              {renderStatComparison('Double Faults', stats.overview[player1].doubleFaults, stats.overview[player2].doubleFaults)}
              {renderStatComparison('First Serve %', stats.overview[player1].firstServePercentage, stats.overview[player2].firstServePercentage, true)}
              {renderStatComparison('First Serve Points Won %', stats.overview[player1].firstServePointsWon, stats.overview[player2].firstServePointsWon, true)}
              {renderStatComparison('Second Serve Points Won %', stats.overview[player1].secondServePointsWon, stats.overview[player2].secondServePointsWon, true)}
            </div>
            <div>
              <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-4">Return & Points</h3>
              {renderStatComparison(
                'Break Points Converted', 
                `${stats.overview[player1].breakPointsConverted}/${stats.overview[player1].breakPointOpportunities}`, 
                `${stats.overview[player2].breakPointsConverted}/${stats.overview[player2].breakPointOpportunities}`
              )}
              {renderStatComparison('Total Points Won', stats.overview[player1].totalPoints, stats.overview[player2].totalPoints)}
              
              {/* Visual representation of total points */}
              <div className="mt-6">
                <h4 className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Match Point Distribution</h4>
                <div className="relative pt-1">
                  <div className="flex h-4 overflow-hidden text-xs bg-gray-200 dark:bg-gray-700 rounded-full">
                    <div 
                      className="flex flex-col justify-center text-center text-white bg-blue-600 shadow-none whitespace-nowrap"
                      style={{ width: `${p1PointsPercentage}%` }}
                    ></div>
                    <div 
                      className="flex flex-col justify-center text-center text-white bg-purple-600 shadow-none whitespace-nowrap"
                      style={{ width: `${p2PointsPercentage}%` }}
                    ></div>
                  </div>
                </div>
                <div className="flex justify-between text-xs text-gray-600 dark:text-gray-400 mt-1">
                  <span>{p1PointsPercentage}%</span>
                  <span>{p2PointsPercentage}%</span>
                </div>
              </div>
            </div>
          </div>
          
          <div className="mt-6 text-sm text-gray-600 dark:text-gray-300">
            <p>
              <strong>{player1}</strong> had a stronger service game with {stats.overview[player1].aces} aces but struggled with break point conversion.
              <strong>{player2}</strong> was more consistent on serve with fewer double faults and a higher first serve percentage.
            </p>
          </div>
        </div>
      )}
      
      {/* Serve Tab */}
      {activeTab === 'serve' && (
        <div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-4">Serve Performance</h3>
              {renderStatComparison('Aces', stats.serve[player1].aces, stats.serve[player2].aces)}
              {renderStatComparison('Double Faults', stats.serve[player1].doubleFaults, stats.serve[player2].doubleFaults)}
              {renderStatComparison('First Serve %', stats.serve[player1].firstServePercentage, stats.serve[player2].firstServePercentage, true)}
              {renderStatComparison('Second Serve %', stats.serve[player1].secondServePercentage, stats.serve[player2].secondServePercentage, true)}
              {renderStatComparison('First Serve Points Won %', stats.serve[player1].firstServePointsWon, stats.serve[player2].firstServePointsWon, true)}
              {renderStatComparison('Second Serve Points Won %', stats.serve[player1].secondServePointsWon, stats.serve[player2].secondServePointsWon, true)}
            </div>
            <div>
              <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-4">Serve Direction</h3>
              
              {/* Serve Direction Visualization */}
              <div className="mb-4">
                <div className="flex justify-between mb-1">
                  <span className="text-sm font-medium text-gray-700 dark:text-gray-300">{player1}</span>
                </div>
                <div className="grid grid-cols-3 gap-2 mb-4">
                  <div className="bg-blue-100 dark:bg-blue-900 p-2 rounded text-center">
                    <div className="text-xs text-gray-500 dark:text-gray-400">Wide</div>
                    <div className="text-sm font-medium text-gray-900 dark:text-white">{stats.serve[player1].wideServes}%</div>
                  </div>
                  <div className="bg-blue-100 dark:bg-blue-900 p-2 rounded text-center">
                    <div className="text-xs text-gray-500 dark:text-gray-400">Body</div>
                    <div className="text-sm font-medium text-gray-900 dark:text-white">{stats.serve[player1].bodyServes}%</div>
                  </div>
                  <div className="bg-blue-100 dark:bg-blue-900 p-2 rounded text-center">
                    <div className="text-xs text-gray-500 dark:text-gray-400">T</div>
                    <div className="text-sm font-medium text-gray-900 dark:text-white">{stats.serve[player1].tServes}%</div>
                  </div>
                </div>
                
                <div className="flex justify-between mb-1">
                  <span className="text-sm font-medium text-gray-700 dark:text-gray-300">{player2}</span>
                </div>
                <div className="grid grid-cols-3 gap-2">
                  <div className="bg-purple-100 dark:bg-purple-900 p-2 rounded text-center">
                    <div className="text-xs text-gray-500 dark:text-gray-400">Wide</div>
                    <div className="text-sm font-medium text-gray-900 dark:text-white">{stats.serve[player2].wideServes}%</div>
                  </div>
                  <div className="bg-purple-100 dark:bg-purple-900 p-2 rounded text-center">
                    <div className="text-xs text-gray-500 dark:text-gray-400">Body</div>
                    <div className="text-sm font-medium text-gray-900 dark:text-white">{stats.serve[player2].bodyServes}%</div>
                  </div>
                  <div className="bg-purple-100 dark:bg-purple-900 p-2 rounded text-center">
                    <div className="text-xs text-gray-500 dark:text-gray-400">T</div>
                    <div className="text-sm font-medium text-gray-900 dark:text-white">{stats.serve[player2].tServes}%</div>
                  </div>
                </div>
              </div>
              
              <div className="text-sm text-gray-600 dark:text-gray-300">
                <p className="mb-2">
                  <strong>{player1}</strong> favors wide serves on the deuce court and T serves on the ad court.
                </p>
                <p>
                  <strong>{player2}</strong> has a more balanced serve distribution with a slight preference for T serves.
                </p>
              </div>
            </div>
          </div>
        </div>
      )}
      
      {/* Rally Tab */}
      {activeTab === 'rally' && (
        <div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-4">Shot Performance</h3>
              {renderStatComparison('Forehand Winners', p1RallyStats.forehandWinners, p2RallyStats.forehandWinners)}
              {renderStatComparison('Backhand Winners', p1RallyStats.backhandWinners, p2RallyStats.backhandWinners)}
              {renderStatComparison('Forehand Errors', p1RallyStats.forehandErrors, p2RallyStats.forehandErrors)}
              {renderStatComparison('Backhand Errors', p1RallyStats.backhandErrors, p2RallyStats.backhandErrors)}
              {renderStatComparison('Net Points Won', 
                `${p1RallyStats.netPointsWon}/${p1RallyStats.netPoints}`, 
                `${p2RallyStats.netPointsWon}/${p2RallyStats.netPoints}`
              )}
            </div>
            <div>
              <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-4">Rally Length</h3>
              
              {/* Rally Length Chart */}
              <div className="space-y-4">
                {Object.entries(stats.rally.rallyLengths).map(([length, values]) => {
                  // Ensure we have valid numbers for both players
                  const p1Value = values[player1] || 0;
                  const p2Value = values[player2] || 0;
                  const total = p1Value + p2Value;
                  const p1Percentage = total > 0 ? (p1Value / total) * 100 : 50;
                  
                  return (
                    <div key={length}>
                      <div className="flex justify-between mb-1">
                        <span className="text-sm font-medium text-gray-700 dark:text-gray-300">{length} shots</span>
                        <div className="flex space-x-4">
                          <span className="text-sm font-medium text-blue-600 dark:text-blue-400">
                            {p1Value}
                          </span>
                          <span className="text-sm font-medium text-purple-600 dark:text-purple-400">
                            {p2Value}
                          </span>
                        </div>
                      </div>
                      <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2.5 overflow-hidden">
                        <div 
                          className="bg-blue-600 h-2.5" 
                          style={{ width: `${p1Percentage}%` }}
                        ></div>
                      </div>
                    </div>
                  );
                })}
              </div>
              
              <div className="mt-4 text-sm text-gray-600 dark:text-gray-300">
                <p className="mb-2">
                  <strong>{player1}</strong> dominates in shorter rallies (1-3 shots), indicating strong serve and return game.
                </p>
                <p>
                  <strong>{player2}</strong> performs better in longer rallies (7+ shots), showing superior endurance and consistency.
                </p>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default StatisticalVisualizations;
