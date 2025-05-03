'use client';

import { useState, useEffect } from 'react';
import { useParams } from 'next/navigation';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Skeleton } from '@/components/ui/skeleton';
import { ArrowLeft } from 'lucide-react';
import Link from 'next/link';
import config from '../../config';

interface Match {
  id: string;
  scheduled: string;
  status: string;
  competitors: Array<{
    id: string;
    name: string;
    country: {
      name: string;
    };
  }>;
  sport_event_status?: {
    match_status: string;
    home_score: number;
    away_score: number;
    winner_id?: string;
  };
}

interface TournamentDetails {
  id: string;
  name: string;
  category?: string;
  status: string;
  matches: Match[];
  start_date?: string;
  end_date?: string;
  year?: string;
  season_ids?: string[];
}

export default function TournamentDetailsPage() {
  const params = useParams();
  const tournamentId = params.id as string;
  
  const [tournament, setTournament] = useState<TournamentDetails | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchTournamentDetails = async () => {
      try {
        setLoading(true);
        setError(null);
        
        // First, get tournament info from the backend
        const apiUrl = `${config.apiServer.baseUrl}/tournaments/api/all`;
        const response = await fetch(apiUrl);
        
        if (!response.ok) {
          throw new Error(`Failed to fetch tournament data: ${response.statusText}`);
        }
        
        const data = await response.json();
        
        // Find the specific tournament
        const tournamentsList = data.data?.tournaments || [];
        const tournamentInfo = tournamentsList.find((t: any) => t.id === tournamentId);
        
        if (!tournamentInfo) {
          throw new Error('Tournament not found');
        }
        
        // Get matches for this tournament from both live and daily endpoints
        const liveResponse = await fetch(`${config.apiServer.baseUrl}/tournaments/api/live`);
        const dailyResponse = await fetch(`${config.apiServer.baseUrl}/tournaments/api/today`);
        
        if (!liveResponse.ok || !dailyResponse.ok) {
          throw new Error('Failed to fetch tournament matches');
        }
        
        const liveData = await liveResponse.json();
        const dailyData = await dailyResponse.json();
        
        // Filter matches for this tournament
        const liveMatches = (liveData.data?.sport_events || []).filter(
          (match: any) => match.tournament?.id === tournamentId || 
                         match.tournament?.category?.id === tournamentId
        );
        
        const dailyMatches = (dailyData.data?.sport_events || []).filter(
          (match: any) => match.tournament?.id === tournamentId || 
                         match.tournament?.category?.id === tournamentId
        );
        
        // Combine and deduplicate matches
        const allMatches = [...liveMatches];
        dailyMatches.forEach((match: any) => {
          if (!allMatches.some(m => m.id === match.id)) {
            allMatches.push(match);
          }
        });
        
        // Sort matches: live first, then by scheduled time
        allMatches.sort((a, b) => {
          const aIsLive = a.sport_event_status?.match_status === 'live';
          const bIsLive = b.sport_event_status?.match_status === 'live';
          
          if (aIsLive && !bIsLive) return -1;
          if (!aIsLive && bIsLive) return 1;
          
          return new Date(a.scheduled).getTime() - new Date(b.scheduled).getTime();
        });
        
        setTournament({
          ...tournamentInfo,
          matches: allMatches
        });
      } catch (err) {
        console.error('Error fetching tournament details:', err);
        setError(err instanceof Error ? err.message : 'An unknown error occurred');
      } finally {
        setLoading(false);
      }
    };
    
    fetchTournamentDetails();
  }, [tournamentId]);
  
  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleString(undefined, { 
      weekday: 'short',
      month: 'short', 
      day: 'numeric',
      hour: '2-digit', 
      minute: '2-digit'
    });
  };
  
  const formatTournamentDates = (startDate?: string, endDate?: string) => {
    if (!startDate || !endDate) return '';
    
    const start = new Date(startDate);
    const end = new Date(endDate);
    
    const startMonth = start.toLocaleString('default', { month: 'short' });
    const endMonth = end.toLocaleString('default', { month: 'short' });
    
    if (startMonth === endMonth) {
      return `${startMonth} ${start.getDate()} - ${end.getDate()}, ${end.getFullYear()}`;
    }
    
    return `${startMonth} ${start.getDate()} - ${endMonth} ${end.getDate()}, ${end.getFullYear()}`;
  };
  
  const getMatchStatusBadge = (match: Match) => {
    if (match.sport_event_status?.match_status === 'live') {
      return <Badge className="bg-red-500">Live</Badge>;
    }
    
    if (match.status === 'closed') {
      return <Badge variant="outline" className="bg-gray-100">Completed</Badge>;
    }
    
    return <Badge variant="outline" className="bg-blue-100">Upcoming</Badge>;
  };
  
  const getScoreDisplay = (match: Match) => {
    if (!match.sport_event_status) return 'vs';
    
    const { home_score, away_score } = match.sport_event_status;
    return `${home_score} - ${away_score}`;
  };

  if (loading) {
    return (
      <div className="container mx-auto py-8">
        <div className="mb-6">
          <Link href="/tournament-info" className="flex items-center text-blue-600 hover:text-blue-800">
            <ArrowLeft className="mr-2 h-4 w-4" />
            Back to Tournaments
          </Link>
        </div>
        <Skeleton className="h-10 w-3/4 mb-6" />
        <Skeleton className="h-6 w-1/2 mb-8" />
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {Array(4).fill(0).map((_, i) => (
            <Card key={i} className="overflow-hidden">
              <CardHeader className="pb-2">
                <Skeleton className="h-4 w-1/2 mb-2" />
                <Skeleton className="h-6 w-3/4" />
              </CardHeader>
              <CardContent>
                <Skeleton className="h-16 w-full mb-2" />
                <Skeleton className="h-4 w-1/3" />
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container mx-auto py-8">
        <div className="mb-6">
          <Link href="/tournament-info" className="flex items-center text-blue-600 hover:text-blue-800">
            <ArrowLeft className="mr-2 h-4 w-4" />
            Back to Tournaments
          </Link>
        </div>
        <div className="p-4 bg-red-50 border border-red-200 rounded-md">
          <h3 className="text-lg font-semibold text-red-700 mb-2">Error</h3>
          <p className="text-red-600">{error}</p>
        </div>
      </div>
    );
  }

  if (!tournament) {
    return (
      <div className="container mx-auto py-8">
        <div className="mb-6">
          <Link href="/tournament-info" className="flex items-center text-blue-600 hover:text-blue-800">
            <ArrowLeft className="mr-2 h-4 w-4" />
            Back to Tournaments
          </Link>
        </div>
        <div className="p-4 bg-yellow-50 border border-yellow-200 rounded-md">
          <h3 className="text-lg font-semibold text-yellow-700 mb-2">Tournament Not Found</h3>
          <p className="text-yellow-600">The requested tournament could not be found.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto py-8">
      <div className="mb-6">
        <Link href="/tournament-info" className="flex items-center text-blue-600 hover:text-blue-800">
          <ArrowLeft className="mr-2 h-4 w-4" />
          Back to Tournaments
        </Link>
      </div>
      
      <h1 className="text-3xl font-bold mb-2">{tournament.name}</h1>
      <div className="flex items-center mb-6">
        {tournament.category && (
          <span className="text-gray-600 mr-4">{tournament.category}</span>
        )}
        {tournament.start_date && tournament.end_date && (
          <span className="text-gray-600">
            {formatTournamentDates(tournament.start_date, tournament.end_date)}
          </span>
        )}
      </div>
      
      <h2 className="text-xl font-semibold mb-4">Matches</h2>
      
      {tournament.matches.length === 0 ? (
        <div className="p-4 bg-gray-50 border border-gray-200 rounded-md">
          <p className="text-gray-600">No matches found for this tournament.</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {tournament.matches.map((match) => (
            <Card key={match.id} className="overflow-hidden">
              <CardHeader className="pb-2">
                <div className="flex justify-between items-center">
                  <CardDescription>
                    {formatDate(match.scheduled)}
                  </CardDescription>
                  {getMatchStatusBadge(match)}
                </div>
              </CardHeader>
              <CardContent>
                <div className="flex justify-between items-center mb-4">
                  <div className="flex-1 text-left">
                    <p className="font-semibold">{match.competitors[0]?.name}</p>
                    <p className="text-xs text-gray-500">{match.competitors[0]?.country.name}</p>
                  </div>
                  <div className="px-4 py-2 bg-gray-100 rounded-md font-bold">
                    {getScoreDisplay(match)}
                  </div>
                  <div className="flex-1 text-right">
                    <p className="font-semibold">{match.competitors[1]?.name}</p>
                    <p className="text-xs text-gray-500">{match.competitors[1]?.country.name}</p>
                  </div>
                </div>
                <Link 
                  href={`/match/${match.id}`}
                  className="block w-full text-center py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
                >
                  Match Details
                </Link>
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}
