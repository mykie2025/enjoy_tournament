import React, { useState } from 'react';

interface Point {
  id: number;
  pointNumber: number;
  gameScore: string;
  pointScore: string;
  server: string;
  winner: string;
  firstServeIn: boolean;
  serveType: string;
  returnType: string | null;
  rallyLength: number;
  winningShot: string;
}

interface PointByPointBreakdownProps {
  matchId: number;
  player1: string;
  player2: string;
}

const PointByPointBreakdown: React.FC<PointByPointBreakdownProps> = ({ matchId, player1, player2 }) => {
  const [currentSet, setCurrentSet] = useState(1);
  const [filterBy, setFilterBy] = useState('all');
  
  // Mock data for demonstration
  const totalSets = 3;
  const points: Point[] = Array.from({ length: 20 }, (_, i) => ({
    id: i + 1,
    pointNumber: i + 1,
    gameScore: `${Math.floor(i / 4)}-${Math.floor(i / 5)}`,
    pointScore: ['0-0', '15-0', '30-0', '40-0', '40-15', '40-30', 'Deuce', 'Adv', 'Game'][i % 9],
    server: i % 2 === 0 ? player1 : player2,
    winner: i % 3 === 0 ? player1 : player2,
    firstServeIn: i % 4 !== 0,
    serveType: ['Wide', 'Body', 'T'][i % 3],
    returnType: i % 5 === 0 ? null : ['Forehand', 'Backhand', 'Slice', 'Block'][i % 4],
    rallyLength: (i % 10) + 1,
    winningShot: ['Forehand Winner', 'Backhand Winner', 'Volley', 'Overhead', 'Ace', 'Forced Error', 'Unforced Error'][i % 7],
  }));
  
  const filteredPoints = points.filter(point => {
    if (filterBy === 'all') return true;
    if (filterBy === 'aces') return point.winningShot === 'Ace';
    if (filterBy === 'winners') return point.winningShot.includes('Winner') || point.winningShot === 'Volley' || point.winningShot === 'Overhead';
    if (filterBy === 'errors') return point.winningShot.includes('Error');
    if (filterBy === player1) return point.winner === player1;
    if (filterBy === player2) return point.winner === player2;
    return true;
  });
  
  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 mb-8">
      <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">Point-by-Point Breakdown</h2>
      
      {/* Filters */}
      <div className="flex flex-wrap items-center gap-4 mb-6">
        <div>
          <label htmlFor="set-selector" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
            Set
          </label>
          <select
            id="set-selector"
            value={currentSet}
            onChange={(e) => setCurrentSet(parseInt(e.target.value))}
            className="bg-gray-100 dark:bg-gray-700 border-gray-300 dark:border-gray-600 rounded-md text-sm"
          >
            {Array.from({ length: totalSets }, (_, i) => (
              <option key={i + 1} value={i + 1}>Set {i + 1}</option>
            ))}
          </select>
        </div>
        
        <div>
          <label htmlFor="filter-by" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
            Filter By
          </label>
          <select
            id="filter-by"
            value={filterBy}
            onChange={(e) => setFilterBy(e.target.value)}
            className="bg-gray-100 dark:bg-gray-700 border-gray-300 dark:border-gray-600 rounded-md text-sm"
          >
            <option value="all">All Points</option>
            <option value="aces">Aces</option>
            <option value="winners">Winners</option>
            <option value="errors">Errors</option>
            <option value={player1}>{player1} Points</option>
            <option value={player2}>{player2} Points</option>
          </select>
        </div>
      </div>
      
      {/* Points Table */}
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
          <thead className="bg-gray-50 dark:bg-gray-700">
            <tr>
              <th scope="col" className="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                #
              </th>
              <th scope="col" className="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                Game
              </th>
              <th scope="col" className="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                Point
              </th>
              <th scope="col" className="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                Server
              </th>
              <th scope="col" className="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                1st Serve
              </th>
              <th scope="col" className="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                Serve Type
              </th>
              <th scope="col" className="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                Rally
              </th>
              <th scope="col" className="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                Winner
              </th>
              <th scope="col" className="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                Winning Shot
              </th>
            </tr>
          </thead>
          <tbody className="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
            {filteredPoints.map((point) => (
              <tr 
                key={point.id}
                className="hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
              >
                <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-900 dark:text-white">
                  {point.pointNumber}
                </td>
                <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-900 dark:text-white">
                  {point.gameScore}
                </td>
                <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-900 dark:text-white">
                  {point.pointScore}
                </td>
                <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-900 dark:text-white">
                  {point.server}
                </td>
                <td className="px-4 py-3 whitespace-nowrap text-sm">
                  <span className={`px-2 py-1 inline-flex text-xs leading-5 font-semibold rounded-full ${
                    point.firstServeIn 
                      ? 'bg-green-100 text-green-800 dark:bg-green-800 dark:text-green-100' 
                      : 'bg-red-100 text-red-800 dark:bg-red-800 dark:text-red-100'
                  }`}>
                    {point.firstServeIn ? 'In' : 'Out'}
                  </span>
                </td>
                <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-900 dark:text-white">
                  {point.serveType}
                </td>
                <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-900 dark:text-white">
                  {point.rallyLength} shots
                </td>
                <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-900 dark:text-white">
                  <span className={`px-2 py-1 inline-flex text-xs leading-5 font-semibold rounded-full ${
                    point.winner === player1
                      ? 'bg-blue-100 text-blue-800 dark:bg-blue-800 dark:text-blue-100'
                      : 'bg-purple-100 text-purple-800 dark:bg-purple-800 dark:text-purple-100'
                  }`}>
                    {point.winner}
                  </span>
                </td>
                <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-900 dark:text-white">
                  {point.winningShot}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      
      {filteredPoints.length === 0 && (
        <div className="text-center py-8 text-gray-500 dark:text-gray-400">
          No points match the selected filters.
        </div>
      )}
    </div>
  );
};

export default PointByPointBreakdown;
