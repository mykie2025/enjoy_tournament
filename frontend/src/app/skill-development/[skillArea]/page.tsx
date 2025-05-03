"use client";

import React, { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import Link from 'next/link';
import TechniqueAnalysisViewer from '@/components/skill-development/TechniqueAnalysisViewer';
import TrainingRecommendations from '@/components/skill-development/TrainingRecommendations';
import ProgressTracking from '@/components/skill-development/ProgressTracking';

interface SkillAreaData {
  id: string;
  name: string;
  description: string;
  icon: string;
}

export default function SkillDevelopmentDetailPage() {
  const params = useParams();
  const skillArea = params.skillArea as string;
  const [skillData, setSkillData] = useState<SkillAreaData | null>(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('technique');
  
  // Mock user ID for demonstration
  const userId = 1;

  useEffect(() => {
    // In a real app, this would fetch data from the API
    // For now, we'll use mock data
    const fetchSkillData = async () => {
      setLoading(true);
      try {
        // Simulate API call
        await new Promise(resolve => setTimeout(resolve, 500));
        
        // Mock data based on skill area
        let mockSkill: SkillAreaData;
        
        switch (skillArea) {
          case 'technical-skills':
            mockSkill = {
              id: 'technical-skills',
              name: 'Technical Skills',
              description: 'Stroke techniques, footwork, and movement patterns',
              icon: '🎯'
            };
            break;
          case 'tactical-skills':
            mockSkill = {
              id: 'tactical-skills',
              name: 'Tactical Skills',
              description: 'Game strategy, shot selection, and court positioning',
              icon: '🧠'
            };
            break;
          case 'mental-skills':
            mockSkill = {
              id: 'mental-skills',
              name: 'Mental Skills',
              description: 'Focus, resilience, and pressure management',
              icon: '🧘'
            };
            break;
          default:
            mockSkill = {
              id: skillArea,
              name: skillArea.split('-').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' '),
              description: 'Detailed analysis and recommendations',
              icon: '📊'
            };
        }
        
        setSkillData(mockSkill);
      } catch (error) {
        console.error('Error fetching skill data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchSkillData();
  }, [skillArea]);

  if (loading) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="flex items-center justify-center h-64">
          <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-indigo-500"></div>
        </div>
      </div>
    );
  }

  if (!skillData) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">Skill Area Not Found</h1>
          <p className="text-gray-600 dark:text-gray-300 mb-6">
            The skill area you're looking for doesn't exist or has been removed.
          </p>
          <Link href="/skill-development" className="text-indigo-600 dark:text-indigo-400 hover:text-indigo-800 dark:hover:text-indigo-300 font-medium">
            ← Back to Skill Development
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Skill Area Header */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 mb-8">
        <div className="flex items-center mb-4">
          <span className="text-3xl mr-3">{skillData.icon}</span>
          <div>
            <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
              {skillData.name}
            </h1>
            <p className="text-gray-600 dark:text-gray-300">
              {skillData.description}
            </p>
          </div>
        </div>
        
        <div className="flex space-x-2">
          <Link href="/skill-development" className="text-indigo-600 dark:text-indigo-400 hover:text-indigo-800 dark:hover:text-indigo-300 text-sm font-medium">
            ← Back to Skill Development
          </Link>
        </div>
      </div>
      
      {/* Tabs */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 mb-8">
        <div className="border-b border-gray-200 dark:border-gray-700 mb-6">
          <nav className="-mb-px flex space-x-8" aria-label="Tabs">
            {['technique', 'training', 'progress'].map((tab) => (
              <button
                key={tab}
                onClick={() => setActiveTab(tab)}
                className={`py-4 px-1 border-b-2 font-medium text-sm ${
                  activeTab === tab
                    ? 'border-indigo-500 text-indigo-600 dark:text-indigo-400'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300 dark:text-gray-400 dark:hover:text-gray-300'
                }`}
              >
                {tab === 'technique' && 'Technique Analysis'}
                {tab === 'training' && 'Training Recommendations'}
                {tab === 'progress' && 'Progress Tracking'}
              </button>
            ))}
          </nav>
        </div>
        
        {/* Tab Content */}
        {activeTab === 'technique' && (
          <TechniqueAnalysisViewer userId={userId} />
        )}
        
        {activeTab === 'training' && (
          <TrainingRecommendations userId={userId} />
        )}
        
        {activeTab === 'progress' && (
          <ProgressTracking userId={userId} />
        )}
      </div>
    </div>
  );
}
