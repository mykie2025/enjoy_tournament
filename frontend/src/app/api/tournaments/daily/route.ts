import { NextResponse } from 'next/server';
import config from '../../../config';

export async function GET() {
  try {
    // Make a request to our backend API for daily tournament schedule
    const apiUrl = `${config.apiServer.baseUrl}/tournaments/api/today`;
    console.log(`Fetching daily tournaments from: ${apiUrl}`);
    
    const response = await fetch(
      apiUrl,
      { next: { revalidate: config.ui.autoRefreshInterval } }
    );
    
    if (!response.ok) {
      return NextResponse.json(
        { 
          status: 'error', 
          message: `Backend API returned ${response.status}: ${response.statusText}` 
        }, 
        { status: response.status }
      );
    }
    
    const data = await response.json();
    
    return NextResponse.json(data);
  } catch (error) {
    console.error('Error fetching daily tournament data:', error);
    return NextResponse.json(
      { 
        status: 'error', 
        message: error instanceof Error ? error.message : 'An unknown error occurred' 
      }, 
      { status: 500 }
    );
  }
}
