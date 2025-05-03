'use client';

import { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Badge } from '@/components/ui/badge';
import { Skeleton } from '@/components/ui/skeleton';
import config from '../config';

interface Competitor {
  id: string;
  name: string;
  country: {
    name: string;
  };
  abbreviation?: string;
}

interface Tournament {
  id: string;
  name: string;
  category: {
    name: string;
  };
}

interface SportEvent {
  id: string;
  scheduled: string;
  status: string;
  tournament: Tournament;
  venue?: {
    name: string;
    city: {
      name: string;
    };
    country: {
      name: string;
    };
  };
  competitors: Competitor[];
  sport_event_status?: {
    status: string;
    match_status: string;
    home_score: number;
    away_score: number;
    winner_id?: string;
  };
}

interface LiveMatchesResponse {
  generated_at: string;
  sport_events: SportEvent[];
}

interface TournamentItem {
  id: string;
  name: string;
  category?: string;
  status: string;
  match_count: number;
  start_date?: string;
  end_date?: string;
  year?: string;
  season_ids?: string[];
}

export default function TournamentInfoPage() {
  const [liveMatches, setLiveMatches] = useState<SportEvent[]>([]);
  const [upcomingMatches, setUpcomingMatches] = useState<SportEvent[]>([]);
  const [tournaments, setTournaments] = useState<TournamentItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [retryCount, setRetryCount] = useState(0);

  const fetchTournamentData = async () => {
    try {
      setLoading(true);
      setError(null);
      
      // Fetch live matches directly from backend
      const liveApiUrl = `${config.apiServer.baseUrl}/tournaments/api/live`;
      console.log(`Fetching live matches from ${liveApiUrl}`);
      
      const liveResponse = await fetch(liveApiUrl);
      
      if (!liveResponse.ok) {
        throw new Error(`Failed to fetch live tournament data: Backend API returned ${liveResponse.status}: ${liveResponse.statusText}`);
      }
      
      const liveData = await liveResponse.json();
      console.log('Live matches data:', liveData);
      setLiveMatches(liveData.data?.sport_events || []);

      // Fetch upcoming matches for today directly from backend
      const todayApiUrl = `${config.apiServer.baseUrl}/tournaments/api/today`;
      console.log(`Fetching daily matches from ${todayApiUrl}`);
      
      const todayResponse = await fetch(todayApiUrl);
      
      if (!todayResponse.ok) {
        throw new Error(`Failed to fetch daily tournament data: Backend API returned ${todayResponse.status}: ${todayResponse.statusText}`);
      }
      
      const todayData = await todayResponse.json();
      console.log('Daily matches data:', todayData);
      
      // Filter for upcoming matches (not live or completed)
      const upcoming = (todayData.data?.sport_events || []).filter(
        (event: SportEvent) => event.status !== 'closed' && 
                             (!event.sport_event_status || 
                              event.sport_event_status.match_status !== 'live')
      );
      setUpcomingMatches(upcoming.slice(0, config.ui.matchDisplayLimit));
      
      // Fetch all tournaments
      const tournamentsApiUrl = `${config.apiServer.baseUrl}/tournaments/api/all`;
      console.log(`Fetching all tournaments from ${tournamentsApiUrl}`);
      
      const tournamentsResponse = await fetch(tournamentsApiUrl);
      
      if (!tournamentsResponse.ok) {
        throw new Error(`Failed to fetch tournaments: Backend API returned ${tournamentsResponse.status}: ${tournamentsResponse.statusText}`);
      }
      
      const tournamentsData = await tournamentsResponse.json();
      console.log('Tournaments data:', tournamentsData);
      setTournaments(tournamentsData.data?.tournaments || []);
      
    } catch (err) {
      console.error('Error fetching tournament data:', err);
      setError(err instanceof Error ? err.message : 'An unknown error occurred');
      
      // Retry logic - retry up to 3 times with exponential backoff
      if (retryCount < 3) {
        const nextRetryCount = retryCount + 1;
        setRetryCount(nextRetryCount);
        const backoffTime = Math.pow(2, nextRetryCount) * 1000; // 2s, 4s, 8s
        
        console.log(`Retrying in ${backoffTime/1000} seconds (attempt ${nextRetryCount}/3)...`);
        setTimeout(() => {
          fetchTournamentData();
        }, backoffTime);
      }
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTournamentData();
    
    // Refresh data based on config interval
    const intervalId = setInterval(fetchTournamentData, config.ui.autoRefreshInterval * 1000);
    
    return () => clearInterval(intervalId);
  }, []);

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  const getScoreDisplay = (event: SportEvent) => {
    if (!event.sport_event_status) return 'vs';
    
    const { home_score, away_score } = event.sport_event_status;
    return `${home_score} - ${away_score}`;
  };

  const getStatusBadge = (event: SportEvent) => {
    if (event.status === 'closed') {
      return <Badge variant="outline" className="bg-gray-100">Completed</Badge>;
    }
    
    if (event.sport_event_status?.match_status === 'live') {
      return <Badge className="bg-red-500">Live</Badge>;
    }
    
    return <Badge variant="outline" className="bg-blue-100">Upcoming</Badge>;
  };

  const getTournamentStatusBadge = (status: string) => {
    if (status === 'live') {
      return <Badge className="bg-red-500">Live</Badge>;
    }
    
    return <Badge variant="outline" className="bg-blue-100">Scheduled</Badge>;
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

  const handleRetry = () => {
    setRetryCount(0);
    fetchTournamentData();
  };

  return (
    <div className="container mx-auto py-8">
      <h1 className="text-3xl font-bold mb-6">Tennis Tournament Information</h1>
      
      {error && (
        <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-md">
          <h3 className="text-lg font-semibold text-red-700 mb-2">Error</h3>
          <p className="text-red-600 mb-3">{error}</p>
          <button 
            onClick={handleRetry}
            className="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700"
          >
            Retry
          </button>
        </div>
      )}
      
      <Tabs defaultValue="tournaments" className="w-full">
        <TabsList className="grid w-full grid-cols-3">
          <TabsTrigger value="tournaments">Tournaments</TabsTrigger>
          <TabsTrigger value="live">Live Matches</TabsTrigger>
          <TabsTrigger value="upcoming">Upcoming Matches</TabsTrigger>
        </TabsList>
        
        <TabsContent value="tournaments">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {loading ? (
              Array(6).fill(0).map((_, i) => (
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
              ))
            ) : error ? (
              <div className="col-span-full p-4 bg-red-50 text-red-500 rounded-md">
                {error}
              </div>
            ) : tournaments.length === 0 ? (
              <div className="col-span-full p-4 bg-gray-50 text-gray-500 rounded-md">
                No tournaments available at the moment.
              </div>
            ) : (
              tournaments.map((tournament) => (
                <Card key={tournament.id} className="overflow-hidden">
                  <CardHeader className="pb-2">
                    <div className="flex justify-between items-center">
                      <CardDescription>
                        {tournament.category || tournament.year || 'Tennis Tournament'}
                      </CardDescription>
                      {getTournamentStatusBadge(tournament.status)}
                    </div>
                    <CardTitle className="text-lg">
                      {tournament.name}
                    </CardTitle>
                    {tournament.start_date && tournament.end_date && (
                      <p className="text-xs text-gray-500 mt-1">
                        {formatTournamentDates(tournament.start_date, tournament.end_date)}
                      </p>
                    )}
                  </CardHeader>
                  <CardContent>
                    <div className="flex justify-between items-center">
                      <div className="text-sm text-gray-500">
                        {tournament.match_count} {tournament.match_count === 1 ? 'match' : 'matches'}
                      </div>
                      <button 
                        className="px-3 py-1 bg-blue-600 text-white text-sm rounded-md hover:bg-blue-700"
                        onClick={() => window.location.href = `/tournament/${tournament.id}`}
                      >
                        View Details
                      </button>
                    </div>
                  </CardContent>
                </Card>
              ))
            )}
          </div>
        </TabsContent>
        
        <TabsContent value="live">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {loading ? (
              Array(3).fill(0).map((_, i) => (
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
              ))
            ) : error ? (
              <div className="col-span-full p-4 bg-red-50 text-red-500 rounded-md">
                {error}
              </div>
            ) : liveMatches.length === 0 ? (
              <div className="col-span-full p-4 bg-gray-50 text-gray-500 rounded-md">
                No live matches at the moment.
              </div>
            ) : (
              liveMatches.map((match) => (
                <Card key={match.id} className="overflow-hidden">
                  <CardHeader className="pb-2">
                    <div className="flex justify-between items-center">
                      <CardDescription>
                        {match.tournament.name}
                      </CardDescription>
                      {getStatusBadge(match)}
                    </div>
                    <CardTitle className="text-lg">
                      {match.venue?.name || 'Unknown Venue'}
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="flex justify-between items-center mb-2">
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
                    <p className="text-xs text-gray-500 text-center">
                      Started at {formatDate(match.scheduled)}
                    </p>
                  </CardContent>
                </Card>
              ))
            )}
          </div>
        </TabsContent>
        
        <TabsContent value="upcoming">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {loading ? (
              Array(3).fill(0).map((_, i) => (
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
              ))
            ) : error ? (
              <div className="col-span-full p-4 bg-red-50 text-red-500 rounded-md">
                {error}
              </div>
            ) : upcomingMatches.length === 0 ? (
              <div className="col-span-full p-4 bg-gray-50 text-gray-500 rounded-md">
                No upcoming matches scheduled for today.
              </div>
            ) : (
              upcomingMatches.map((match) => (
                <Card key={match.id} className="overflow-hidden">
                  <CardHeader className="pb-2">
                    <div className="flex justify-between items-center">
                      <CardDescription>
                        {match.tournament.name}
                      </CardDescription>
                      {getStatusBadge(match)}
                    </div>
                    <CardTitle className="text-lg">
                      {match.venue?.name || 'Unknown Venue'}
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="flex justify-between items-center mb-2">
                      <div className="flex-1 text-left">
                        <p className="font-semibold">{match.competitors[0]?.name}</p>
                        <p className="text-xs text-gray-500">{match.competitors[0]?.country.name}</p>
                      </div>
                      <div className="px-4 py-2 bg-gray-100 rounded-md font-bold">
                        vs
                      </div>
                      <div className="flex-1 text-right">
                        <p className="font-semibold">{match.competitors[1]?.name}</p>
                        <p className="text-xs text-gray-500">{match.competitors[1]?.country.name}</p>
                      </div>
                    </div>
                    <p className="text-xs text-gray-500 text-center">
                      Scheduled for {formatDate(match.scheduled)}
                    </p>
                  </CardContent>
                </Card>
              ))
            )}
          </div>
        </TabsContent>
      </Tabs>
    </div>
  );
}
