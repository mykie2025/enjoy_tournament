'use client';

import { useState, useEffect } from 'react';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Badge } from '@/components/ui/badge';
import { Skeleton } from '@/components/ui/skeleton';
import { Button } from '../../components/ui/button';
import { toast } from '../../components/ui/use-toast';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "../../components/ui/table"
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
  is_selected?: boolean;
  external_id?: string;
}

export default function TournamentInfoPage() {
  const [liveMatches, setLiveMatches] = useState<SportEvent[]>([]);
  const [upcomingMatches, setUpcomingMatches] = useState<SportEvent[]>([]);
  const [tournaments, setTournaments] = useState<TournamentItem[]>([]);
  const [selectedTournaments, setSelectedTournaments] = useState<TournamentItem[]>([]);
  const [endedTournaments, setEndedTournaments] = useState<TournamentItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [retryCount, setRetryCount] = useState(0);
  const [selectingTournament, setSelectingTournament] = useState<string | null>(null);
  const [checkedTournaments, setCheckedTournaments] = useState<Set<string>>(new Set());
  const [savingMultiple, setSavingMultiple] = useState(false); 
  const [activeTab, setActiveTab] = useState("tournaments");

  // Ensure checkboxes are unchecked when component mounts
  useEffect(() => {
    setCheckedTournaments(new Set());
  }, []);

  useEffect(() => {
    fetchTournamentData();
  }, [retryCount]);

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
      // Ensure external_id is properly set for each tournament
      const mappedTournaments = (tournamentsData.data?.tournaments || []).map((t: any) => ({
        ...t,
        external_id: t.external_id || t.id // fallback to id if external_id is not set
      }));
      console.log('Mapped tournaments with external_id:', mappedTournaments);
      setTournaments(mappedTournaments);
      
      // Fetch selected tournaments
      const selectedApiUrl = `${config.apiServer.baseUrl}/tournaments/selected`;
      console.log(`Fetching selected tournaments from ${selectedApiUrl}`);
      
      const selectedResponse = await fetch(selectedApiUrl);
      
      if (!selectedResponse.ok) {
        throw new Error(`Failed to fetch selected tournaments: Backend API returned ${selectedResponse.status}: ${selectedResponse.statusText}`);
      }
      
      const selectedData = await selectedResponse.json();
      console.log('Selected tournaments data:', selectedData);
      console.log('DEBUG: Setting selectedTournaments state with:', selectedData.data?.tournaments || []);
      // Ensure external_id is properly set for each selected tournament
      const mappedSelectedTournaments = (selectedData.data?.tournaments || []).map((t: any) => ({
        ...t,
        external_id: t.external_id || t.id // fallback to id if external_id is not set
      }));
      console.log('Mapped selected tournaments with external_id:', mappedSelectedTournaments);
      setSelectedTournaments(mappedSelectedTournaments);
      
      // Fetch ended selected tournaments
      const endedApiUrl = `${config.apiServer.baseUrl}/tournaments/selected/ended`;
      console.log(`Fetching ended tournaments from ${endedApiUrl}`);
      
      const endedResponse = await fetch(endedApiUrl);
      
      if (!endedResponse.ok) {
        throw new Error(`Failed to fetch ended tournaments: Backend API returned ${endedResponse.status}: ${endedResponse.statusText}`);
      }
      
      const endedData = await endedResponse.json();
      console.log('Ended tournaments data:', endedData);
      // Ensure external_id is properly set for each ended tournament
      const mappedEndedTournaments = (endedData.data?.tournaments || []).map((t: any) => ({
        ...t,
        external_id: t.external_id || t.id // fallback to id if external_id is not set
      }));
      console.log('Mapped ended tournaments with external_id:', mappedEndedTournaments);
      setEndedTournaments(mappedEndedTournaments);
      
      // Update tournament statuses
      await fetch(`${config.apiServer.baseUrl}/tournaments/update-status`, {
        method: 'PUT'
      });
      
    } catch (err) {
      console.error('Error fetching tournament data:', err);
      setError(`Failed to load tournament data: ${err instanceof Error ? err.message : String(err)}`);
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleString('en-US', { month: 'short', day: 'numeric', hour: 'numeric', minute: '2-digit' });
  };
  
  const getScoreDisplay = (event: SportEvent) => {
    if (event.sport_event_status) {
      return `${event.sport_event_status.home_score} - ${event.sport_event_status.away_score}`;
    }
    return 'vs';
  };
  
  const getStatusBadge = (event: SportEvent) => {
    const status = event.sport_event_status?.match_status || event.status;
    
    if (status === 'live') {
      return <Badge className="bg-red-500 hover:bg-red-600">LIVE</Badge>;
    } else if (status === 'closed') {
      return <Badge className="bg-gray-500 hover:bg-gray-600">Completed</Badge>;
    } else {
      return <Badge className="bg-blue-500 hover:bg-blue-600">Upcoming</Badge>;
    }
  };
  
  const getTournamentStatusBadge = (status: string) => {
    if (status === 'live') {
      return <Badge className="bg-red-500 hover:bg-red-600">LIVE</Badge>;
    } else if (status === 'ended') {
      return <Badge className="bg-gray-500 hover:bg-gray-600">Ended</Badge>;
    } else {
      return <Badge className="bg-blue-500 hover:bg-blue-600">Upcoming</Badge>;
    }
  };
  
  const formatTournamentDates = (startDate?: string, endDate?: string) => {
    if (!startDate && !endDate) {
      return 'Dates not available';
    }
    
    let formattedDate = '';
    
    if (startDate) {
      const start = new Date(startDate);
      formattedDate += start.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
    }
    
    if (endDate) {
      const end = new Date(endDate);
      formattedDate += ' - ' + end.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
    }
    
    return formattedDate;
  };
  
  const handleRetry = () => {
    setRetryCount(prev => prev + 1);
  };

  const handleCheckboxChange = (tournamentId: string, checked: boolean) => {
    setCheckedTournaments(prev => {
      const newChecked = new Set(prev);
      
      if (checked) {
        newChecked.add(tournamentId);
      } else {
        newChecked.delete(tournamentId);
      }
      
      return newChecked;
    });
  };

  const handleSaveMultiple = async () => {
    if (checkedTournaments.size === 0) {
      toast({
        title: "No Tournaments Selected",
        description: "Please select at least one tournament to save.",
        variant: "destructive"
      });
      return;
    }

    try {
      setSavingMultiple(true);
      
      // Get the external_ids of the selected tournaments
      const tournamentIds: string[] = [];
      tournaments.forEach(t => {
        if (checkedTournaments.has(t.id) && t.external_id) {
          tournamentIds.push(t.external_id);
        }
      });
      
      console.log('DEBUG: handleSaveMultiple - Sending external IDs to save:', tournamentIds);
      
      // Log the tournaments being saved for debugging
      console.log('DEBUG: Tournaments being saved:');
      tournaments.forEach(t => {
        if (checkedTournaments.has(t.id)) {
          console.log(`  - ID: ${t.id}, Name: ${t.name}, External ID: ${t.external_id}`);
        }
      });
      
      if (tournamentIds.length === 0) {
        toast({
          title: "No Valid Tournaments",
          description: "Selected tournaments don't have valid external IDs.",
          variant: "destructive"
        });
        setSavingMultiple(false);
        return;
      }
      
      const response = await fetch(`${config.apiServer.baseUrl}/tournaments/select-multiple`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ tournament_ids: tournamentIds })
      });
      
      if (!response.ok) {
        throw new Error(`Failed to save tournaments: ${response.status} ${response.statusText}`);
      }
      
      const responseData = await response.json();
      console.log('DEBUG: handleSaveMultiple - Save successful, response:', responseData);
      
      // Update tournaments list
      setTournaments(prev => 
        prev.map(t => checkedTournaments.has(t.id) ? { ...t, is_selected: true } : t)
      );
      
      // Clear checked tournaments
      setCheckedTournaments(new Set());
      
      // Refresh selected tournaments
      fetchTournamentData();
      
      toast({
        title: "Tournaments Saved",
        description: `${tournamentIds.length} tournament(s) have been saved to your database.`,
      });
    } catch (err) {
      console.error('Error saving tournaments:', err);
      console.log('DEBUG: handleSaveMultiple - Error saving tournaments:', err);
      toast({
        title: "Error",
        description: `Failed to save tournaments: ${err instanceof Error ? err.message : String(err)}`,
        variant: "destructive"
      });
    } finally {
      setSavingMultiple(false);
    }
  };

  const handleDeselectMultiple = async () => {
    if (checkedTournaments.size === 0) {
      toast({
        title: "No Tournaments Selected",
        description: "Please select at least one tournament to remove.",
        variant: "destructive"
      });
      return;
    }

    try {
      setSavingMultiple(true);
      
      // Get the external_ids of the selected tournaments
      const tournamentIds: string[] = [];
      selectedTournaments.forEach(t => {
        if (checkedTournaments.has(t.id) && t.external_id) {
          tournamentIds.push(t.external_id);
        }
      });
      
      console.log('DEBUG: handleDeselectMultiple - Sending external IDs to remove:', tournamentIds);
      
      if (tournamentIds.length === 0) {
        toast({
          title: "No Valid Tournaments",
          description: "Selected tournaments don't have valid external IDs.",
          variant: "destructive"
        });
        setSavingMultiple(false);
        return;
      }
      
      const response = await fetch(`${config.apiServer.baseUrl}/tournaments/deselect-multiple`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ tournament_ids: tournamentIds })
      });
      
      if (!response.ok) {
        throw new Error(`Failed to remove tournaments: ${response.status} ${response.statusText}`);
      }
      
      const data = await response.json();
      console.log('Tournaments removed:', data);
      
      // Update tournaments list
      setTournaments(prev => 
        prev.map(t => checkedTournaments.has(t.id) ? { ...t, is_selected: false } : t)
      );
      
      // Clear checked tournaments
      setCheckedTournaments(new Set());
      
      // Refresh selected tournaments
      fetchTournamentData();
      
      toast({
        title: "Tournaments Removed",
        description: `${tournamentIds.length} tournament(s) have been removed from your saved tournaments.`,
      });
    } catch (err) {
      console.error('Error removing tournaments:', err);
      toast({
        title: "Error",
        description: `Failed to remove tournaments: ${err instanceof Error ? err.message : String(err)}`,
        variant: "destructive"
      });
    } finally {
      setSavingMultiple(false);
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-6">Tennis Tournament Information</h1>
      
      <Tabs defaultValue="tournaments" className="mb-8" onValueChange={(value) => {
        setActiveTab(value);
        setCheckedTournaments(new Set());
      }}>
        <TabsList className="mb-4">
          <TabsTrigger value="tournaments">Tournaments</TabsTrigger>
          <TabsTrigger value="live">Live Matches</TabsTrigger>
          <TabsTrigger value="upcoming">Upcoming Matches</TabsTrigger>
          <TabsTrigger value="selected">Selected Tournaments</TabsTrigger>
          <TabsTrigger value="ended">Ended Tournaments</TabsTrigger>
        </TabsList>
        
        <TabsContent value="tournaments">
          {/* Multiple selection controls */}
          <div className="flex justify-between items-center mb-4">
            <div className="text-sm text-gray-500">
              <>{checkedTournaments.size} tournament(s) selected</>
            </div>
            <div className="flex gap-2">
              {checkedTournaments.size > 0 && (
                <Button 
                  variant="outline"
                  onClick={() => setCheckedTournaments(new Set())}
                  className="mr-2"
                >
                  Clear Selection
                </Button>
              )}
              {savingMultiple ? (
                <Button disabled>
                  Processing...
                </Button>
              ) : (
                <Button 
                  onClick={handleSaveMultiple}
                  disabled={checkedTournaments.size === 0}
                >
                  Save Selected
                </Button>
              )}
            </div>
          </div>

          <Table>
            <TableHeader>
              <TableRow>
                <TableHead className="w-[50px]"></TableHead> {/* Checkbox column */}
                <TableHead>Tournament</TableHead>
                <TableHead>Dates</TableHead>
                <TableHead>Status</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {loading ? (
                Array(5).fill(0).map((_, i) => (
                  <TableRow key={`skel-${i}`}>
                    <TableCell><Skeleton className="h-4 w-4" /></TableCell>
                    <TableCell><Skeleton className="h-4 w-3/4" /></TableCell>
                    <TableCell><Skeleton className="h-4 w-1/2" /></TableCell>
                    <TableCell><Skeleton className="h-6 w-16" /></TableCell>
                  </TableRow>
                ))
              ) : error ? (
                <TableRow>
                  <TableCell colSpan={4} className="p-4 bg-red-50 text-red-500 rounded-md text-center">
                    {error}
                  </TableCell>
                </TableRow>
              ) : tournaments.length === 0 ? (
                <TableRow>
                  <TableCell colSpan={4} className="p-4 bg-gray-50 text-gray-500 rounded-md text-center">
                    No current tournaments available.
                  </TableCell>
                </TableRow>
              ) : (
                tournaments.map((tournament) => (
                  <TableRow key={tournament.id} data-state={checkedTournaments.has(tournament.id) ? 'selected' : ''}>
                    <TableCell>
                      <input
                        type="checkbox"
                        id={`tournament-${tournament.id}`}
                        className="h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500"
                        checked={checkedTournaments.has(tournament.id)}
                        onChange={(e) => {
                          handleCheckboxChange(tournament.id, e.target.checked);
                        }}
                      />
                    </TableCell>
                    <TableCell>
                      <div className="font-medium">{tournament.name}</div>
                      <div className="text-sm text-muted-foreground">{tournament.category || 'Tennis Tournament'}</div>
                      <div className="text-xs text-gray-400">ID: {tournament.id}, ExternalID: {tournament.external_id || 'none'}</div>
                    </TableCell>
                    <TableCell className="text-sm text-muted-foreground">
                      {formatTournamentDates(tournament.start_date, tournament.end_date)}
                    </TableCell>
                    <TableCell>
                      {getTournamentStatusBadge(tournament.status)}
                    </TableCell>
                  </TableRow>
                ))
              )}
            </TableBody>
          </Table>
        </TabsContent>
        
        <TabsContent value="live">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {loading ? (
              Array(3).fill(0).map((_, i) => (
                <div key={i} className="overflow-hidden">
                  <div className="pb-2">
                    <Skeleton className="h-4 w-1/2 mb-2" />
                    <Skeleton className="h-6 w-3/4" />
                  </div>
                  <div>
                    <Skeleton className="h-16 w-full mb-2" />
                    <Skeleton className="h-4 w-1/3" />
                  </div>
                </div>
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
                <div key={match.id} className="overflow-hidden">
                  <div className="pb-2">
                    <div className="flex justify-between items-center">
                      <div>
                        {match.tournament.name}
                      </div>
                      {getStatusBadge(match)}
                    </div>
                    <div className="text-lg">
                      {match.venue?.name || 'Unknown Venue'}
                    </div>
                  </div>
                  <div>
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
                  </div>
                </div>
              ))
            )}
          </div>
        </TabsContent>
        
        <TabsContent value="upcoming">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {loading ? (
              Array(3).fill(0).map((_, i) => (
                <div key={i} className="overflow-hidden">
                  <div className="pb-2">
                    <Skeleton className="h-4 w-1/2 mb-2" />
                    <Skeleton className="h-6 w-3/4" />
                  </div>
                  <div>
                    <Skeleton className="h-16 w-full mb-2" />
                    <Skeleton className="h-4 w-1/3" />
                  </div>
                </div>
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
                <div key={match.id} className="overflow-hidden">
                  <div className="pb-2">
                    <div className="flex justify-between items-center">
                      <div>
                        {match.tournament.name}
                      </div>
                      {getStatusBadge(match)}
                    </div>
                    <div className="text-lg">
                      {match.venue?.name || 'Unknown Venue'}
                    </div>
                  </div>
                  <div>
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
                  </div>
                </div>
              ))
            )}
          </div>
        </TabsContent>
        
        <TabsContent value="selected">
          {/* Multiple deselection controls */}
          <div className="flex justify-between items-center mb-4">
            <div className="text-sm text-gray-500">
              <>{checkedTournaments.size} tournament(s) selected</>
            </div>
            <div className="flex gap-2">
              {checkedTournaments.size > 0 && (
                <Button 
                  variant="outline"
                  onClick={() => setCheckedTournaments(new Set())}
                  className="mr-2"
                >
                  Clear Selection
                </Button>
              )}
              {savingMultiple ? (
                <Button disabled variant="outline">
                  Processing...
                </Button>
              ) : (
                <Button 
                  onClick={handleDeselectMultiple}
                  disabled={checkedTournaments.size === 0}
                  variant="outline"
                >
                  Remove Selected
                </Button>
              )}
            </div>
          </div>
          
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead className="w-[50px]"></TableHead> {/* Checkbox column */}
                <TableHead>Tournament</TableHead>
                <TableHead>Dates</TableHead>
                <TableHead>Status</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {loading ? (
                Array(3).fill(0).map((_, i) => (
                  <TableRow key={`skel-sel-${i}`}>
                    <TableCell><Skeleton className="h-4 w-4" /></TableCell>
                    <TableCell><Skeleton className="h-4 w-3/4" /></TableCell>
                    <TableCell><Skeleton className="h-4 w-1/2" /></TableCell>
                    <TableCell><Skeleton className="h-6 w-16" /></TableCell>
                  </TableRow>
                ))
              ) : error ? (
                <TableRow>
                  <TableCell colSpan={4} className="p-4 bg-red-50 text-red-500 rounded-md text-center">
                    {error}
                  </TableCell>
                </TableRow>
              ) : selectedTournaments.length === 0 ? (
                <TableRow>
                  <TableCell colSpan={4} className="p-4 bg-gray-50 text-gray-500 rounded-md text-center">
                    No tournaments have been selected yet.
                  </TableCell>
                </TableRow>
              ) : (
                selectedTournaments.map((tournament) => (
                  <TableRow key={tournament.id} data-state={checkedTournaments.has(tournament.id) ? 'selected' : ''}>
                    <TableCell>
                       <input
                        type="checkbox"
                        id={`selected-tournament-${tournament.id}`}
                        className="h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500"
                        checked={checkedTournaments.has(tournament.id)}
                        onChange={(e) => {
                          handleCheckboxChange(tournament.id, e.target.checked)
                        }}
                      />
                    </TableCell>
                    <TableCell>
                      <div className="font-medium">{tournament.name}</div>
                      <div className="text-sm text-muted-foreground">{tournament.category || 'Tennis Tournament'}</div>
                      <div className="text-xs text-gray-400">ID: {tournament.id}, ExternalID: {tournament.external_id || 'none'}</div>
                    </TableCell>
                    <TableCell className="text-sm text-muted-foreground">
                      {formatTournamentDates(tournament.start_date, tournament.end_date)}
                    </TableCell>
                    <TableCell>
                      {getTournamentStatusBadge(tournament.status)}
                    </TableCell>
                  </TableRow>
                ))
              )}
            </TableBody>
          </Table>
        </TabsContent>
        
        <TabsContent value="ended">
          {/* Multiple deselection controls for ended tournaments */}
          <div className="flex justify-between items-center mb-4">
            <div className="text-sm text-gray-500">
              <>{checkedTournaments.size} tournament(s) selected</>
            </div>
            <div className="flex gap-2">
              {checkedTournaments.size > 0 && (
                <Button 
                  variant="outline"
                  onClick={() => setCheckedTournaments(new Set())}
                  className="mr-2"
                >
                  Clear Selection
                </Button>
              )}
              {savingMultiple ? (
                <Button disabled variant="outline">
                  Processing...
                </Button>
              ) : (
                <Button 
                  onClick={handleDeselectMultiple}
                  disabled={checkedTournaments.size === 0}
                  variant="outline"
                >
                  Remove Selected
                </Button>
              )}
            </div>
          </div>
          
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead className="w-[50px]"></TableHead> {/* Checkbox column */}
                <TableHead>Tournament</TableHead>
                <TableHead>Dates</TableHead>
                <TableHead>Status</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {loading ? (
                Array(3).fill(0).map((_, i) => (
                  <TableRow key={`skel-end-${i}`}>
                    <TableCell><Skeleton className="h-4 w-4" /></TableCell>
                    <TableCell><Skeleton className="h-4 w-3/4" /></TableCell>
                    <TableCell><Skeleton className="h-4 w-1/2" /></TableCell>
                    <TableCell><Skeleton className="h-6 w-16" /></TableCell>
                  </TableRow>
                ))
              ) : error ? (
                <TableRow>
                  <TableCell colSpan={4} className="p-4 bg-red-50 text-red-500 rounded-md text-center">
                    {error}
                  </TableCell>
                </TableRow>
              ) : endedTournaments.length === 0 ? (
                <TableRow>
                  <TableCell colSpan={4} className="p-4 bg-gray-50 text-gray-500 rounded-md text-center">
                    No ended tournaments have been saved yet.
                  </TableCell>
                </TableRow>
              ) : (
                endedTournaments.map((tournament) => (
                  <TableRow key={tournament.id} data-state={checkedTournaments.has(tournament.id) ? 'selected' : ''}>
                    <TableCell>
                      <input
                        type="checkbox"
                        id={`ended-tournament-${tournament.id}`}
                        className="h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500"
                        checked={checkedTournaments.has(tournament.id)}
                        onChange={(e) => {
                          handleCheckboxChange(tournament.id, e.target.checked)
                        }}
                      />
                    </TableCell>
                    <TableCell>
                      <div className="font-medium">{tournament.name}</div>
                      <div className="text-sm text-muted-foreground">{tournament.category || 'Tennis Tournament'}</div>
                      <div className="text-xs text-gray-400">ID: {tournament.id}, ExternalID: {tournament.external_id || 'none'}</div>
                    </TableCell>
                    <TableCell className="text-sm text-muted-foreground">
                      {formatTournamentDates(tournament.start_date, tournament.end_date)}
                    </TableCell>
                    <TableCell>
                      <Badge className="bg-gray-500 hover:bg-gray-600">Ended</Badge>
                    </TableCell>
                  </TableRow>
                ))
              )}
            </TableBody>
          </Table>
        </TabsContent>
      </Tabs>
    </div>
  );
}
