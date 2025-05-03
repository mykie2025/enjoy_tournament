import React, { useState } from 'react';

interface MatchReplayViewerProps {
  matchId: number;
  player1: string;
  player2: string;
}

const MatchReplayViewer: React.FC<MatchReplayViewerProps> = ({ matchId, player1, player2 }) => {
  const [currentPoint, setCurrentPoint] = useState(1);
  const [isPlaying, setIsPlaying] = useState(false);
  const [playbackSpeed, setPlaybackSpeed] = useState(1);
  
  // Mock data for demonstration
  const totalPoints = 25;
  const currentScore = "30-15";
  const currentGame = "4-3";
  const currentSet = "1-0";
  
  const handlePrevPoint = () => {
    if (currentPoint > 1) {
      setCurrentPoint(currentPoint - 1);
    }
  };
  
  const handleNextPoint = () => {
    if (currentPoint < totalPoints) {
      setCurrentPoint(currentPoint + 1);
    }
  };
  
  const togglePlayback = () => {
    setIsPlaying(!isPlaying);
  };
  
  const handleSpeedChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setPlaybackSpeed(parseFloat(e.target.value));
  };
  
  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 mb-8">
      <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">Match Replay</h2>
      
      {/* Court Visualization */}
      <div className="relative w-full h-64 bg-green-600 rounded-lg mb-6">
        {/* Tennis court markings */}
        <div className="absolute inset-0 flex items-center justify-center">
          <div className="w-3/4 h-full border-2 border-white flex">
            <div className="w-1/2 h-full border-r-2 border-white flex items-center justify-center">
              <div className="w-1/2 h-1/2 border-2 border-white"></div>
            </div>
            <div className="w-1/2 h-full flex items-center justify-center">
              <div className="w-1/2 h-1/2 border-2 border-white"></div>
            </div>
          </div>
        </div>
        
        {/* Net */}
        <div className="absolute top-0 left-1/2 h-full w-1 bg-white transform -translate-x-1/2"></div>
        
        {/* Players */}
        <div className="absolute bottom-10 left-1/4 w-6 h-6 bg-red-500 rounded-full transform -translate-x-1/2" title={player1}></div>
        <div className="absolute top-10 right-1/4 w-6 h-6 bg-blue-500 rounded-full transform translate-x-1/2" title={player2}></div>
        
        {/* Ball */}
        <div className="absolute top-1/2 left-1/2 w-3 h-3 bg-yellow-300 rounded-full transform -translate-x-1/2 -translate-y-1/2 shadow-md"></div>
      </div>
      
      {/* Playback Controls */}
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center space-x-4">
          <button 
            onClick={handlePrevPoint}
            disabled={currentPoint === 1}
            className="bg-gray-200 dark:bg-gray-700 p-2 rounded-full disabled:opacity-50"
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z" clipRule="evenodd" />
            </svg>
          </button>
          
          <button 
            onClick={togglePlayback}
            className="bg-indigo-600 hover:bg-indigo-700 text-white p-2 rounded-full"
          >
            {isPlaying ? (
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zM7 8a1 1 0 012 0v4a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v4a1 1 0 102 0V8a1 1 0 00-1-1z" clipRule="evenodd" />
              </svg>
            ) : (
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2z" clipRule="evenodd" />
              </svg>
            )}
          </button>
          
          <button 
            onClick={handleNextPoint}
            disabled={currentPoint === totalPoints}
            className="bg-gray-200 dark:bg-gray-700 p-2 rounded-full disabled:opacity-50"
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clipRule="evenodd" />
            </svg>
          </button>
        </div>
        
        <div className="flex items-center space-x-2">
          <span className="text-sm text-gray-600 dark:text-gray-300">Speed:</span>
          <select 
            value={playbackSpeed}
            onChange={handleSpeedChange}
            className="bg-gray-100 dark:bg-gray-700 border-gray-300 dark:border-gray-600 rounded-md text-sm"
          >
            <option value="0.5">0.5x</option>
            <option value="1">1x</option>
            <option value="1.5">1.5x</option>
            <option value="2">2x</option>
          </select>
        </div>
      </div>
      
      {/* Point Information */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
        <div className="bg-gray-100 dark:bg-gray-700 p-4 rounded-lg">
          <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">Point</h3>
          <p className="text-lg font-semibold text-gray-900 dark:text-white">{currentPoint} of {totalPoints}</p>
        </div>
        
        <div className="bg-gray-100 dark:bg-gray-700 p-4 rounded-lg">
          <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">Score</h3>
          <div className="flex items-center justify-between">
            <p className="text-lg font-semibold text-gray-900 dark:text-white">{currentSet}</p>
            <p className="text-lg font-semibold text-gray-900 dark:text-white">{currentGame}</p>
            <p className="text-lg font-semibold text-gray-900 dark:text-white">{currentScore}</p>
          </div>
        </div>
        
        <div className="bg-gray-100 dark:bg-gray-700 p-4 rounded-lg">
          <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">Server</h3>
          <p className="text-lg font-semibold text-gray-900 dark:text-white">{currentPoint % 2 === 0 ? player2 : player1}</p>
        </div>
      </div>
      
      {/* Point Details */}
      <div className="bg-gray-100 dark:bg-gray-700 p-4 rounded-lg">
        <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400 mb-2">Point Details</h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div>
            <span className="block text-xs text-gray-500 dark:text-gray-400">Serve Type</span>
            <span className="block text-sm font-medium text-gray-900 dark:text-white">Wide</span>
          </div>
          <div>
            <span className="block text-xs text-gray-500 dark:text-gray-400">Return Type</span>
            <span className="block text-sm font-medium text-gray-900 dark:text-white">Backhand</span>
          </div>
          <div>
            <span className="block text-xs text-gray-500 dark:text-gray-400">Rally Length</span>
            <span className="block text-sm font-medium text-gray-900 dark:text-white">7 shots</span>
          </div>
          <div>
            <span className="block text-xs text-gray-500 dark:text-gray-400">Winner</span>
            <span className="block text-sm font-medium text-gray-900 dark:text-white">{player1}</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default MatchReplayViewer;
