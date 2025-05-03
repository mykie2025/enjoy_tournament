"use client";

import React, { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import Link from 'next/link';
import MatchReplayViewer from '@/components/match-analysis/MatchReplayViewer';
import PointByPointBreakdown from '@/components/match-analysis/PointByPointBreakdown';
import StatisticalVisualizations from '@/components/match-analysis/StatisticalVisualizations';

interface MatchData {
  id: number;
  player1: string;
  player2: string;
  score: string;
  date: string;
  tournament: string;
  round: string;
}

export default function MatchAnalysisDetailPage() {
  const params = useParams();
  const matchId = Number(params.matchId);
  const [match, setMatch] = useState<MatchData | null>(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('replay');

  useEffect(() => {
    // In a real app, this would fetch data from the API
    // For now, we'll use mock data
    const fetchMatchData = async () => {
      setLoading(true);
      try {
        // Simulate API call
        await new Promise(resolve => setTimeout(resolve, 500));
        
        // Mock data
        const mockMatch: MatchData = {
          id: matchId,
          player1: 'Roger Federer',
          player2: 'Rafael Nadal',
          score: '6-4, 7-6, 6-3',
          date: 'May 1, 2025',
          tournament: 'Wimbledon',
          round: 'Final'
        };
        
        setMatch(mockMatch);
      } catch (error) {
        console.error('Error fetching match data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchMatchData();
  }, [matchId]);

  if (loading) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="flex items-center justify-center h-64">
          <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-indigo-500"></div>
        </div>
      </div>
    );
  }

  if (!match) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">Match Not Found</h1>
          <p className="text-gray-600 dark:text-gray-300 mb-6">
            The match you're looking for doesn't exist or has been removed.
          </p>
          <Link href="/match-analysis" className="text-indigo-600 dark:text-indigo-400 hover:text-indigo-800 dark:hover:text-indigo-300 font-medium">
            ← Back to Match Analysis
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Match Header */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 mb-8">
        <div className="flex flex-col md:flex-row md:items-center md:justify-between mb-4">
          <div>
            <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
              {match.player1} vs {match.player2}
            </h1>
            <p className="text-gray-600 dark:text-gray-300">
              {match.tournament} • {match.round} • {match.date}
            </p>
          </div>
          <div className="mt-4 md:mt-0">
            <span className="text-xl font-semibold text-gray-900 dark:text-white">
              Score: {match.score}
            </span>
          </div>
        </div>
        
        <div className="flex space-x-2">
          <Link href="/match-analysis" className="text-indigo-600 dark:text-indigo-400 hover:text-indigo-800 dark:hover:text-indigo-300 text-sm font-medium">
            ← Back to Match Analysis
          </Link>
        </div>
      </div>
      
      {/* Tabs */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 mb-8">
        <div className="border-b border-gray-200 dark:border-gray-700 mb-6">
          <nav className="-mb-px flex space-x-8" aria-label="Tabs">
            {['replay', 'points', 'stats'].map((tab) => (
              <button
                key={tab}
                onClick={() => setActiveTab(tab)}
                className={`py-4 px-1 border-b-2 font-medium text-sm ${
                  activeTab === tab
                    ? 'border-indigo-500 text-indigo-600 dark:text-indigo-400'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300 dark:text-gray-400 dark:hover:text-gray-300'
                }`}
              >
                {tab === 'replay' && 'Match Replay'}
                {tab === 'points' && 'Point-by-Point'}
                {tab === 'stats' && 'Statistics'}
              </button>
            ))}
          </nav>
        </div>
        
        {/* Tab Content */}
        {activeTab === 'replay' && (
          <MatchReplayViewer matchId={matchId} />
        )}
        
        {activeTab === 'points' && (
          <PointByPointBreakdown matchId={matchId} />
        )}
        
        {activeTab === 'stats' && (
          <StatisticalVisualizations 
            matchId={matchId} 
            player1={match.player1} 
            player2={match.player2} 
          />
        )}
      </div>
    </div>
  );
}
