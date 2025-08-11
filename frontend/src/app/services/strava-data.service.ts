import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class StravaDataService {
  private readonly apiUrl = 'http://localhost:8000'; // Your backend URL

  constructor(private http: HttpClient) {}

  exchangeCodeForToken(code: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/auth/token`, { code });
  }

  refreshUserData(accessToken: string): Observable<any> {
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${accessToken}`
    });
    
    return this.http.post(`${this.apiUrl}/data/refresh`, {}, { headers });
  }

  getDataStatus(): Observable<any> {
    return this.http.get(`${this.apiUrl}/data/status`);
  }

  getUserProfile(accessToken: string): Observable<any> {
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${accessToken}`
    });
    
    return this.http.get(`${this.apiUrl}/user/profile`, { headers });
  }

  getUserStats(accessToken: string): Observable<any> {
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${accessToken}`
    });
    
    return this.http.get(`${this.apiUrl}/user/stats`, { headers });
  }

  getRecentActivities(accessToken: string, limit: number = 10): Observable<any> {
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${accessToken}`
    });
    
    return this.http.get(`${this.apiUrl}/user/recent-activities?limit=${limit}`, { headers });
  }

  getUserActivities(): Observable<any> {
    return this.http.get(`${this.apiUrl}/activities`);
  }

  getUserProfileOld(): Observable<any> {
    return this.http.get(`${this.apiUrl}/profile`);
  }
} 